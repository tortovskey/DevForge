import {chromium} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';
const browser=await chromium.launch({channel:'msedge',headless:true,args:['--disable-gpu']});
try{
 const page=await browser.newPage({viewport:{width:1600,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const response=await page.goto((process.env.DEVFORGE_TEST_URL||'http://127.0.0.1:18765')+'/ide');
 await page.locator('.monaco-editor').first().waitFor({timeout:45000});
 await mkdir('../build/qa',{recursive:true});
 await page.screenshot({path:'../build/qa/ide.png',fullPage:true});
 await writeFile('../build/qa/ui.json',JSON.stringify({status:response.status(),errors,title:await page.title()},null,2));
 console.log(JSON.stringify({status:response.status(),errors,title:await page.title()}));
}finally{await browser.close();}
