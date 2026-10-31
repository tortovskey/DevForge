import {test,expect} from '@playwright/test';
test('all 309 teaching examples produce their documented results',async({page},info)=>{
 test.setTimeout(600000);await page.goto('/');await expect(page.locator('.app-shell,.auth-card')).toBeVisible();
 const report=await page.evaluate(async()=>{
  const {BrowserRunner}=await import(/* @vite-ignore */ '/src/runners/runner.ts');
  const {checkHtml,documentSource}=await import(/* @vite-ignore */ '/src/runners/html.ts');
  const courses=await (await fetch('/api/courses')).json();const errors:string[]=[];let count=0;
  for(const course of courses){
   const runner=course.id==='html-css'?null:new BrowserRunner(course.id);
   for(const lesson of course.lessons){
    const guide=lesson.guide;
    if(!guide||guide.steps.length<3||guide.idea.length<150||!guide.solution||!guide.experiment){errors.push(lesson.id+': incomplete guide');continue;}
    const e=guide.example;
    const output=runner?await runner.run({code:e.code,setupSql:e.setupSql,reset:true}):await checkHtml(documentSource(e.code),[{id:'example',dom:e.dom,expected:e.expected}]);
    const actual=e.kind==='stdout'?output.stdout.trim():e.kind==='table'?output.tables.at(-1)?.values:output.results[0]?.actual;
    const expected=e.kind==='stdout'?e.expected.trim():e.expected;
    if(output.error||output.results.some((r:any)=>r.error)||JSON.stringify(actual)!==JSON.stringify(expected))errors.push(lesson.id+': '+JSON.stringify({actual,expected,error:output.error,results:output.results}));
    count++;
   }runner?.reset();
  }return {count,errors};
 });
 await info.attach('teaching-examples.json',{body:JSON.stringify(report,null,2),contentType:'application/json'});console.log(JSON.stringify(report));
 expect(report.count).toBe(309);expect(report.errors).toEqual([]);
});

test('guided lesson explains, runs an isolated editable example and leads to practice',async({page})=>{
 test.setTimeout(150000);
 await page.request.post('/api/auth/register',{data:{username:'teaching_'+Date.now(),displayName:'Новый ученик',password:'TestPassword42'}});
 for(const [id,needle] of [['python-first-print','Я учусь'],['sql-first-values','7'],['postgresql-first','Boris'],['c-first','Tea'],['html-css-first','Предпросмотр обновлён.'],['javascript-first-console','JavaScript'],['typescript-first-type','DevForge IDE v4'],['java-first-main','Java'],['cpp-first-cout','Старт C++'],['cs-first-console','Старт .NET'],['objc-first-nslog','Старт Cocoa'],['rust-first-println','Старт Rust'],['1c-first-soobschit','Старт 1С']]){
  await page.goto('/learn/'+id);await expect(page.getByRole('heading',{name:'Что здесь происходит'})).toBeVisible();
  await page.getByRole('button',{name:'К маленькому примеру',exact:true}).click();
  await expect(page.getByLabel('Код примера — его можно менять')).toBeVisible();
  await page.getByRole('button',{name:'Запустить пример',exact:true}).click();
  await expect(page.getByRole('region',{name:'Результат примера'})).toContainText(needle);
  await expect(page.locator('.teaching-output .error-text')).toHaveCount(0);
  await page.getByRole('button',{name:'К эксперименту',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Небольшой эксперимент'})).toBeVisible();
  await page.getByRole('button',{name:'Теперь самостоятельное задание',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Что сделать по порядку'})).toBeVisible();
  await page.getByText('Застряли? Открыть готовое решение для сверки',{exact:true}).click();
  await expect(page.locator('.solution-details pre')).toBeVisible();
 }
 await page.goto('/learn/python-variable-step');await expect(page.locator('.monaco-editor')).toContainText('coins');await page.getByRole('button',{name:'К маленькому примеру',exact:true}).click();
 const before=await page.locator('.monaco-editor .view-lines').innerText();
 await page.getByLabel('Код примера — его можно менять').fill('print(12345)');await page.getByRole('button',{name:'Запустить пример',exact:true}).click();
 await expect(page.getByRole('region',{name:'Результат примера'})).toContainText('12345');
 expect(await page.locator('.monaco-editor .view-lines').innerText()).toBe(before);
 const progress=await (await page.request.get('/api/progress')).json();expect(progress.xp).toBe(0);
 await page.getByRole('button',{name:'Вернуть исходный пример'}).click();
 await page.screenshot({path:'test-results/teaching-example.png',fullPage:true});
 await page.getByRole('button',{name:'Развернуть объяснение'}).click();
 await expect(page.locator('.workspace')).toHaveClass(/reading-mode/);
 await page.screenshot({path:'test-results/teaching-reading.png',fullPage:true});
 await page.getByRole('button',{name:'Я уже понял — перейти к заданию'}).click();await expect(page.locator('.monaco-editor')).toBeVisible();
 await page.setViewportSize({width:700,height:900});await page.getByRole('button',{name:'Теория',exact:true}).click();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
});
