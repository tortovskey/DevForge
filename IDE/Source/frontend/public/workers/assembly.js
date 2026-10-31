/* DevForge Assembly (x86-64 NASM) Emulator Worker */
/* Models Linux x86-64 System V ABI, registers, stack, memory, and syscalls */

let output = '', errors = '';

function append(val, isError = false) {
  const limit = 32000;
  const str = String(val);
  if (isError) {
    if (errors.length < limit) errors += str.slice(0, limit - errors.length);
  } else {
    if (output.length < limit) output += str.slice(0, limit - output.length);
  }
}

class X86_64_Machine {
  constructor(stdin = '') {
    this.memory = new Uint8Array(1024 * 1024 * 16); // 16MB linear address space
    this.dataBase = 0x400000;
    this.stackBase = 0x700000;

    this.regs = {
      rax: 0n, rbx: 0n, rcx: 0n, rdx: 0n,
      rsi: 0n, rdi: 0n, rbp: BigInt(this.stackBase), rsp: BigInt(this.stackBase),
      r8: 0n, r9: 0n, r10: 0n, r11: 0n, r12: 0n, r13: 0n, r14: 0n, r15: 0n
    };

    this.flags = { zf: 0, sf: 0, cf: 0, of: 0 };
    this.labels = {};
    this.constants = {};
    this.instructions = [];
    this.ip = 0;
    this.exitCode = 0;
    this.halted = false;

    const text = String(stdin || '').replace(/\r\n/g, '\n');
    this.stdinLines = text ? text.split('\n') : [];
    if (text.endsWith('\n')) this.stdinLines.pop();
    this.stdinPos = 0;
  }

  memRead(addr, size = 8) {
    const offset = Number(addr);
    if (offset < 0 || offset + size > this.memory.length) return 0n;
    let val = 0n;
    for (let i = 0; i < size; i++) {
      val |= BigInt(this.memory[offset + i]) << BigInt(i * 8);
    }
    return val;
  }

  memWrite(addr, val, size = 8) {
    const offset = Number(addr);
    if (offset < 0 || offset + size > this.memory.length) return;
    let v = BigInt(val);
    for (let i = 0; i < size; i++) {
      this.memory[offset + i] = Number(v & 0xffn);
      v >>= 8n;
    }
  }

  memReadString(addr, maxLen = 4096) {
    const offset = Number(addr);
    let str = '';
    for (let i = 0; i < maxLen; i++) {
      const b = this.memory[offset + i];
      if (b === 0 || b === undefined) break;
      str += String.fromCharCode(b);
    }
    return str;
  }

  memReadBytes(addr, count) {
    const offset = Number(addr);
    let str = '';
    for (let i = 0; i < count; i++) {
      const b = this.memory[offset + i] || 0;
      str += String.fromCharCode(b);
    }
    return str;
  }

  getReg(name) {
    const n = name.toLowerCase();
    // 64-bit
    if (this.regs[n] !== undefined) return this.regs[n];
    // 32-bit
    const map32 = { eax:'rax', ebx:'rbx', ecx:'rcx', edx:'rdx', esi:'rsi', edi:'rdi', esp:'rsp', ebp:'rbp', r8d:'r8', r9d:'r9', r10d:'r10', r11d:'r11', r12d:'r12', r13d:'r13', r14d:'r14', r15d:'r15' };
    if (map32[n]) return this.regs[map32[n]] & 0xffffffffn;
    // 16-bit
    const map16 = { ax:'rax', bx:'rbx', cx:'rcx', dx:'rdx', si:'rsi', di:'rdi', sp:'rsp', bp:'rbp', r8w:'r8', r9w:'r9', r10w:'r10', r11w:'r11', r12w:'r12', r13w:'r13', r14w:'r14', r15w:'r15' };
    if (map16[n]) return this.regs[map16[n]] & 0xffffn;
    // 8-bit low
    const map8l = { al:'rax', bl:'rbx', cl:'rcx', dl:'rdx', sil:'rsi', dil:'rdi', spl:'rsp', bpl:'rbp', r8b:'r8', r9b:'r9', r10b:'r10', r11b:'r11', r12b:'r12', r13b:'r13', r14b:'r14', r15b:'r15' };
    if (map8l[n]) return this.regs[map8l[n]] & 0xffn;
    // 8-bit high
    const map8h = { ah:'rax', bh:'rbx', ch:'rcx', dh:'rdx' };
    if (map8h[n]) return (this.regs[map8h[n]] >> 8n) & 0xffn;
    return null;
  }

