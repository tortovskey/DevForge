import {chromium} from '@playwright/test';
import {writeFile,mkdir} from 'node:fs/promises';
const codes={
 python:'print(5)',javascript:'console.log(5);',typescript:'const x: number=5;console.log(x);',
 java:'public class Main { public static void main(String[] args) { System.out.println(5); } }',
 c:'#include <stdio.h>\nint main(void){puts("5");return 0;}',cpp:'#include <iostream>\nint main(){std::cout<<5<<std::endl;return 0;}',
 csharp:'using System;\nclass Program{static void Main(){Console.WriteLine(5);}}',objc:'#import <Foundation/Foundation.h>\nint main(){@autoreleasepool{NSLog(@"5");}return 0;}',
 rust:'fn main(){println!("5");}', '1c':'Сообщить(5);',lua:'print(5)',sql:'SELECT 5 AS result;',postgresql:'SELECT 5 AS result;',
 assembly:'section .data\nmsg db "5",10\nsection .text\nglobal _start\n_start:\nmov rax,1\nmov rdi,1\nmov rsi,msg\nmov rdx,2\nsyscall\nmov rax,60\nxor rdi,rdi\nsyscall'
};
const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu']});
const report={};
try{
 const page=await browser.newPage();await page.goto(process.env.DEVFORGE_TEST_URL||'http://127.0.0.1:18765');
 for(const [language,code] of Object.entries(codes)){
  report[language]=await page.evaluate(({language,code})=>new Promise(resolve=>{
   const worker=new Worker(`/workers/${language}.js`,language==='postgresql'?{type:'module'}:undefined);
   const done=result=>{clearTimeout(timer);worker.terminate();resolve(result);};
   const timer=setTimeout(()=>done({error:'Worker timeout'}),45000);
   worker.onerror=e=>done({error:e.message});
   worker.onmessage=e=>{if(e.data.type==='ready')worker.postMessage({code,reset:true});else if(e.data.type==='boot-error')done({error:e.data.error});else if(e.data.type==='result')done(e.data.result);};
  }),{language,code});
  const r=report[language];console.log(language,JSON.stringify({stdout:r.stdout,error:r.error,table:r.tables?.[0]?.values}));
 }
 await mkdir('../build/qa',{recursive:true});await writeFile('../build/qa/runtimes.json',JSON.stringify(report,null,2));
 if(Object.entries(report).some(([language,r])=>r.error||(['sql','postgresql'].includes(language)?r.tables?.[0]?.values?.[0]?.[0]!==5:r.stdout?.trim()!=='5')))process.exitCode=1;
}finally{await browser.close();}
