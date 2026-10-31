import {test,expect,type Page} from '@playwright/test';
import {mkdir} from 'node:fs/promises';
import {resolve} from 'node:path';

async function prefs(page:Page){return (await page.request.get('/api/settings')).json();}
async function open(page:Page){await page.goto('/ide');await expect(page.locator('.monaco-editor').first()).toBeVisible();await page.getByRole('button',{name:'Настроить IDE',exact:true}).click();return page.getByRole('dialog');}
async function apply(page:Page){await page.getByRole('button',{name:'Применить',exact:true}).click();await expect(page.getByText('Настройки применены и сохранены.',{exact:true})).toBeVisible();}
test.beforeEach(async({page})=>{
  const r=await page.request.post('/api/auth/register',{data:{username:'workbench_'+Date.now(),displayName:'Workbench QA',password:'TestPassword42'}});expect(r.status()).toBe(201);
});

test('themes and Monaco preferences persist and really affect the editor',async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  const dialog=await open(page);
  await expect(dialog.locator('.ide-theme-grid>button')).toHaveCount(6);
  await dialog.getByRole('button',{name:'Тема Paper Light',exact:true}).click();
  await dialog.getByRole('button',{name:'Редактор',exact:true}).click();
  await dialog.getByRole('spinbutton',{name:'Размер шрифта',exact:true}).fill('18');
  await dialog.getByText('Ширина табуляции',{exact:true}).locator('..').locator('..').getByRole('combobox').selectOption('2');
  await dialog.getByText('Номера строк',{exact:true}).locator('..').locator('..').getByRole('combobox').selectOption('relative');
  await apply(page);await page.getByRole('button',{name:'Закрыть настройки IDE'}).click();
  await expect(page.locator('.ide-workbench')).toHaveAttribute('data-theme','light');
  await expect(page.locator('.monaco-editor').first()).toHaveCSS('background-color','rgb(255, 255, 255)');
  await expect(page.locator('.view-lines').first()).toHaveCSS('font-size','18px');
  expect((await prefs(page)).ide.tabSize).toBe(2);
  await page.reload();await expect(page.locator('.monaco-editor').first()).toBeVisible();
  await expect(page.locator('.ide-workbench')).toHaveAttribute('data-theme','light');
  expect(errors).toEqual([]);
});

test('docking, sash resizing and focus mode preserve and restore the workspace',async({page})=>{
  const d=await open(page);await d.getByRole('button',{name:'Рабочее место',exact:true}).click();
  await d.getByText('Боковая панель',{exact:true}).locator('..').locator('..').getByRole('combobox').selectOption('right');
  await d.getByText('Панель инструментов',{exact:true}).locator('..').locator('..').getByRole('combobox').selectOption('right');
  await apply(page);await page.getByRole('button',{name:'Закрыть настройки IDE'}).click();
  const sidebar=page.locator('.fusion-sidebar-window'),editor=page.locator('.fusion-monaco-shell');
  const a=await sidebar.boundingBox(),b=await editor.boundingBox();expect(a!.x).toBeGreaterThan(b!.x);
  const sash=page.getByRole('separator',{name:'Изменить ширину боковой панели'}),pos=await sash.boundingBox();
  await page.mouse.move(pos!.x+2,pos!.y+80);await page.mouse.down();await page.mouse.move(pos!.x-48,pos!.y+80,{steps:8});await page.mouse.up();
  await expect.poll(async()=>(await prefs(page)).ide.sidebarWidth).toBe(298);
  await sash.focus();await page.keyboard.press('ArrowLeft');
  await expect.poll(async()=>(await prefs(page)).ide.sidebarWidth).toBe(308);
  await page.getByRole('button',{name:'Режим фокуса',exact:true}).click();await expect(sidebar).not.toBeVisible();await expect(page.locator('.fusion-bottom-panel')).not.toBeVisible();
  await page.getByRole('button',{name:'Вернуть панели',exact:true}).click();await expect(sidebar).toBeVisible();await expect(page.locator('.fusion-bottom-panel')).toBeVisible();
  await page.reload();await expect(sidebar).toHaveCSS('width','308px');
});

test('profiles export, validate on import and reject damaged files without mutation',async({page})=>{
  const d=await open(page);await d.getByRole('button',{name:'Тема Nord',exact:true}).click();
  await d.getByRole('button',{name:'Профили',exact:true}).click();await d.getByRole('textbox',{name:'Имя профиля'}).fill('Night work');await d.getByRole('button',{name:'Сохранить текущий'}).click();
  await apply(page);expect((await prefs(page)).ideProfiles[0].name).toBe('Night work');
  const before=await prefs(page);
  await d.locator('input[type=file]').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from('{"version":999}')});
  await expect(d.getByRole('alert')).toContainText('не прошёл проверку');expect(await prefs(page)).toEqual(before);
  const downloadPromise=page.waitForEvent('download');await d.getByRole('button',{name:'Экспорт текущего'}).click();
  const file=await downloadPromise;expect(file.suggestedFilename()).toBe('devforge-profile.json');
  const stream=await file.createReadStream(),chunks:Buffer[]=[];for await(const c of stream!)chunks.push(c as Buffer);
  const data=JSON.parse(Buffer.concat(chunks).toString());data.profile.preferences.ide.theme='paper';data.profile.preferences.theme='light';
  await d.locator('input[type=file]').setInputFiles({name:'valid.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(data))});
  await expect(d.getByText('Профиль проверен и загружен.',{exact:false})).toBeVisible();await apply(page);
  expect((await prefs(page)).ide.theme).toBe('paper');
});

