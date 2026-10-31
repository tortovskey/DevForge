import {CheckCircle2, CircleX, Terminal, Cpu} from 'lucide-react';
import type {Lesson,RunResult} from '../types';
export function same(a:unknown,b:unknown):boolean {
  if(a===b)return true;
  if(!a||!b||typeof a!=='object'||typeof b!=='object')return false;
  if(Array.isArray(a)!==Array.isArray(b))return false;
  const x=Object.keys(a),y=Object.keys(b);
  return x.length===y.length&&x.every(k=>Object.hasOwn(b,k)&&same((a as Record<string,unknown>)[k],(b as Record<string,unknown>)[k]));
}
export default function Output({result,lesson}:{result:RunResult|null;lesson?:Lesson}){
  const passed=result?.results.filter(r=>!r.error&&same(r.actual,lesson?.tests.find(t=>t.id===r.id)?.expected)).length||0;
  const flags = result?.registers?.flags as { zf?: number; sf?: number; cf?: number; of?: number } | undefined;
  return <div className="output-content" aria-live="polite">
    {!result&&<div className="empty-output"><Terminal size={24}/><span>Всё начинается с первой строки.</span><small>Запустите код · Ctrl + Enter</small></div>}
    {result?.error&&<pre className="error-text">{result.error}</pre>}
    {result?.stdout&&<pre>{result.stdout}</pre>}
    {result?.stderr&&<pre className="error-text">{result.stderr}</pre>}
    {result?.registers&&<div className="registers-panel">
      <div className="registers-header">
        <span className="reg-title"><Cpu size={14}/>Регистры x86-64</span>
        {flags&&<span className="flags-badge">ZF:{flags.zf ?? 0} SF:{flags.sf ?? 0} CF:{flags.cf ?? 0} OF:{flags.of ?? 0} | Exit:{result.registers.exitCode}</span>}
      </div>
      <div className="registers-grid">
        {['rax','rbx','rcx','rdx','rsi','rdi','rsp','rbp','r8','r9','r10','r11','r12','r13','r14','r15'].map(r=><div key={r} className="reg-item"><span className="reg-name">{r.toUpperCase()}:</span><span className="reg-val">{String(result.registers![r]||'0x0000000000000000')}</span></div>)}
      </div>
    </div>}
    {!!result?.results.length&&<><div className={`test-summary ${passed===result.results.length?'success':'error-text'}`}>Tests passed: {passed}/{result.results.length}</div>{result.results.map(r=>{const test=lesson?.tests.find(t=>t.id===r.id);const ok=!r.error&&same(r.actual,test?.expected);return <div key={r.id} className="test-row">{ok?<CheckCircle2 size={16} className="success"/>:<CircleX size={16} className="error-text"/>}<div><strong>{test?.label}</strong>{!ok&&<pre>{r.error||`Ожидалось: ${JSON.stringify(test?.expected)}\nПолучено: ${JSON.stringify(r.actual)}`}</pre>}</div></div>;})}</>}
    {result?.tables.map((table,i)=><div className="table-scroll" key={i}><table><thead><tr>{table.columns.map((c,j)=><th key={j}>{c}</th>)}</tr></thead><tbody>{table.values.map((row,j)=><tr key={j}>{row.map((cell,k)=><td key={k}>{cell===null?<em>NULL</em>:String(cell)}</td>)}</tr>)}</tbody></table><small className="muted">{table.values.length} строк</small></div>)}
  </div>;
}
