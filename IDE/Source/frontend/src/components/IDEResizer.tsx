import {useRef,type PointerEvent} from 'react';

/** Pointer capture survives leaving the thin sash; keyboard resizing is equivalent. */
export default function IDEResizer({label,axis,value,min,max,reverse=false,onPreview,onCommit}:{label:string;axis:'x'|'y';value:number;min:number;max:number;reverse?:boolean;onPreview:(n:number)=>void;onCommit:(n:number)=>void}){
  const drag=useRef<{id:number;origin:number;initial:number;latest:number}|null>(null);
  const clamp=(n:number)=>Math.round(Math.min(max,Math.max(min,n)));
  function finish(e:PointerEvent){const d=drag.current;if(!d||e.pointerId!==d.id)return;drag.current=null;e.currentTarget.releasePointerCapture(d.id);onCommit(d.latest);}
  return <div className={`ide-sash ide-sash-${axis}`} role="separator" aria-label={label} aria-orientation={axis==='x'?'vertical':'horizontal'} aria-valuemin={min} aria-valuemax={max} aria-valuenow={value} tabIndex={0}
    onPointerDown={e=>{if(e.button!==0)return;e.preventDefault();e.currentTarget.setPointerCapture(e.pointerId);drag.current={id:e.pointerId,origin:axis==='x'?e.clientX:e.clientY,initial:value,latest:value};}}
    onPointerMove={e=>{const d=drag.current;if(!d||e.pointerId!==d.id)return;d.latest=clamp(d.initial+((axis==='x'?e.clientX:e.clientY)-d.origin)*(reverse?-1:1));onPreview(d.latest);}}
    onPointerUp={finish} onPointerCancel={e=>{const d=drag.current;if(!d)return;drag.current=null;onPreview(d.initial);e.currentTarget.releasePointerCapture(d.id);}}
    onKeyDown={e=>{const decrease=axis==='x'?'ArrowLeft':'ArrowUp',increase=axis==='x'?'ArrowRight':'ArrowDown';if(![decrease,increase,'Home','End'].includes(e.key))return;e.preventDefault();const n=e.key==='Home'?min:e.key==='End'?max:clamp(value+(e.key===increase?1:-1)*(reverse?-1:1)*(e.shiftKey?40:10));onPreview(n);onCommit(n);}}/>
}