test('custom keybindings, conflict feedback and keyboard command palette work',async({page})=>{
  const d=await open(page);await d.getByRole('button',{name:'Клавиши',exact:true}).click();
  const key=d.getByRole('textbox',{name:'Клавиши: Переключить боковую панель'});await key.focus();await page.keyboard.press('Control+S');
  await expect(d.getByRole('alert')).toContainText('Ctrl+S');await expect(d.getByRole('button',{name:'Применить',exact:true})).toBeDisabled();
  await key.focus();await page.keyboard.press('Control+Alt+B');await apply(page);await page.getByRole('button',{name:'Закрыть настройки IDE'}).click();
  await page.keyboard.press('Control+Alt+B');await expect(page.locator('.fusion-sidebar-window')).not.toBeVisible();
  await page.keyboard.press('Control+Alt+B');await expect(page.locator('.fusion-sidebar-window')).toBeVisible();
  await page.keyboard.press('F1');const search=page.getByRole('combobox',{name:'Поиск команд и файлов'});await search.fill('Настроить IDE');await search.press('Enter');await expect(d).toBeVisible();
});

test('closing a tab never deletes its file or contents',async({page})=>{
  const files=[{name:'main.py',content:'print(42)'},{name:'notes.txt',content:'keep this data'}];
  const p=await(await page.request.post('/api/projects',{data:{name:'Tab safety',language:'python',files}})).json();
  await page.goto('/projects/'+p.id);await expect(page.locator('.monaco-editor')).toBeVisible();
  await page.getByRole('button',{name:'Закрыть вкладку notes.txt',exact:true}).click();
  await expect(page.locator('.fusion-tab-bar')).not.toContainText('notes.txt');
  await page.getByRole('button',{name:'Сохранить код',exact:true}).click();
  await expect.poll(async()=>(await(await page.request.get('/api/projects/'+p.id)).json()).revision).toBe(2);
  expect((await(await page.request.get('/api/projects/'+p.id)).json()).files).toEqual(files);
  await page.locator('.file-tree-list').getByText('notes.txt',{exact:true}).click();await expect(page.locator('.fusion-tab-bar')).toContainText('notes.txt');
});

test('edited JSON is validated on Apply and failed saves can be retried',async({page})=>{
  const d=await open(page);await d.getByRole('button',{name:'JSON',exact:true}).click();
  const text=d.getByRole('textbox',{name:'JSON профиля IDE'});const value=JSON.parse(await text.inputValue());value.profile.preferences.ide.accent='#ad99ff';await text.fill(JSON.stringify(value));await apply(page);expect((await prefs(page)).ide.accent).toBe('#ad99ff');
  await text.fill('{"not":"a profile"}');await d.getByRole('button',{name:'Применить',exact:true}).click();await expect(d.getByRole('alert')).toBeVisible();expect((await prefs(page)).ide.accent).toBe('#ad99ff');
  await d.getByRole('button',{name:'Оформление',exact:true}).click();await d.getByRole('button',{name:'Тема Graphite'}).click();
  await page.route('**/api/settings',async route=>route.request().method()==='PUT'?route.fulfill({status:503,body:'{"detail":"Test unavailable"}',contentType:'application/json'}):route.continue());
  await d.getByRole('button',{name:'Применить',exact:true}).click();await expect(d.getByRole('alert')).toContainText('Не удалось сохранить');await page.unroute('**/api/settings');await apply(page);expect((await prefs(page)).ide.theme).toBe('graphite');
});

test('workbench and preferences remain usable at smaller window sizes',async({page})=>{
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await open(page);await mkdir(resolve('../build/qa'),{recursive:true});
  await page.screenshot({path:resolve('../build/qa/workbench-preferences.png')});
  for(const width of [1000,760]){await page.setViewportSize({width,height:800});expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);await expect(page.getByRole('button',{name:'Применить',exact:true})).toBeInViewport();}
  await page.getByRole('button',{name:'Закрыть настройки IDE'}).click();await page.setViewportSize({width:1440,height:1000});await page.screenshot({path:resolve('../build/qa/workbench-dark.png')});expect(errors).toEqual([]);
});

test('JetBrains keymap opens settings, terminal and runs Python with Shift F10',async({page})=>{
  const d=await open(page);await d.getByRole('button',{name:'Клавиши',exact:true}).click();
  await d.getByText('Схема клавиш',{exact:true}).locator('..').locator('..').getByRole('combobox').selectOption('jetbrains');
  await apply(page);await page.getByRole('button',{name:'Закрыть настройки IDE'}).click();
  await page.keyboard.press('Control+Alt+S');await expect(d).toBeVisible();await page.keyboard.press('Escape');await expect(d).not.toBeVisible();
  await page.keyboard.press('Alt+F12');await expect(page.locator('.terminal-input-row input')).toBeVisible();
  const editor=page.locator('.monaco-editor textarea').first();await editor.focus();await page.keyboard.press('Control+A');await page.keyboard.insertText('print(6 * 7)');
  await page.keyboard.press('Shift+F10');await expect(page.locator('.fusion-bottom-panel')).toContainText('42',{timeout:60000});
  await page.keyboard.press('Shift');await page.keyboard.press('Shift');await expect(page.getByRole('combobox',{name:'Поиск команд и файлов'})).toBeVisible();
});
