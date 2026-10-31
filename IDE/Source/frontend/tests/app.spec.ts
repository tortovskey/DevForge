import {test,expect,type Page} from '@playwright/test';
import solutions from './solutions.json' with {type:'json'};

async function ready(page:Page){await page.request.post('/api/auth/register',{data:{username:'test_'+Date.now(),displayName:'Regression',password:'TestPassword42'}});await page.goto('/');await expect(page.getByRole('heading',{name:'Хороший день, чтобы создать что-то.'})).toBeVisible();}
async function runtime(page:Page,language:string,request:unknown,timeout=5000){
  return page.evaluate(async({language,request,timeout})=>{
    // Load the production controller through Vite; use real browser Workers and WASM.
    const {BrowserRunner}=await import(/* @vite-ignore */ '/src/runners/runner.ts');
    const runner=new BrowserRunner(language,()=>{},timeout);
    const result=await runner.run(request);runner.reset();return result;
  },{language,request,timeout});
}

test('Python output, traceback, timeout, cancellation and restart',async({page})=>{
  await ready(page);
  const result=await runtime(page,'python',{code:'def add(a,b):\n    return a+b\nprint(add(5,3))'});
  expect(result.stdout.trim()).toBe('8');
  const broken=await runtime(page,'python',{code:'print(1/0)'});
  expect(broken.error).toContain('ZeroDivisionError');
  expect(broken.error).toContain('line 1');
  const timeout=await runtime(page,'python',{code:'while True:\n    pass'},300);
  expect(timeout.error).toContain('Timeout');
  const cancelled=await page.evaluate(async()=>{
    const {BrowserRunner}=await import(/* @vite-ignore */ '/src/runners/runner.ts');
    let runner:any;
    runner=new BrowserRunner('python',(status:string)=>{if(status==='Выполнение…')setTimeout(()=>runner.stop(),100);});
    const first=await runner.run({code:'while True:\n    pass'});
    runner.reset();
    return first;
  });
  expect(cancelled.error).toContain('остановлено');
  expect((await runtime(page,'python',{code:'print(42)'})).stdout.trim()).toBe('42');
});

test('SQL persists during Run, resets, and checks on independent databases',async({page})=>{const request=page.request;
  await ready(page);const lesson=await (await request.get('/api/lessons/sql-insert')).json();
  const results=await page.evaluate(async({lesson,solution})=>{
    const {BrowserRunner}=await import(/* @vite-ignore */ '/src/runners/runner.ts');
    const runner=new BrowserRunner('sql');
    const a=await runner.run({code:solution,setupSql:lesson.setupSql});
    const b=await runner.run({code:'SELECT COUNT(*) FROM users',setupSql:lesson.setupSql});
    const c=await runner.run({code:'SELECT COUNT(*) FROM users',setupSql:lesson.setupSql,reset:true});
    const d=await runner.run({code:solution,setupSql:lesson.setupSql,check:true,tests:lesson.tests});
    const e=await runner.run({code:solution,setupSql:lesson.setupSql,check:true,tests:lesson.tests});runner.reset();
    return {a,b,c,d,e};
  },{lesson,solution:solutions['sql-insert']});
  expect(results.a.error).toBeUndefined();expect(results.b.tables[0].values).toEqual([[5]]);expect(results.c.tables[0].values).toEqual([[4]]);expect(results.d.results).toEqual(results.e.results);
});

