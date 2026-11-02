import {test,expect} from '@playwright/test';
test.use({baseURL:process.env.DEVFORGE_PRODUCTION_URL||'http://127.0.0.1:8004'});
test('local production assets, real Workers and HTML preview',async({page})=>{
 test.setTimeout(120000);const external:string[]=[];
 await page.route('**/*',route=>{const url=new URL(route.request().url());if(!['127.0.0.1','localhost'].includes(url.hostname)){external.push(url.href);return route.abort();}return route.continue();});
 expect((await page.request.get('/api/health')).ok()).toBeTruthy();
 const auth=await page.request.post('/api/auth/register',{data:{username:'portable_'+Date.now(),displayName:'Portable QA',password:'TestPassword42'}});expect(auth.status()).toBe(201);
 await page.goto('/');await expect(page.getByRole('heading',{name:'Хороший день, чтобы создать что-то.'})).toBeVisible();
 const results=await page.evaluate(async()=>{
  const output:Record<string,any>={};
  for(const language of ['python','sql','postgresql','c','javascript','typescript','java','cpp','csharp','objc','rust','1c']){
   const worker=new Worker(`/workers/${language}.js`,language==='postgresql'?{type:'module'}:undefined);
   output[language]=await new Promise((resolve,reject)=>{const t=setTimeout(()=>reject(new Error(language+' timeout')),45000);worker.onerror=e=>reject(new Error(e.message));worker.onmessage=e=>{if(e.data.type==='ready')worker.postMessage({code:language==='c'?'#include <stdio.h>\nint main(void){puts("5");return 0;}':language==='cpp'?'#include <iostream>\nint main(){std::cout<<5<<std::endl;return 0;}':language==='csharp'?'using System;\nclass Program{static void Main(){Console.WriteLine(5);}}':language==='objc'?'#import <Foundation/Foundation.h>\nint main(){@autoreleasepool{NSLog(@"5");}return 0;}':language==='rust'?'fn main(){println!("5");}':language==='1c'?'Сообщить(5);':language==='python'?'print(int(input())+3)':language==='javascript'?'console.log(5);':language==='typescript'?'const x: number = 5; console.log(x);':language==='java'?'public class Main { public static void main(String[] args) { System.out.println(5); } }':'SELECT 2+3 AS result;',stdin:'2',reset:true});else if(e.data.type==='boot-error')reject(new Error(e.data.error));else if(e.data.type==='result'){clearTimeout(t);resolve(e.data.result);}};});worker.terminate();
  }return output;
 });
 for(const [language,result] of Object.entries(results))console.log('Runtime check',language,JSON.stringify({stdout:(result as any).stdout,error:(result as any).error}));
 expect(results.python.stdout.trim()).toBe('5');expect(results.c.stdout.trim()).toBe('5');expect(results.cpp.stdout.trim()).toBe('5');expect(results.csharp.stdout.trim()).toBe('5');expect(results.objc.stdout.trim()).toBe('5');expect(results.rust.stdout.trim()).toBe('5');expect(results['1c'].stdout.trim()).toBe('5');expect(results.javascript.stdout.trim()).toBe('5');expect(results.typescript.stdout.trim()).toBe('5');expect(results.java.stdout.trim()).toBe('5');for(const lang of ['sql','postgresql'])expect(results[lang].tables[0].values).toEqual([[5]]);
 await page.goto('/learn/html-css-first');await expect(page.locator('.monaco-editor')).toBeVisible();await page.getByRole('button',{name:'Run',exact:true}).click();await expect(page.locator('iframe[title="Предпросмотр HTML и CSS"]')).toBeVisible();expect(external).toEqual([]);
});

