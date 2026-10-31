import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'./tests',timeout:120000,expect:{timeout:15000},workers:1,fullyParallel:false,use:{baseURL:process.env.DEVFORGE_TEST_URL||'http://127.0.0.1:5174',headless:true,channel:'msedge',viewport:{width:1440,height:1000},screenshot:'only-on-failure'},reporter:'list'});