test('UI editor Run Check XP persistence, hints, documentation and themes',async({page})=>{const request=page.request;
  await ready(page);
  const prior=await (await request.get('/api/progress')).json();
  await request.put('/api/drafts/python-functions',{data:{code:'def add(a, b):\n    pass'}});
  await page.goto('/learn/python-functions');
  await expect(page.locator('.monaco-editor')).toBeVisible();
  await page.getByRole('button',{name:'Задание',exact:true}).click();
  await page.getByRole('button',{name:'Подсказка 1 / 3'}).click();await expect(page.locator('.hint')).toHaveCount(1);
  await page.getByRole('button',{name:'Check',exact:true}).click();await expect(page.getByText('Tests passed: 0/3')).toBeVisible();
  await page.locator('.monaco-editor').click();await page.keyboard.press('Control+a');await page.keyboard.insertText('print(8)\n'+solutions['python-functions']);
  await expect(page.getByRole('button',{name:'Run',exact:true})).toBeVisible();
  await page.keyboard.press('Control+Enter');await expect(page.locator('.output-content pre')).toHaveText('8\n');
  await page.getByRole('button',{name:'Check',exact:true}).click();await expect(page.getByText('Tests passed: 3/3')).toBeVisible();await expect(page.getByRole('heading',{name:'Урок пройден'})).toBeVisible();
  await expect.poll(async()=> (await (await request.get('/api/progress')).json()).completed).toContain('python-functions');
  const after=await (await request.get('/api/progress')).json();
  expect(after.xp).toBe(prior.xp+(prior.completed.includes('python-functions')?0:60));
  await page.reload();await expect(page.locator('.monaco-editor')).toBeVisible();
  await page.getByRole('button',{name:'Check',exact:true}).click();await expect(page.getByText('Tests passed: 3/3')).toBeVisible();
  expect((await (await request.get('/api/progress')).json()).xp).toBe(after.xp);
  await page.goto('/documentation');await page.getByRole('textbox',{name:'Поиск по документации'}).fill('JOIN');await expect(page.locator('.docs-sidebar nav').getByRole('button',{name:/JOIN/}).first()).toBeVisible();
  await page.goto('/settings');await page.getByRole('button',{name:'Светлая'}).click();await expect(page.locator('html')).toHaveAttribute('data-theme','light');await page.reload();await expect(page.locator('html')).toHaveAttribute('data-theme','light');await page.getByRole('button',{name:'Тёмная'}).click();
});

test('Project file creation rename save reload delete',async({page})=>{const request=page.request;
  await ready(page);await page.goto('/projects');await page.getByRole('button',{name:'Новый проект',exact:true}).click();await page.getByLabel('Название проекта').fill('Browser test project');await page.getByRole('button',{name:'Создать проект',exact:true}).click();await expect(page.locator('.monaco-editor')).toBeVisible();
  const id=page.url().split('/').pop();
  page.once('dialog',dialog=>dialog.accept('extra.py'));await page.getByRole('button',{name:'Добавить файл'}).click();
  await page.locator('.monaco-editor').click();await page.keyboard.press('Control+a');await page.keyboard.insertText('print("saved file")');
  page.once('dialog',dialog=>dialog.accept('renamed.py'));await page.getByRole('button',{name:'Переименовать файл'}).click();
  await page.keyboard.press('Control+s');await expect.poll(async()=> (await (await request.get(`/api/projects/${id}`)).json()).files[1].name).toBe('renamed.py');
  await page.reload();await page.locator('.file-tree').getByRole('button',{name:'renamed.py'}).click();await page.getByRole('button',{name:'Run',exact:true}).click();await expect(page.locator('.output-content')).toContainText('saved file');
  page.once('dialog',dialog=>dialog.accept());await page.getByRole('button',{name:'Удалить файл',exact:true}).click();await page.getByRole('button',{name:'Сохранить код'}).click();await expect.poll(async()=> (await (await request.get(`/api/projects/${id}`)).json()).files.length).toBe(1);
  await request.delete(`/api/projects/${id}`);
});

test('Offline runtime resources and narrow layout',async({page})=>{
  const external:string[]=[];
  await page.route('**/*',route=>{const url=new URL(route.request().url());if(!['127.0.0.1','localhost'].includes(url.hostname)){external.push(url.href);return route.abort();}return route.continue();});
  await ready(page);expect((await runtime(page,'python',{code:'print("offline")'})).stdout.trim()).toBe('offline');expect((await runtime(page,'sql',{code:'SELECT 8 AS result'})).tables[0].values).toEqual([[8]]);expect(external).toEqual([]);
  await page.setViewportSize({width:390,height:844});await page.goto('/learn/python-variables');await expect(page.locator('.monaco-editor')).toBeVisible();expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBeTruthy();
});
