import type {ProjectFile,RunResult,Test} from '../types';
export function documentSource(code:string,files:ProjectFile[]=[],active='index.html'){
  const html=active.endsWith('.css')?files.find(f=>f.name.endsWith('.html'))?.content||'<main class="card"><h1>CSS Playground</h1><p>Измените оформление этой карточки.</p></main>':code;
  const doc=new DOMParser().parseFromString(html,'text/html');
  doc.querySelectorAll('script,iframe,object,embed,base,meta[http-equiv],link[rel="import"]').forEach(el=>el.remove());
  doc.querySelectorAll('*').forEach(el=>{for(const attr of [...el.attributes])if(attr.name.toLowerCase().startsWith('on'))el.removeAttribute(attr.name);});
  doc.querySelectorAll('link[rel="stylesheet"]').forEach(link=>{
    const file=files.find(f=>f.name===link.getAttribute('href'));if(file){const style=doc.createElement('style');style.textContent=file.name===active?code:file.content;link.replaceWith(style);}else link.remove();
  });
  if(active.endsWith('.css')&&!files.some(f=>f.name.endsWith('.html')&&f.content.includes(active))){const style=doc.createElement('style');style.textContent=code;doc.head.append(style);}
  const csp=doc.createElement('meta');csp.httpEquiv='Content-Security-Policy';csp.content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; font-src 'none'; form-action 'none'; base-uri 'none'; script-src 'none'";doc.head.prepend(csp);
  return '<!doctype html>'+doc.documentElement.outerHTML;
}
export async function checkHtml(source:string,tests:Test[]):Promise<RunResult>{
  const start=performance.now();const frame=document.createElement('iframe');
  // Trusted checker can inspect the DOM; scripts are denied by sandbox AND CSP.
  frame.sandbox.add('allow-same-origin');frame.style.cssText='position:fixed;left:-10000px;width:800px;height:600px;visibility:hidden';
  const result:RunResult={stdout:'Предпросмотр обновлён.',stderr:'',tables:[],results:[]};
  try{
    await new Promise<void>((resolve,reject)=>{const timer=setTimeout(()=>reject(new Error('Таймаут HTML-предпросмотра')),3000);frame.onload=()=>{clearTimeout(timer);resolve();};frame.srcdoc=source;document.body.append(frame);});
    const doc=frame.contentDocument!;
    for(const t of tests){try{
      frame.style.width=`${t.viewport||800}px`;
      // Read layout after changing the iframe viewport so media queries are current.
      void frame.contentDocument!.documentElement.offsetWidth;
      const rule=t.dom!;const nodes=doc.querySelectorAll(rule.selector);const node=nodes[0] as HTMLElement|undefined;let actual:unknown;
      if(t.focus&&node){node.focus();}
      if(rule.property==='count')actual=nodes.length;
      else if(rule.property==='texts')actual=[...nodes].map(n=>n.textContent?.trim());
      else if(!node)throw new Error(`Элемент ${rule.selector} не найден`);
      else if(rule.property==='text')actual=node.textContent?.trim();
      else if(rule.property==='attr')actual=node.getAttribute(rule.attribute!);
      else if(rule.property==='style')actual=frame.contentWindow!.getComputedStyle(node).getPropertyValue(rule.css!);
      else if(rule.property==='columns')actual=frame.contentWindow!.getComputedStyle(node).gridTemplateColumns.split(' ').filter(Boolean).length;
      else throw new Error('Неизвестная проверка');
      result.results.push({id:t.id,actual,error:null});
    }catch(error){result.results.push({id:t.id,actual:null,error:String(error)});}}
  }catch(error){result.error=String(error);}finally{frame.remove();}
  return {...result,duration:performance.now()-start};
}
