import {test,expect} from '@playwright/test';

async function edit(page:any,code:string){const input=page.locator('.monaco-editor textarea').first();await input.focus();await page.keyboard.press('Control+A');await page.keyboard.insertText(code);}
async function account(page:any){const r=await page.request.post('/api/auth/register',{data:{username:'ide_'+Date.now(),displayName:'IDE QA',password:'TestPassword42'}});expect(r.status()).toBe(201);}

test('IDE opens with a real forge icon and no JavaScript crash',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/ide');await expect(page.locator('.monaco-editor').first()).toBeVisible();
 const icon=page.locator('img[src="/forge.svg"]').first();
 await expect.poll(()=>icon.evaluate((img:HTMLImageElement)=>img.naturalWidth)).toBeGreaterThan(0);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 expect(errors).toEqual([]);
});

test('project can be edited and saved repeatedly with current revisions',async({page})=>{
 await account(page);
 const p=await (await page.request.post('/api/projects',{data:{name:'Save regression',language:'python',files:[{name:'main.py',content:'print(1)'}]}})).json();
 await page.goto('/projects/'+p.id);await expect(page.locator('.monaco-editor')).toBeVisible();
 for(let revision=2;revision<=3;revision++){
  await edit(page,`print(${revision})`);
  await page.locator('button[title="Сохранить проект (Ctrl+S)"]').click();
  await expect.poll(async()=> (await (await page.request.get('/api/projects/'+p.id)).json()).revision).toBe(revision);
 }
 await page.reload();await expect(page.locator('.monaco-editor .view-lines')).toContainText('print(3)');
});

test('Python input opens its dialog and continues after an answer',async({page})=>{
 await page.goto('/ide');await expect(page.locator('.monaco-editor').first()).toBeVisible();
 await edit(page,'print(int(input())+1)');await page.getByRole('button',{name:'Запустить',exact:true}).click();
 await expect(page.getByRole('dialog',{name:'Программа ожидает ввод'})).toBeVisible({timeout:45000});
 await page.getByLabel('Введите следующую строку').fill('41');await page.getByRole('button',{name:'Отправить',exact:true}).click();
 await expect(page.locator('.fusion-bottom-panel')).toContainText('42');
});

test('edits made during a save survive a reload',async({page})=>{
 await account(page);
 const p=await (await page.request.post('/api/projects',{data:{name:'Concurrent edits',language:'python',files:[{name:'main.py',content:'print(1)'}]}})).json();
 await page.goto('/projects/'+p.id);await expect(page.locator('.monaco-editor')).toBeVisible();
 let release!:()=>void;const hold=new Promise<void>(resolve=>release=resolve);
 await page.route('**/api/projects/'+p.id,async route=>{if(route.request().method()==='PUT'){const response=await route.fetch();await hold;await route.fulfill({response});}else await route.continue();});
 await edit(page,'print(2)');const started=page.waitForRequest(r=>r.url().endsWith('/api/projects/'+p.id)&&r.method()==='PUT');
 await page.getByRole('button',{name:'Сохранить код',exact:true}).click();await started;await edit(page,'print(3)');release();
 await expect(page.locator('.fusion-statusbar')).toContainText('Есть новые изменения');
 page.on('dialog',dialog=>dialog.accept());await page.reload();
 await expect(page.locator('.monaco-editor .view-lines')).toContainText('print(3)');
 expect((await (await page.request.get('/api/projects/'+p.id)).json()).files[0].content).toBe('print(2)');
});

test('invalid cached files do not crash startup',async({page})=>{
 await page.goto('/ide');await expect(page.locator('.monaco-editor').first()).toBeVisible();
 await page.evaluate(async()=>{const account=await (await fetch('/api/auth/me')).json();localStorage.setItem(`scratch:${account.id}:ide_files`,JSON.stringify([{name:42,content:null}]));});
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.reload();
 await expect(page.locator('.monaco-editor').first()).toBeVisible();expect(errors).toEqual([]);
});

test('HTML project renders a sandbox preview without starting a Worker',async({page})=>{
 await account(page);
 const p=await (await page.request.post('/api/projects',{data:{name:'HTML preview',language:'html-css',files:[{name:'index.html',content:'<h1>Forge preview</h1><script>parent.__unsafe=true</script>'}]}})).json();
 await page.goto('/projects/'+p.id);await expect(page.locator('.monaco-editor')).toBeVisible();
 await page.getByRole('button',{name:'Запустить',exact:true}).click();
 await expect(page.frameLocator('iframe[title="Предпросмотр HTML и CSS"]').getByRole('heading',{name:'Forge preview'})).toBeVisible();
 expect(await page.evaluate(()=>(window as any).__unsafe)).toBeUndefined();
});

test('Python REPL evaluates expressions and retains variables',async({page})=>{
 await page.goto('/ide');await expect(page.locator('.monaco-editor').first()).toBeVisible();
 await page.getByRole('button',{name:'Python REPL',exact:true}).click();
 const input=page.getByPlaceholder('Вычислить выражение в Python...');
 await input.fill('x = 6');await input.press('Enter');
 await expect(page.locator('.fusion-bottom-panel')).toContainText('x = 6',{timeout:45000});
 await expect(page.locator('.repl-vars-half')).toContainText('6',{timeout:45000});
 await input.fill('x * 7');await input.press('Enter');
 await expect(page.locator('.fusion-bottom-panel')).toContainText('42',{timeout:45000});
});

for (const language of ['assembly','lua'] as const) {
 test(`new ${language} project creates and runs its own template instead of SQL`,async({page})=>{
  await account(page);
  const workers:string[]=[];
  page.on('worker',worker=>workers.push(worker.url()));
  await page.goto('/projects');
  await page.getByRole('button',{name:'Новый проект',exact:true}).click();
  await page.getByLabel('Название проекта').fill(`${language} template regression`);
  await page.getByLabel('Язык проекта',{exact:true}).selectOption(language);
  await page.getByRole('button',{name:'Создать проект',exact:true}).click();
  await expect(page.locator('.monaco-editor')).toBeVisible();
  const filename=language==='assembly'?'main.asm':'main.lua';
  await expect(page.locator('.fusion-tab-bar')).toContainText(filename);
  await expect(page.locator('.fusion-tab-bar')).not.toContainText('query.sql');
  await expect(page.locator('.lang-badge')).toContainText(language==='assembly'?'Assembly':'Lua');
  const project=await(await page.request.get('/api/projects/'+page.url().split('/').pop())).json();
  expect(project.language).toBe(language);
  expect(project.files[0].name).toBe(filename);
  await page.getByRole('button',{name:'Запустить',exact:true}).click();
  await expect(page.locator('.panel-output-view .output-content')).toContainText('Hello, DevForge!');
  expect(workers.some(url=>url.endsWith(`/workers/${language}.js`))).toBe(true);
 });
}

test('run file selector executes the selected file',async({page})=>{
 await account(page);
 const p=await(await page.request.post('/api/projects',{data:{name:'Run selection',language:'python',files:[{name:'main.py',content:'print("first file")'},{name:'second.py',content:'print("selected file")'}]}})).json();
 await page.goto('/projects/'+p.id);await expect(page.locator('.monaco-editor')).toBeVisible();
 await page.locator('.fusion-topbar').getByRole('combobox',{name:'Файл для запуска',exact:true}).selectOption('1');
 await expect(page.locator('.fusion-tab.active')).toContainText('second.py');
 await page.getByRole('button',{name:'Запустить',exact:true}).click();
 await expect(page.locator('.panel-output-view')).toContainText('selected file');
});
