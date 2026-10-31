import {PGlite} from '/runtimes/pglite/index.js';
let runDb,checkDb;
try{runDb=await PGlite.create();self.postMessage({type:'ready'});}
catch(error){self.postMessage({type:'boot-error',error:String(error)});}
async function reset(db,setup){
  await db.exec('ROLLBACK;');
  await db.exec('DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public; SET search_path TO public;');
  if(setup)await db.exec(setup);
}
function tables(results){return results.filter(r=>r.fields.length).map(r=>{
  if(r.rows.length>1000)throw new Error('Лимит результата: 1000 строк. Используйте LIMIT.');
  return {columns:r.fields.map(f=>f.name),values:r.rows.map(row=>row.map(v=>v instanceof Date?v.toISOString():typeof v==='bigint'?Number(v):v&&typeof v==='object'?JSON.stringify(v):v))};
});}
self.onmessage=async({data})=>{
  const results=[];let output=[];
  try{
    if(data.check){
      if(!checkDb)checkDb=await PGlite.create();
      for(const test of data.tests||[]){
        try{
          await reset(checkDb,data.setupSql);
          const returned=tables(await checkDb.exec(data.code,{rowMode:'array'}));
          let actual;
          if(test.query==='$result')actual=returned.at(-1)?.values||[];
          else if(test.query.startsWith('$reject:')){
            actual=false;
            try{await checkDb.exec(test.query.slice(8));}catch(e){actual=['23502','23503','23505','23514'].includes(e.code);}
          }else actual=tables(await checkDb.exec(test.query,{rowMode:'array'})).at(-1)?.values||[];
          results.push({id:test.id,actual,error:null});if(!output.length)output=returned;
        }catch(error){results.push({id:test.id,actual:null,error:String(error)});}
      }
    }else{
      if(data.reset)await reset(runDb,data.setupSql);
      output=tables(await runDb.exec(data.code,{rowMode:'array'}));
    }
    self.postMessage({type:'result',result:{stdout:output.length?'':'Запрос PostgreSQL выполнен.',stderr:'',tables:output,results}});
  }catch(error){self.postMessage({type:'result',result:{stdout:'',stderr:'',tables:[],results,error:String(error)}});}
};