test('inline completion is offered and accepted with Tab',async({page})=>{
 await page.request.post('/api/auth/register',{data:{username:'inline_'+Date.now(),displayName:'Inline QA',password:'TestPassword42'}});
 await page.goto('/ide');await expect(page.locator('.monaco-editor')).toBeVisible();
 const input=page.locator('.monaco-editor textarea');await input.focus();await page.keyboard.press('Control+A');await page.keyboard.type('retu',{delay:50});await page.keyboard.press('Alt+Backslash');
 await expect(page.locator('.ghost-text-decoration')).toBeVisible();await page.keyboard.press('Tab');
 await expect(page.locator('.view-lines')).toContainText('return');
});

test('portable Python waits for input and continues in the editor',async({page})=>{
 test.setTimeout(90000);
 await page.request.post('/api/auth/register',{data:{username:'live_'+Date.now(),displayName:'Live input QA',password:'TestPassword42'}});
 await page.goto('/ide');await expect(page.locator('.monaco-editor')).toBeVisible();
 expect(await page.evaluate(()=>crossOriginIsolated)).toBe(true);
 await page.locator('.monaco-editor textarea').focus();await page.keyboard.press('Control+A');
 await page.keyboard.insertText('print("Hi")\nnumber=int(input())\nprint(number+1)');
 await page.getByRole('button',{name:'Запустить',exact:true}).click();
 await expect(page.getByRole('dialog')).toBeVisible();
 // Waiting for a person must not consume the five-second execution limit.
 await page.waitForTimeout(5500);
 await page.getByLabel('Введите следующую строку').fill('41');
 await page.screenshot({path:'test-results/interactive-input.png',fullPage:true});
 await page.getByRole('button',{name:'Отправить'}).click();
 await expect(page.locator('.fusion-bottom-panel')).toContainText('42');
 await expect(page.locator('.fusion-bottom-panel')).toContainText('Hi');
 await expect(page.locator('.fusion-bottom-panel')).not.toContainText('EOFError');
});

test('portable teaching flow and example keyboard shortcut keep the exercise unchanged',async({page})=>{
 test.setTimeout(120000);
 await page.request.post('/api/auth/register',{data:{username:'guide_'+Date.now(),displayName:'Учусь с нуля',password:'TestPassword42'}});
 await page.goto('/learn/python-variable-step');
 await expect(page.getByRole('heading',{name:'Что здесь происходит'})).toBeVisible();
 await expect(page.locator('.monaco-editor')).toBeVisible();await expect(page.locator('.monaco-editor')).toContainText('coins');
 const exercise=await page.locator('.monaco-editor .view-lines').innerText();
 await page.getByRole('button',{name:'Развернуть объяснение'}).click();
 await page.screenshot({path:'test-results/teaching-intro.png',fullPage:true});
 await page.getByRole('button',{name:'К маленькому примеру',exact:true}).click();
 await page.getByLabel('Код примера — его можно менять').fill('print(12345)');
 await page.getByLabel('Код примера — его можно менять').press('Control+Enter');
 await expect(page.getByRole('region',{name:'Результат примера'})).toContainText('12345');
 await expect(page.locator('.console')).not.toContainText('12345');
 await page.getByRole('button',{name:'Вернуть исходный пример'}).click();
 await page.screenshot({path:'test-results/teaching-reading.png',fullPage:true});
 await page.getByRole('button',{name:'Я уже понял — перейти к заданию'}).click();
 await expect(page.locator('.monaco-editor')).toBeVisible();await expect(page.locator('.monaco-editor .view-lines')).toContainText('coins');
 expect(await page.locator('.monaco-editor .view-lines').innerText()).toBe(exercise);
 await expect(page.getByRole('heading',{name:'Что сделать по порядку'})).toBeVisible();
 await page.getByText('Застряли? Открыть готовое решение для сверки',{exact:true}).click();
 await expect(page.locator('.solution-details pre')).toBeVisible();
 const progress=await (await page.request.get('/api/progress')).json();expect(progress.xp).toBe(0);
 await page.goto('/learn/sql-where');await page.getByRole('button',{name:'Задание',exact:true}).click();
 await expect(page.locator('.task-support')).toContainText('Ada');
});