  setReg(name, val) {
    const n = name.toLowerCase();
    let v = BigInt(val);
    // 64-bit
    if (this.regs[n] !== undefined) {
      this.regs[n] = v & 0xffffffffffffffffn;
      return true;
    }
    // 32-bit (x86-64 zeroes upper 32 bits!)
    const map32 = { eax:'rax', ebx:'rbx', ecx:'rcx', edx:'rdx', esi:'rsi', edi:'rdi', esp:'rsp', ebp:'rbp', r8d:'r8', r9d:'r9', r10d:'r10', r11d:'r11', r12d:'r12', r13d:'r13', r14d:'r14', r15d:'r15' };
    if (map32[n]) {
      this.regs[map32[n]] = v & 0xffffffffn;
      return true;
    }
    // 16-bit (preserves upper bits)
    const map16 = { ax:'rax', bx:'rbx', cx:'rcx', dx:'rdx', si:'rsi', di:'rdi', sp:'rsp', bp:'rbp', r8w:'r8', r9w:'r9', r10w:'r10', r11w:'r11', r12w:'r12', r13w:'r13', r14w:'r14', r15w:'r15' };
    if (map16[n]) {
      const orig = this.regs[map16[n]];
      this.regs[map16[n]] = (orig & ~0xffffn) | (v & 0xffffn);
      return true;
    }
    // 8-bit low
    const map8l = { al:'rax', bl:'rbx', cl:'rcx', dl:'rdx', sil:'rsi', dil:'rdi', spl:'rsp', bpl:'rbp', r8b:'r8', r9b:'r9', r10b:'r10', r11b:'r11', r12b:'r12', r13b:'r13', r14b:'r14', r15b:'r15' };
    if (map8l[n]) {
      const orig = this.regs[map8l[n]];
      this.regs[map8l[n]] = (orig & ~0xffn) | (v & 0xffn);
      return true;
    }
    // 8-bit high
    const map8h = { ah:'rax', bh:'rbx', ch:'rcx', dh:'rdx' };
    if (map8h[n]) {
      const orig = this.regs[map8h[n]];
      this.regs[map8h[n]] = (orig & ~0xff00n) | ((v & 0xffn) << 8n);
      return true;
    }
    return false;
  }

