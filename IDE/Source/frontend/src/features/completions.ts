import type * as Monaco from 'monaco-editor';
import type {Settings} from '../types';

export function localContinuation(line:string,language:string):string{
  if(language==='c'){
    if(/\bprin$/.test(line))return 'tf("\\n");';
    if(/\bretu$/.test(line))return 'rn 0;';
    if(line.endsWith('#include <std'))return 'io.h>';
  }
  if(language==='cpp'){
    if(/\bcou$/.test(line)||/\bcout$/.test(line))return 't << "" << std::endl;';
    if(/\bcin$/.test(line))return ' >> ;';
    if(line.endsWith('#include <io'))return 'stream>';
    if(/\bretu$/.test(line))return 'rn 0;';
  }
  if(language==='csharp'){
    if(/\bConsole\.W$/.test(line)||/\bcw$/.test(line))return 'riteLine();';
    if(/\bConsole\.R$/.test(line))return 'eadLine();';
    if(/\bpubl$/.test(line))return 'ic static void Main(string[] args) {';
  }
  if(language==='objective-c'||language==='objc'){
    if(/\bNSL$/.test(line)||/\bNSLog$/.test(line))return '(@"");';
    if(line.endsWith('#import <Found'))return 'ation/Foundation.h>';
  }
  if(language==='rust'){
    if(/\bprintl$/.test(line)||/\bprintln!$/.test(line))return 'ln!("{}");';
    if(/\bfn m$/.test(line))return 'ain() {\n    \n}';
    if(/\blet m$/.test(line))return 'ut ';
  }
  if(language==='plaintext'||language==='1c'){
    if(/\bСооб$/.test(line)||/\bСообщить$/.test(line))return 'щить("");';
    if(/\bЕсли $/.test(line))return ' Тогда\n    \nКонецЕсли;';
    if(/\bДля $/.test(line))return 'Сч = 1 По 10 Цикл\n    \nКонецЦикла;';
    if(/\bПроц$/.test(line))return 'едура Имя()\n    \nКонецПроцедуры';
    if(/\bФунк$/.test(line))return 'ция Имя()\n    Возврат ;\nКонецФункции';
    if(/\bНовый М$/.test(line))return 'ассив;';
    if(/\bНовый С$/.test(line))return 'труктура("");';
  }
  if(language==='python'){
    if(/\bprin$/.test(line))return 't()';
    if(/\bprint$/.test(line))return '()';
    if(/\bfor $/.test(line))return 'i in range(10):';
    if(/\bdef $/.test(line))return 'main():';
    if(/\.appen$/.test(line))return 'd()';
    if(/\bretu$/.test(line))return 'rn ';
    if(/\bif __name__$/.test(line))return ' == "__main__":';
  }
  if(language==='javascript'||language==='typescript'){
    if(/\bconso$/.test(line))return 'le.log();';
    if(/\bconsole\.l$/.test(line))return 'og();';
    if(/\bfunc$/.test(line))return 'tion ';
    if(/\bretu$/.test(line))return 'rn ';
  }
  if(language==='java'){
    if(/\bSystem\.out\.p$/.test(line))return 'rintln();';
    if(/\bpubl$/.test(line))return 'ic static void main(String[] args) {';
    if(/\bretu$/.test(line))return 'rn ';
  }
  if(language==='sql'){
    if(/\bSEL$/i.test(line))return 'ECT ';
    if(/\bSELECT $/i.test(line))return '* FROM ';
    if(/\bORDER $/i.test(line))return 'BY ';
    if(/\bGROUP $/i.test(line))return 'BY ';
  }
  if(language==='lua'){
    if(/\bprin$/.test(line)||/\bprint$/.test(line))return '()';
    if(/\blocal func$/.test(line))return 'tion () end';
    if(/\bfunc$/.test(line))return 'tion () end';
    if(/\bfor i ?= ?1,$/.test(line))return ' 10 do end';
    if(/\btable\.ins$/.test(line))return 'ert(tbl, val)';
    if(/\bcoroutine\.cr$/.test(line))return 'eate(function() end)';
    if(/\bsetmeta$/.test(line))return 'table(tbl, mt)';
    if(/\bretu$/.test(line))return 'rn ';
  }
  if(language==='assembly'||language==='asm'||language==='nasm'){
    if(/\bsecti$/.test(line))return 'on .text';
    if(/\bgloba$/.test(line))return 'l _start';
    if(/\bmov r$/.test(line))return 'ax, ';
    if(/\bsysc$/.test(line))return 'all';
    if(/\bmov rax, 60$/.test(line))return '\n    mov rdi, 0\n    syscall';
    if(/\b_sta$/.test(line))return 'rt:';
    if(/\bpush r$/.test(line))return 'bp';
    if(/\bpop r$/.test(line))return 'bp';
    if(/\bret$/.test(line))return '';
  }
  if(language==='html'){
    if(line.endsWith('<h1'))return '>Заголовок</h1>';
    if(line.endsWith('<p'))return '>Текст</p>';
    if(line.endsWith('<div'))return ' class="card"></div>';
  }
  if(language==='css'){
    if(/display:\s*f$/.test(line))return 'lex;';
    if(/box-sizing:\s*b$/.test(line))return 'order-box;';
  }
  return '';
}

export function registerInline(monaco:typeof Monaco,settings:()=>Settings){
  const cache=new Map<string,string>();
  const langs = ['python','sql','html','css','c','cpp','csharp','objective-c','objc','rust','1c','plaintext','javascript','typescript','java','lua','assembly','nasm','asm'];
  return monaco.languages.registerInlineCompletionsProvider(langs,{
    async provideInlineCompletions(model,position,_context,token){
      const cfg=settings();if(!cfg.inlineCompletion)return {items:[]};
      const line=model.getLineContent(position.lineNumber).slice(0,position.column-1);
      if(model.getLineContent(position.lineNumber).slice(position.column-1).trim())return {items:[]};
      let text=localContinuation(line,model.getLanguageId());
      if(!text&&cfg.aiCompletion&&cfg.aiProvider!=='disabled'&&cfg.aiModel&&line.trim().length>=3){
        const prefix=model.getValueInRange({startLineNumber:1,startColumn:1,endLineNumber:position.lineNumber,endColumn:position.column}).slice(-3500);
        const suffix=model.getValue().slice(model.getOffsetAt(position)).slice(0,1000);
        const key=cfg.aiModel+'|'+prefix+'|'+suffix;
        if(cache.has(key))text=cache.get(key)!;
        else {
          const controller=new AbortController();const cancellation=token.onCancellationRequested(()=>controller.abort());
          try{
            await new Promise<void>(resolve=>{const id=setTimeout(resolve,450);controller.signal.addEventListener('abort',()=>{clearTimeout(id);resolve();},{once:true});});
            if(token.isCancellationRequested)return {items:[]};
            const response=await fetch('/api/ai/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mode:'complete',code:prefix,suffix,language:model.getLanguageId()}),signal:controller.signal});
            if(response.ok){text=(await response.json()).text||'';if(cache.size>80)cache.clear();cache.set(key,text);}
          }catch{/* optional */}finally{cancellation.dispose();}
        }
      }
      if(!text||token.isCancellationRequested)return {items:[]};
      return {items:[{insertText:text,range:new monaco.Range(position.lineNumber,position.column,position.lineNumber,position.column)}]};
    },
    freeInlineCompletions(){},
  });
}
