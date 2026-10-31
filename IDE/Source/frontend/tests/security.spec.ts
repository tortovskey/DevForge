import {test, expect} from '@playwright/test';

test.beforeEach(async ({page}) => {
  const response = await page.request.post('/api/auth/register', {data: {
    username: 'security_' + Date.now(), displayName: 'Security QA', password: 'TestPassword42'
  }});
  expect(response.status()).toBe(201);
});

test('user Worker cannot read account API, write projects or contact external hosts', async ({page}) => {
  await page.goto('/');
  const result = await page.evaluate(async () => {
    const worker = new Worker('/workers/javascript.js');
    try {
      return await new Promise<string[]>((resolve, reject) => {
        const timeout = setTimeout(() => reject(new Error('Worker policy test timeout')), 10000);
        worker.onerror = e => reject(new Error(e.message));
        worker.onmessage = event => {
          if(event.data.type === 'ready') worker.postMessage({code: `
            Promise.allSettled([
              fetch('/api/auth/me'),
              fetch('/api/projects', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Intrusion',language:'python',files:[{name:'main.py',content:''}]})}),
              fetch('https://example.invalid/collect')
            ]).then(results => self.postMessage({type:'policy-results',results:results.map(r=>r.status)}));
          `});
          if(event.data.type === 'policy-results') {clearTimeout(timeout); resolve(event.data.results);}
        };
      });
    } finally {worker.terminate();}
  });
  expect(result).toEqual(['rejected', 'rejected', 'rejected']);
  expect(await (await page.request.get('/api/projects')).json()).toEqual([]);
});

test('minimap setting survives reload and valid sync import shows its backup', async ({page}) => {
  const errors:string[]=[]; page.on('pageerror', error => errors.push(error.message));
  await page.goto('/ide');
  await expect(page.locator('.monaco-editor')).toBeVisible();
  await page.getByRole('button', {name: 'Переключить миникарту'}).click();
  await expect.poll(async () => (await (await page.request.get('/api/settings')).json()).minimap).toBe(true);
  await page.reload(); await expect(page.locator('.minimap')).toBeVisible();
  await page.goto('/settings');
  await page.getByRole('button', {name: 'Синхронизация', exact:true}).click();
  const bundle = await (await page.request.get('/api/sync/export')).json();
  await page.locator('input[type=file]').setInputFiles({name:'backup.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(bundle))});
  await expect(page.getByText('Данные готовы к переносу')).toBeVisible();
  await page.getByRole('button', {name:'Применить и синхронизировать'}).click();
  await expect(page.locator('.sync-alert.success')).toBeVisible();
  await expect(page.locator('.backups-list')).toContainText('devforge_pre_import_');
  expect(errors).toEqual([]);
});

test('malformed backup displays an error without crashing the settings page', async ({page}) => {
  await page.goto('/settings');
  await page.getByRole('button', {name:'Синхронизация',exact:true}).click();
  await page.locator('input[type=file]').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from('{"data":{},"account":{}}')});
  await expect(page.locator('.sync-alert.error')).toBeVisible();
  await expect(page.getByRole('heading', {name:'Синхронизация прогресса'})).toBeVisible();
  await expect(page.getByText('Данные готовы к переносу')).not.toBeVisible();
});