  parseOperand(op) {
    if (!op) return { type: 'none' };
    let s = op.trim();

    // Check size prefix
    let size = 8;
    if (/^byte\b/i.test(s)) { size = 1; s = s.replace(/^byte\s+/i, ''); }
    else if (/^word\b/i.test(s)) { size = 2; s = s.replace(/^word\s+/i, ''); }
    else if (/^dword\b/i.test(s)) { size = 4; s = s.replace(/^dword\s+/i, ''); }
    else if (/^qword\b/i.test(s)) { size = 8; s = s.replace(/^qword\s+/i, ''); }

    // Memory [addr]
    if (s.startsWith('[') && s.endsWith(']')) {
      const expr = s.slice(1, -1).trim();
      return { type: 'mem', expr, size };
    }

    // Register
    if (this.getReg(s) !== null) {
      return { type: 'reg', name: s };
    }

    // Constant equ
    if (this.constants[s] !== undefined) {
      return { type: 'imm', value: BigInt(this.constants[s]) };
    }

    // Label address
    if (this.labels[s] !== undefined) {
      return { type: 'imm', value: BigInt(this.labels[s]) };
    }

    // Immediate number or char
    if (/^'(\\.|[^'])'$/.test(s)) {
      return { type: 'imm', value: BigInt(s.charCodeAt(1)) };
    }
    if (/^0x[0-9a-fA-F]+$/i.test(s) || /^-?[0-9]+$/.test(s)) {
      return { type: 'imm', value: BigInt(s) };
    }

    // Raw label name (for jmp/call)
    return { type: 'label', name: s };
  }

  evalMemAddr(expr) {
    // Examples: rbp-8, rdi + rsi*4 + 16, msg, msg + 5
    const parts = expr.split(/([+-])/).map(p => p.trim()).filter(Boolean);
    let total = 0n;
    let sign = 1n;

    for (let i = 0; i < parts.length; i++) {
      const p = parts[i];
      if (p === '+') { sign = 1n; continue; }
      if (p === '-') { sign = -1n; continue; }

      // Handle multiplication: reg*scale
      if (p.includes('*')) {
        const [r, scale] = p.split('*').map(x => x.trim());
        const rVal = this.getReg(r) ?? (this.labels[r] !== undefined ? BigInt(this.labels[r]) : 0n);
        total += sign * rVal * BigInt(scale);
        continue;
      }

      const rVal = this.getReg(p);
      if (rVal !== null) {
        total += sign * rVal;
      } else if (this.labels[p] !== undefined) {
        total += sign * BigInt(this.labels[p]);
      } else if (this.constants[p] !== undefined) {
        total += sign * BigInt(this.constants[p]);
      } else if (/^0x[0-9a-fA-F]+$/i.test(p) || /^-?[0-9]+$/.test(p)) {
        total += sign * BigInt(p);
      }
    }
    return total;
  }

  getValue(parsed) {
    if (parsed.type === 'reg') return this.getReg(parsed.name);
    if (parsed.type === 'imm') return parsed.value;
    if (parsed.type === 'mem') {
      const addr = this.evalMemAddr(parsed.expr);
      return this.memRead(addr, parsed.size);
    }
    if (parsed.type === 'label' && this.labels[parsed.name] !== undefined) {
      return BigInt(this.labels[parsed.name]);
    }
    return 0n;
  }

  setValue(parsed, val) {
    let v = BigInt(val);
    if (parsed.type === 'reg') {
      this.setReg(parsed.name, v);
    } else if (parsed.type === 'mem') {
      const addr = this.evalMemAddr(parsed.expr);
      this.memWrite(addr, v, parsed.size);
    }
  }

  updateFlags(res, size = 64) {
    const mask = (1n << BigInt(size)) - 1n;
    const signBit = 1n << BigInt(size - 1);
    const masked = res & mask;
    this.flags.zf = masked === 0n ? 1 : 0;
    this.flags.sf = (masked & signBit) !== 0n ? 1 : 0;
  }

  assemble(source) {
    const lines = source.split('\n');
    let curSection = '.text';
    let dataOffset = this.dataBase;

    // First pass: collect labels, equs, and memory layouts
    for (let line of lines) {
      line = line.replace(/;.*$/, '').trim();
      if (!line) continue;

      if (/^section\s+\.data/i.test(line)) { curSection = '.data'; continue; }
      if (/^section\s+\.bss/i.test(line)) { curSection = '.bss'; continue; }
      if (/^section\s+\.text/i.test(line)) { curSection = '.text'; continue; }
      if (/^global\b/i.test(line) || /^extern\b/i.test(line)) continue;

      // Handle EQU: NAME equ VALUE or NAME: equ VALUE
      const equMatch = line.match(/^([a-zA-Z0-9_]+):?\s+equ\s+(.+)$/i);
      if (equMatch) {
        const name = equMatch[1];
        let valExpr = equMatch[2].trim();
        // Handle $-msg length calculation
        if (valExpr.startsWith('$-') || valExpr.startsWith('$ -')) {
          const prevLabel = valExpr.replace(/^\$\s*-\s*/, '').trim();
          if (this.labels[prevLabel] !== undefined) {
            this.constants[name] = dataOffset - this.labels[prevLabel];
          } else {
            this.constants[name] = 0;
          }
        } else {
          try { this.constants[name] = Number(valExpr); } catch { this.constants[name] = 0; }
        }
        continue;
      }

      // Handle label at start (with or without colon)
      let labelName = null;
      const colonMatch = line.match(/^([a-zA-Z0-9_]+):\s*(.*)$/);
      if (colonMatch) {
        labelName = colonMatch[1];
        line = colonMatch[2];
      } else {
        const dataMatch = line.match(/^([a-zA-Z0-9_]+)\s+(db|dw|dd|dq|resb|resw|resd|resq)\s+(.*)$/i);
        if (dataMatch) {
          labelName = dataMatch[1];
          line = `${dataMatch[2]} ${dataMatch[3]}`;
        }
      }

      if (labelName) {
        if (curSection === '.data' || curSection === '.bss') {
          this.labels[labelName] = dataOffset;
        } else {
          this.labels[labelName] = this.instructions.length;
        }
      }

      if (!line) continue;

      // Handle Data Directives in .data / .bss
      if (curSection === '.data' || curSection === '.bss') {
        const dataDirMatch = line.match(/^(db|dw|dd|dq|resb|resw|resd|resq)\s+(.+)$/i);
        if (dataDirMatch) {
          const dir = dataDirMatch[1].toLowerCase();
          const rest = dataDirMatch[2].trim();
          if (dir === 'resb') { dataOffset += Number(rest); continue; }
          if (dir === 'resw') { dataOffset += Number(rest) * 2; continue; }
          if (dir === 'resd') { dataOffset += Number(rest) * 4; continue; }
          if (dir === 'resq') { dataOffset += Number(rest) * 8; continue; }

          // Split comma separated values, respecting strings
          const items = [];
          let cur = '', inQuote = false;
          for (let ch of rest) {
            if (ch === '"' || ch === "'") inQuote = !inQuote;
            if (ch === ',' && !inQuote) { items.push(cur.trim()); cur = ''; }
            else { cur += ch; }
          }
          if (cur.trim()) items.push(cur.trim());

          for (let it of items) {
            if (/^["'].*["']$/.test(it)) {
              const strVal = it.slice(1, -1);
              for (let i = 0; i < strVal.length; i++) {
                this.memory[dataOffset++] = strVal.charCodeAt(i);
              }
            } else {
              const num = Number(it) || 0;
              const size = dir === 'db' ? 1 : (dir === 'dw' ? 2 : (dir === 'dd' ? 4 : 8));
              let tmp = BigInt(num);
              for (let b = 0; b < size; b++) {
                this.memory[dataOffset++] = Number(tmp & 0xffn);
                tmp >>= 8n;
              }
            }
          }
          continue;
        }
      }

      // Instruction in .text
      const instParts = line.match(/^([a-zA-Z]+)(?:\s+(.*))?$/);
      if (instParts) {
        const mnemonic = instParts[1].toLowerCase();
        const operandsStr = instParts[2] || '';
        const rawOps = [];
        let cur = '', inBrackets = false;
        for (let ch of operandsStr) {
          if (ch === '[') inBrackets = true;
          if (ch === ']') inBrackets = false;
          if (ch === ',' && !inBrackets) { rawOps.push(cur.trim()); cur = ''; }
          else { cur += ch; }
        }
        if (cur.trim()) rawOps.push(cur.trim());

        this.instructions.push({ mnemonic, operands: rawOps });
      }
    }

    // Set entry point (_start or main or instruction 0)
    if (this.labels['_start'] !== undefined) {
      this.ip = this.labels['_start'];
    } else if (this.labels['main'] !== undefined) {
      this.ip = this.labels['main'];
    } else {
      this.ip = 0;
    }
  }

  step() {
    if (this.ip < 0 || this.ip >= this.instructions.length || this.halted) {
      this.halted = true;
      return false;
    }

    const inst = this.instructions[this.ip++];
    const { mnemonic, operands } = inst;
    const op1 = operands[0] ? this.parseOperand(operands[0]) : null;
    const op2 = operands[1] ? this.parseOperand(operands[1]) : null;

    switch (mnemonic) {
      case 'mov': {
        const val = this.getValue(op2);
        this.setValue(op1, val);
        break;
      }
      case 'lea': {
        if (op1 && op2 && op2.type === 'mem') {
          const addr = this.evalMemAddr(op2.expr);
          this.setValue(op1, addr);
        }
        break;
      }
      case 'xchg': {
        const v1 = this.getValue(op1);
        const v2 = this.getValue(op2);
        this.setValue(op1, v2);
        this.setValue(op2, v1);
        break;
      }
      case 'add': {
        const v1 = this.getValue(op1);
        const v2 = this.getValue(op2);
        const res = v1 + v2;
        this.setValue(op1, res);
        this.updateFlags(res);
        this.flags.cf = res > 0xffffffffffffffffn ? 1 : 0;
        break;
      }
      case 'sub': {
        const v1 = this.getValue(op1);
        const v2 = this.getValue(op2);
        const res = v1 - v2;
        this.setValue(op1, res);
        this.updateFlags(res);
        this.flags.cf = v1 < v2 ? 1 : 0;
        break;
      }
      case 'inc': {
        const v = this.getValue(op1) + 1n;
        this.setValue(op1, v);
        this.updateFlags(v);
        break;
      }
      case 'dec': {
        const v = this.getValue(op1) - 1n;
        this.setValue(op1, v);
        this.updateFlags(v);
        break;
      }
      case 'neg': {
        const v = -this.getValue(op1);
        this.setValue(op1, v);
        this.updateFlags(v);
        break;
      }
      case 'imul':
      case 'mul': {
        if (op2) {
          const v1 = this.getValue(op1);
          const v2 = this.getValue(op2);
          const res = v1 * v2;
          this.setValue(op1, res);
          this.updateFlags(res);
        } else {
          const v = this.getValue(op1);
          const res = this.regs.rax * v;
          this.regs.rax = res & 0xffffffffffffffffn;
          this.regs.rdx = (res >> 64n) & 0xffffffffffffffffn;
          this.updateFlags(res);
        }
        break;
      }
      case 'idiv':
      case 'div': {
        const divisor = this.getValue(op1);
        if (divisor === 0n) {
          append('Исключение x86-64: деление на ноль (#DE)\n', true);
          this.halted = true;
          return false;
        }
        const dividend = (this.regs.rdx << 64n) | (this.regs.rax & 0xffffffffffffffffn);
        this.regs.rax = (dividend / divisor) & 0xffffffffffffffffn;
        this.regs.rdx = (dividend % divisor) & 0xffffffffffffffffn;
        break;
      }
      case 'and': {
        const res = this.getValue(op1) & this.getValue(op2);
        this.setValue(op1, res);
        this.updateFlags(res);
        this.flags.cf = 0; this.flags.of = 0;
        break;
      }
      case 'or': {
        const res = this.getValue(op1) | this.getValue(op2);
        this.setValue(op1, res);
        this.updateFlags(res);
        this.flags.cf = 0; this.flags.of = 0;
        break;
      }
      case 'xor': {
        const res = this.getValue(op1) ^ this.getValue(op2);
        this.setValue(op1, res);
        this.updateFlags(res);
        this.flags.cf = 0; this.flags.of = 0;
        break;
      }
      case 'not': {
        const res = ~this.getValue(op1);
        this.setValue(op1, res);
        break;
      }
      case 'shl':
      case 'sal': {
        const count = Number(this.getValue(op2));
        const res = this.getValue(op1) << BigInt(count);
        this.setValue(op1, res);
        this.updateFlags(res);
        break;
      }
      case 'shr': {
        const count = Number(this.getValue(op2));
        const res = this.getValue(op1) >> BigInt(count);
        this.setValue(op1, res);
        this.updateFlags(res);
        break;
      }
      case 'cmp': {
        const v1 = this.getValue(op1);
        const v2 = this.getValue(op2);
        const res = v1 - v2;
        this.updateFlags(res);
        this.flags.cf = v1 < v2 ? 1 : 0;
        break;
      }
      case 'test': {
        const res = this.getValue(op1) & this.getValue(op2);
        this.updateFlags(res);
        this.flags.cf = 0; this.flags.of = 0;
        break;
      }
      case 'push': {
        const val = this.getValue(op1);
        this.regs.rsp -= 8n;
        this.memWrite(this.regs.rsp, val, 8);
        break;
      }
      case 'pop': {
        const val = this.memRead(this.regs.rsp, 8);
        this.regs.rsp += 8n;
        this.setValue(op1, val);
        break;
      }
      case 'call': {
        const target = op1.type === 'label' ? this.labels[op1.name] : Number(this.getValue(op1));
        if (target !== undefined) {
          this.regs.rsp -= 8n;
          this.memWrite(this.regs.rsp, BigInt(this.ip), 8);
          this.ip = target;
        }
        break;
      }
      case 'ret': {
        const retIp = Number(this.memRead(this.regs.rsp, 8));
        this.regs.rsp += 8n;
        this.ip = retIp;
        break;
      }
      case 'jmp': {
        const target = op1.type === 'label' ? this.labels[op1.name] : Number(this.getValue(op1));
        if (target !== undefined) this.ip = target;
        break;
      }
      case 'je':
      case 'jz': {
        if (this.flags.zf === 1) this.ip = this.labels[op1.name];
        break;
      }
      case 'jne':
      case 'jnz': {
        if (this.flags.zf === 0) this.ip = this.labels[op1.name];
        break;
      }
      case 'jl':
      case 'jnge': {
        if (this.flags.sf !== this.flags.of) this.ip = this.labels[op1.name];
        break;
      }
      case 'jle':
      case 'jng': {
        if (this.flags.zf === 1 || this.flags.sf !== this.flags.of) this.ip = this.labels[op1.name];
        break;
      }
      case 'jg':
      case 'jnle': {
        if (this.flags.zf === 0 && this.flags.sf === this.flags.of) this.ip = this.labels[op1.name];
        break;
      }
      case 'jge':
      case 'jnl': {
        if (this.flags.sf === this.flags.of) this.ip = this.labels[op1.name];
        break;
      }
      case 'loop': {
        this.regs.rcx -= 1n;
        if (this.regs.rcx !== 0n) this.ip = this.labels[op1.name];
        break;
      }
      case 'syscall': {
        const syscallNr = Number(this.regs.rax);
        if (syscallNr === 60) {
          // sys_exit
          this.exitCode = Number(this.regs.rdi);
          this.halted = true;
          return false;
        } else if (syscallNr === 1) {
          // sys_write: rdi=fd, rsi=buf, rdx=count
          const fd = Number(this.regs.rdi);
          const bufAddr = this.regs.rsi;
          const count = Number(this.regs.rdx);
          const textOut = this.memReadBytes(bufAddr, count);
          if (fd === 1) {
            append(textOut);
          } else {
            append(textOut, true);
          }
          this.regs.rax = BigInt(count);
        } else if (syscallNr === 0) {
          // sys_read: rdi=fd, rsi=buf, rdx=count
          const bufAddr = this.regs.rsi;
          const maxCount = Number(this.regs.rdx);
          let inputStr = '';
          if (this.stdinPos < this.stdinLines.length) {
            inputStr = this.stdinLines[this.stdinPos++] + '\n';
          }
          const bytesToCopy = Math.min(inputStr.length, maxCount);
          for (let i = 0; i < bytesToCopy; i++) {
            this.memory[Number(bufAddr) + i] = inputStr.charCodeAt(i);
          }
          this.regs.rax = BigInt(bytesToCopy);
        } else {
          append(`Неподдерживаемый системный вызов x86-64 syscall #${syscallNr}\n`, true);
        }
        break;
      }
      case 'nop':
        break;
      default:
        append(`Неизвестная инструкция ассемблера: '${mnemonic}'\n`, true);
        break;
    }
    return true;
  }

  run(maxSteps = 100000) {
    let steps = 0;
    while (!this.halted && steps < maxSteps) {
      if (!this.step()) break;
      steps++;
    }
    if (steps >= maxSteps) {
      append('Превышен лимит тактов процессора (100000 шагов). Возможен бесконечный цикл.\n', true);
    }
  }

  getRegistersDump() {
    const dump = {};
    for (const [k, v] of Object.entries(this.regs)) {
      dump[k] = '0x' + v.toString(16).padStart(16, '0');
    }
    dump.flags = { ...this.flags };
    dump.exitCode = this.exitCode;
    return dump;
  }
}

