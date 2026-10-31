import {test,expect} from '@playwright/test';
import solutions from './solutions.json' with {type:'json'};
test.use({baseURL:'http://127.0.0.1:5174'});
test('222 reference solutions, negative cases, offline runtimes and warm latency',async({page},info)=>{
 test.setTimeout(600000);
 await page.goto('/');await expect(page.locator('.app-shell,.auth-card')).toBeVisible();
 const result=await page.evaluate(async(solutions)=>{
  const {getRunner,clearRunners}=await import(/* @vite-ignore */ '/src/runners/runner.ts');
  const {checkHtml,documentSource}=await import(/* @vite-ignore */ '/src/runners/html.ts');
  const courses=await (await fetch('/api/courses')).json();const errors:string[]=[];let count=0;
  for(const lesson of courses.flatMap((c:any)=>c.lessons)){
   const run=async(code:string)=>lesson.language==='html-css'?checkHtml(documentSource(code),lesson.tests):getRunner(lesson.language).run({code,stdin:lesson.stdin,tests:lesson.tests,setupSql:lesson.setupSql,check:true,context:lesson.id});
   const good=await run(solutions[lesson.id as keyof typeof solutions]);
   if(good.error)errors.push(lesson.id+': '+good.error);
   for(const t of lesson.tests){const actual=good.results.find((r:any)=>r.id===t.id);if(!actual||actual.error||JSON.stringify(actual.actual)!==JSON.stringify(t.expected))errors.push(lesson.id+': '+t.id+' '+JSON.stringify(actual)+' expected '+JSON.stringify(t.expected));}
   const bad=await run(lesson.language==='c'?'int main(void){return 0;}':lesson.language==='python'?'pass':lesson.language==='html-css'?'<p>wrong</p>':lesson.language==='java'?'public class Main { public static void main(String[] args) {} }':lesson.language==='javascript'||lesson.language==='typescript'?'console.log(98765);':'SELECT 98765;');
   if(!bad.error&&!bad.results.some((r:any)=>r.error||JSON.stringify(r.actual)!==JSON.stringify(lesson.tests.find((t:any)=>t.id===r.id).expected)))errors.push(lesson.id+': incorrect code passed');
   count++;
  }
  const timings:Record<string,number[]>={};
  for(const lang of ['python','sql','postgresql']){timings[lang]=[];for(let i=0;i<10;i++){const r=await getRunner(lang).run({code:lang==='python'?'print(1+1)':'SELECT 1+1;',context:'benchmark'});if(r.error)errors.push(lang+': '+r.error);timings[lang].push(r.duration);}}
  clearRunners();return {count,errors,timings};
 },solutions);
 await info.attach('runtimes.json',{body:JSON.stringify(result,null,2),contentType:'application/json'});
 console.log(JSON.stringify(result));expect(result.count).toBe(222);expect(result.errors).toEqual([]);
});

test('registration, placement, account isolation, HTML preview and completion',async({page},info)=>{
 test.setTimeout(150000);await page.goto('/');await expect(page.locator('.auth-card')).toBeVisible();page.on('dialog',dialog=>dialog.accept());
 const username='ui_'+Date.now();
 if(await page.getByRole('button',{name:'Создать новый локальный аккаунт'}).isVisible())await page.getByRole('button',{name:'Создать новый локальный аккаунт'}).click();
 await page.getByLabel('Ваше имя',{exact:true}).fill('Тестовый ученик');await page.getByLabel('Логин',{exact:true}).fill(username);await page.getByLabel('Пароль',{exact:true}).fill('DevForge2026');await page.getByRole('button',{name:'Создать аккаунт',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Начните со своей точки.'})).toBeVisible();
 await page.getByRole('button',{name:'Узнать свой уровень'}).click();
 for(const input of await page.getByLabel('Пока не знаю',{exact:true}).all())await input.check();
 await page.getByRole('button',{name:'Получить индивидуальный план'}).click();await expect(page.getByRole('heading',{name:'Предварительный уровень: С нуля'})).toBeVisible();
 await page.screenshot({path:'test-results/assessment.png',fullPage:true});
 await page.goto('/learn/python-first-print');await expect(page.locator('.monaco-editor')).toBeVisible();
 const input=page.locator('.monaco-editor textarea');await input.focus();await page.keyboard.press('Control+A');await page.keyboard.type('prin');await page.keyboard.press('Escape');await page.waitForTimeout(700);await page.keyboard.press('Alt+Backslash');await page.waitForTimeout(700);
 // Explicit action triggers provider independently of suggestion-widget precedence.
 const continuation=await page.evaluate(async()=>{const {localContinuation}=await import(/* @vite-ignore */ '/src/features/completions.ts');return localContinuation('prin','python');});expect(continuation).toBe('t()');
 await input.focus();await page.keyboard.press('Control+A');await page.keyboard.insertText('print("Привет, мир!")');await page.getByRole('button',{name:'Check',exact:true}).click();await expect(page.locator('.console')).toContainText('мс');
 await page.goto('/learn/html-css-first');await expect(page.locator('.monaco-editor')).toBeVisible();await page.locator('.monaco-editor textarea').focus();await page.keyboard.press('Control+A');await page.keyboard.insertText(solutions['html-css-first']);await page.getByRole('button',{name:'Check',exact:true}).click();await expect(page.frameLocator('iframe[title="Предпросмотр HTML и CSS"]').locator('h1')).toBeVisible();
 await page.screenshot({path:'test-results/html-workspace.png',fullPage:true});
 await page.getByRole('button',{name:'Выйти из аккаунта'}).click();await expect(page.getByRole('button',{name:'Войти',exact:true})).toBeVisible();
 await page.getByLabel('Логин',{exact:true}).fill(username);await page.getByLabel('Пароль',{exact:true}).fill('DevForge2026');await page.getByRole('button',{name:'Войти',exact:true}).click();await expect(page.getByRole('heading',{name:'Хороший день, чтобы создать что-то.'})).toBeVisible();
 await page.screenshot({path:'test-results/dashboard.png',fullPage:true});
});

