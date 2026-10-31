import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import ts from 'typescript';
const source=await readFile(new URL('../src/services/platform.ts',import.meta.url),'utf8');
const compiled=ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.ESNext,target:ts.ScriptTarget.ES2022}}).outputText;
const {validateSyncBundle,readSyncFile}=await import('data:text/javascript;base64,'+Buffer.from(compiled).toString('base64'));
const bundle=version=>({format:'devforge-sync',version,checksum:'a'.repeat(64),account:{username:'test'},data:{completions:[],projects:[],attempts:[],drafts:[],settings:{}}});
test('sync accepts release 1.0 and legacy 0.4/0.5 backups',()=>{
  for(const version of ['0.4.0','0.5.0','0.5.12','1.0.0','1.0.12'])assert.equal(validateSyncBundle(bundle(version)).version,version);
  for(const version of ['1.1.0','0.50.0','2.0.0','1.0.0\n',undefined])assert.throws(()=>validateSyncBundle(bundle(version)));
});
test('sync rejects malformed and oversized files before a preview',async()=>{
  for(const value of [null,{},[],{...bundle('1.0.0'),checksum:'invalid'},{...bundle('1.0.0'),data:{}}])assert.throws(()=>validateSyncBundle(value));
  await assert.rejects(readSyncFile({size:6500001,text:()=>{throw new Error('must not read');}}),/слишком большой/);
  await assert.rejects(readSyncFile({size:10,text:async()=>'{broken'}));
});