if (typeof self !== 'undefined' && self.postMessage) {
  self.postMessage({ type: 'ready' });
}

self.onmessage = async ({ data }) => {
  output = '';
  errors = '';
  const results = [];

  try {
    const code = data.code || '';
    const vm = new X86_64_Machine(data.stdin || '');
    vm.assemble(code);
    vm.run();

    const regDump = vm.getRegistersDump();

    if (data.tests && Array.isArray(data.tests)) {
      for (const test of data.tests) {
        try {
          if (test.expression) {
            const expr = test.expression.trim().toLowerCase();
            let actual = null;
            if (expr === 'exit_code' || expr === 'exitcode') {
              actual = vm.exitCode;
            } else if (vm.regs[expr] !== undefined) {
              actual = Number(vm.regs[expr]);
            } else if (vm.getReg(expr) !== null) {
              actual = Number(vm.getReg(expr));
            } else if (vm.labels[expr] !== undefined) {
              actual = Number(vm.memRead(vm.labels[expr], 8));
            } else if (expr.startsWith('[') && expr.endsWith(']')) {
              const memAddr = vm.evalMemAddr(expr.slice(1, -1));
              actual = Number(vm.memRead(memAddr, 8));
            }
            results.push({
              id: test.id,
              actual,
              error: null
            });
          } else {
            // Stdout comparison test
            const normalizedOut = output.trim();
            results.push({
              id: test.id,
              actual: normalizedOut,
              error: null
            });
          }
        } catch (tErr) {
          results.push({
            id: test.id,
            actual: null,
            error: tErr.message
          });
        }
      }
    }

    self.postMessage({
      type: 'result',
      result: {
        stdout: output,
        stderr: errors,
        tables: [],
        registers: regDump,
        results
      }
    });
  } catch (err) {
    append('Ошибка эмуляции x86-64 NASM: ' + (err.message || String(err)) + '\n', true);
    self.postMessage({
      type: 'result',
      result: {
        stdout: output,
        stderr: errors,
        tables: [],
        results: []
      }
    });
  }
};
