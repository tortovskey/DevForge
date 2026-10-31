let SQL, db;
(async()=>{
  try {
    importScripts('/runtimes/sql/sql-wasm.js');
    SQL=await initSqlJs({locateFile:file=>'/runtimes/sql/'+file});
    self.postMessage({type:'ready'});
  } catch(e) {self.postMessage({type:'boot-error',error:String(e)});}
})();
function create(setup) {const database=new SQL.Database();database.run("PRAGMA foreign_keys=ON;");if(setup)database.run(setup);return database;}
function limitedTables(database, code) {
  // Iterate rows rather than materializing an unbounded result in JS.
  const tables=[];
  for(const statement of database.iterateStatements(code)) {
    const columns=statement.getColumnNames(),values=[];
    let count=0;
    while(statement.step()) {
      if(++count>1000) throw new Error('Лимит результата: 1000 строк. Используйте LIMIT.');
      values.push(statement.get().map(v=>v instanceof Uint8Array ? `[BLOB ${v.length} bytes]` : v));
    }
    if(columns.length) tables.push({columns,values});
  }
  return tables;
}
self.onmessage=({data})=>{
  let results=[],tables=[];
  try {
    if(data.check) {
      for(const test of data.tests||[]) {
        let isolated;
        try {
          isolated=create(data.setupSql);
          const produced=limitedTables(isolated,data.code);
          let actual;
          if(test.query==='$result') actual=produced.at(-1)?.values||[];
          else if(test.query.startsWith('$reject:')) {
            actual=false;
            // Distinguish integrity failures from missing tables or invalid SQL.
            try {isolated.run(test.query.slice(8));} catch(e) {actual=/constraint failed/i.test(String(e));}
          } else actual=limitedTables(isolated,test.query).at(-1)?.values||[];
          results.push({id:test.id,actual,error:null});
          if(!tables.length) tables=produced;
        } catch(e) {results.push({id:test.id,actual:null,error:String(e)});}
        finally {isolated?.close();}
      }
    } else {
      if(!db||data.reset) {db?.close();db=create(data.setupSql);}
      tables=limitedTables(db,data.code);
    }
    self.postMessage({type:'result',result:{stdout:tables.length?'': 'Запрос выполнен успешно.',stderr:'',tables,results}});
  } catch(e) {self.postMessage({type:'result',result:{stdout:'',stderr:'',tables:[],results,error:String(e)}});}
};
