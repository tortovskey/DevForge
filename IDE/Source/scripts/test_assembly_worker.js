let lastMsg = null;
globalThis.self = {
  postMessage: (msg) => { lastMsg = msg; }
};

require('../frontend/public/workers/assembly.js');

async function runTest() {
  const code = `
section .data
    msg db "Hello, x86-64 NASM!", 10
    len equ $ - msg

section .text
    global _start

_start:
    ; sys_write(1, msg, len)
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, len
    syscall

    ; calculate 25 + 17 = 42
    mov rax, 25
    add rax, 17

    ; sys_exit(0)
    mov rdi, 0
    mov rax, 60
    syscall
  `;

  await globalThis.self.onmessage({
    data: {
      code,
      tests: [
        { id: 't1', label: 'stdout test', expected: 'Hello, x86-64 NASM!' },
        { id: 't2', expression: 'exit_code', expected: 0 }
      ]
    }
  });

  console.log('Assembly Result:', JSON.stringify(lastMsg, null, 2));
}

runTest().catch(console.error);
