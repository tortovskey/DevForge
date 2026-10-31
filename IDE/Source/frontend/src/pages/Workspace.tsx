import DevForgeIDE from '../components/DevForgeIDE';
import {lazy,Suspense,useEffect,useRef,useState} from 'react';
import {Link,useNavigate,useParams} from 'react-router-dom';
import {Play,Square,RotateCcw,Check,Save,FileCode2,Plus,ChevronRight,Lightbulb,BookOpen,Terminal,Trash2,Pencil,ArrowRight,Code2,Map} from 'lucide-react';
const CodeEditor=lazy(()=>import('../components/CodeEditor'));
import Output,{same} from '../components/Output';
import LessonGuide,{LessonTaskSupport,LessonSolution} from '../components/LessonGuide';
import {BrowserRunner,getRunner} from '../runners/runner';
import {checkHtml,documentSource} from '../runners/html';
import AIHelp from '../components/AIHelp';
import {LANGUAGE_NAMES,EXTENSIONS} from '../types';
import {api} from '../services/api';
import {useStore} from '../services/store';
import {localTutor} from '../services/tutor';
import type {Lesson,Project,RunResult} from '../types';

export default function Workspace(){
  const {lessonId,projectId}=useParams();const {courses}=useStore();
  const lesson=courses.flatMap(c=>c.lessons).find(l=>l.id===lessonId);
  if(lessonId&&!lesson)return <div className="page"><h1>Урок не найден</h1><Link to="/learn">К курсам</Link></div>;
  if(!lesson) {
    return <DevForgeIDE key={projectId||'scratch'} projectId={projectId}/>;
  }
  return <WorkspaceInner key={lessonId} lesson={lesson} projectId={projectId}/>;
}
function WorkspaceInner({lesson,projectId}:{lesson?:Lesson;projectId?:string}) {
  const {settings,updateSettings,notify,refresh,courses,progress,account}=useStore();const navigate=useNavigate();
  const [project,setProject]=useState<Project|null>(null),[active,setActive]=useState(0),[code,setCode]=useState('');
  const [loading,setLoading]=useState(true),[loadError,setLoadError]=useState(''),[dirty,setDirty]=useState(false),[saveState,setSaveState]=useState('Сохранено');
  const [result,setResult]=useState<RunResult|null>(null),[busy,setBusy]=useState(false),[status,setStatus]=useState('Готово');
  const [stdin,setStdin]=useState(lesson?.stdin||'');
  const [inputPrompt,setInputPrompt]=useState<string|null>(null),[inputValue,setInputValue]=useState('');
  const inputResolve=useRef<((value:string|null)=>void)|null>(null);
  const [preview,setPreview]=useState(''),[showAI,setShowAI]=useState(false);
  const [reading,setReading]=useState(false);
  const [hint,setHint]=useState(0),[tab,setTab]=useState('theory'),[explanation,setExplanation]=useState('');
  const alive=useRef(true),editVersion=useRef(0),saving=useRef(false),draftQueue=useRef(Promise.resolve());
  function persistDraft(value:string):Promise<void>{
    const task=draftQueue.current.then(()=>api<void>(`/drafts/${lesson!.id}`,'PUT',{code:value}));
    draftQueue.current=task.catch(()=>{});return task;
  }
  const language=lesson?.language||project?.language||'python';
  const runner=useRef<BrowserRunner|null>(null);
  useEffect(()=>{if(language==='html-css'){runner.current=null;setStatus('Предпросмотр готов');return;}
    runner.current=getRunner(language,setStatus);
    runner.current.onInputRequest=prompt=>new Promise(resolve=>{inputResolve.current=resolve;setInputValue('');setInputPrompt(prompt.trim().slice(-160)||'Программа ожидает строку ввода');});
    runner.current.onInputCancel=()=>{inputResolve.current?.(null);inputResolve.current=null;setInputPrompt(null);};
    void runner.current.warm().catch(e=>notify(String(e)));
    return()=>{runner.current?.stop();if(runner.current){runner.current.onStatus=()=>{};runner.current.onInputRequest=async()=>null;runner.current.onInputCancel=()=>{};}};
  },[language]);
  function answerInput(value:string|null){inputResolve.current?.(value);inputResolve.current=null;setInputPrompt(null);}
  useEffect(()=>{
    alive.current=true;
    (async()=>{
      if(lesson){
        const draft=await api<{code:string}>(`/drafts/${lesson.id}`);
        if(!alive.current)return;
        const backup=localStorage.getItem(`draft:${account.id}:${lesson.id}`);
        setCode(backup??draft.code);setDirty(backup!==null&&backup!==draft.code);
        updateSettings({lastLesson:lesson.id}).catch(e=>notify(String(e)));
      } else if(projectId){
        const saved=await api<Project>(`/projects/${projectId}`);
        if(!alive.current)return;
        const raw=localStorage.getItem(`project:${account.id}:${projectId}`);
        let cached:Project|null=null;
        try{cached=raw?JSON.parse(raw):null;}catch{localStorage.removeItem(`project:${account.id}:${projectId}`);}
        if(cached&&cached.revision===saved.revision){setProject(cached);setDirty(true);setSaveState('Восстановлен черновик');}
        else {setProject(saved);if(cached)notify('На сервере новая версия. Старый черновик сохранён в браузере, но не применён.');}
      } else {setCode(localStorage.getItem(`scratch:${account.id}:python`)||'def add(a, b):\n    return a + b\n\nprint(add(5, 3))');}
      if(alive.current)setLoading(false);
    })().catch(e=>{if(alive.current){setLoadError(String(e));setLoading(false);}});
    return()=>{alive.current=false;};
  },[]);
  useEffect(()=>{
    if(loading||!lesson||!dirty)return;
    const value=code,version=editVersion.current;setSaveState('Сохранение…');
    const timer=setTimeout(()=>persistDraft(value).then(()=>{if(alive.current&&editVersion.current===version){setDirty(false);setSaveState('Сохранено');localStorage.removeItem(`draft:${account.id}:${lesson.id}`);}}).catch(e=>{if(alive.current){setSaveState('Черновик в браузере');notify(String(e));}}),800);
    return()=>clearTimeout(timer);
  },[code,dirty,loading]);
  useEffect(()=>{const handler=(e:BeforeUnloadEvent)=>{if(dirty){e.preventDefault();e.returnValue='';}};window.addEventListener('beforeunload',handler);return()=>window.removeEventListener('beforeunload',handler);},[dirty]);
  const currentCode=project?project.files[active]?.content||'':code;
  const currentName=project?.files[active]?.name||(
    language==='html-css'?'index.html':
    language==='python'?'main.py':
    language==='c'?'main.c':
    language==='cpp'?'main.cpp':
    language==='csharp'?'Program.cs':
    language==='objc'?'main.m':
    language==='rust'?'main.rs':
    language==='1c'?'Module.bsl':
    language==='javascript'?'index.js':
    language==='typescript'?'index.ts':
    language==='java'?'Main.java':language==='lua'?'main.lua':language==='assembly'?'main.asm':'query.sql');
  function updateProject(next:Project){editVersion.current++;setProject(next);setDirty(true);setSaveState('Не сохранено');localStorage.setItem(`project:${account.id}:${next.id}`,JSON.stringify(next));}
  function changeCode(value:string){
    if(project)updateProject({...project,files:project.files.map((f,i)=>i===active?{...f,content:value}:f)});
    else {editVersion.current++;setCode(value);setDirty(true);localStorage.setItem(lesson?`draft:${account.id}:${lesson.id}`:`scratch:${account.id}:python`,value);if(!lesson)setSaveState('Черновик в браузере');}
  }
  async function save(){
    if(saving.current)return;
    saving.current=true;
    try{
      if(project){const version=editVersion.current;setSaveState('Сохранение…');const {id,updated_at,...body}=project;const saved=await api<Project>(`/projects/${id}`,'PUT',body);if(version===editVersion.current){setProject(saved);setDirty(false);localStorage.removeItem(`project:${account.id}:${id}`);setSaveState('Сохранено');}else{setProject(current=>{if(!current)return current;const next={...current,revision:saved.revision};localStorage.setItem(`project:${account.id}:${id}`,JSON.stringify(next));return next;});setSaveState('Есть новые изменения');}await refresh();}
      else if(lesson){const version=editVersion.current;await persistDraft(code);if(alive.current&&version===editVersion.current){setDirty(false);setSaveState('Сохранено');localStorage.removeItem(`draft:${account.id}:${lesson.id}`);}}
      else {localStorage.setItem(`scratch:${account.id}:python`,code);setDirty(false);setSaveState('Сохранено в браузере');}
      notify('Код сохранён');
    }catch(e){notify(String(e));setSaveState('Ошибка сохранения');}finally{saving.current=false;}
  }
  async function run(check=false){
    if(busy||(!runner.current&&language!=='html-css'))return;
    setBusy(true);setExplanation('');setResult(null);
    try{
      let response:RunResult;
      if(language==='html-css'){const source=documentSource(currentCode,project?.files,currentName);setPreview(source);response=await checkHtml(source,check?lesson?.tests||[]:[]);}
      else response=await runner.current!.run({code:currentCode,stdin,files:project?.files,filename:currentName,setupSql:lesson?.setupSql,tests:check?lesson?.tests:undefined,check,context:lesson?.id||projectId||'scratch'});
      if(!alive.current)return;
      setResult(response);
      if(check&&lesson){
        const results=response.results.length?response.results:lesson.tests.map(t=>({id:t.id,actual:null,error:response.error||'Выполнение прервано'}));
        await api('/progress/attempts','POST',{id:crypto.randomUUID(),lesson_id:lesson.id,results});
        await refresh();
      }
    }catch(e){notify(`Результат не сохранён: ${String(e)}`);}
    finally{if(alive.current)setBusy(false);}
  }
  const actions=useRef({run,save});actions.current={run,save};
  useEffect(()=>{const handler=(e:KeyboardEvent)=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){if((e.target as HTMLElement)?.closest?.('.teaching-guide'))return;e.preventDefault();e.stopPropagation();void actions.current.run();}if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();e.stopPropagation();void actions.current.save();}};window.addEventListener('keydown',handler,true);return()=>window.removeEventListener('keydown',handler,true);},[]);
  function reset(){if(!confirm(lesson?'Восстановить стартовый код и сбросить среду?':'Сбросить среду выполнения? Код останется в редакторе.'))return;runner.current?.reset();setResult(null);setPreview('');if(lesson)changeCode(lesson.starterCode);notify('Среда сброшена');}
  function newFile(){if(!project)return;const name=prompt('Имя файла',language==='html-css'?'style.css':language==='python'?'new_file.py':language==='c'?'helper.c':language==='cpp'?'helper.cpp':language==='csharp'?'Helper.cs':language==='objc'?'Helper.m':language==='rust'?'helper.rs':language==='1c'?'Helper.bsl':language==='javascript'?'helper.js':language==='typescript'?'helper.ts':language==='java'?'Helper.java':language==='lua'?'helper.lua':language==='assembly'?'helper.asm':'query.sql');if(!name)return;if(!/^[\w-][\w. -]*\.(py|sql|html|css|c|h|cpp|hpp|cc|cxx|cs|m|rs|bsl|js|ts|java|lua|asm|s|inc)$/u.test(name)||name.includes('..')||!(language==='html-css'?/\.(html|css)$/.test(name):language==='c'?/\.(c|h)$/.test(name):name.endsWith(EXTENSIONS[language]))||project.files.some(f=>f.name.toLowerCase()===name.toLowerCase())){notify('Введите уникальное имя файла с расширением языка проекта, без папок.');return;}updateProject({...project,files:[...project.files,{name,content:''}]});setActive(project.files.length);}
  function renameFile(){if(!project)return;const name=prompt('Новое имя',currentName);if(!name||name===currentName)return;if(!/^[\w-][\w. -]*\.(py|sql|html|css|c|h|cpp|hpp|cc|cxx|cs|m|rs|bsl|js|ts|java|lua|asm|s|inc)$/u.test(name)||name.includes('..')||!(language==='html-css'?/\.(html|css)$/.test(name):language==='c'?/\.(c|h)$/.test(name):name.endsWith(EXTENSIONS[language]))||project.files.some(f=>f.name.toLowerCase()===name.toLowerCase())){notify('Некорректное или занятое имя файла.');return;}updateProject({...project,files:project.files.map((f,i)=>i===active?{...f,name}:f)});}
  function deleteFile(){if(!project)return;if(project.files.length===1){notify('В проекте должен остаться хотя бы один файл.');return;}if(confirm(`Удалить ${currentName}?`)){updateProject({...project,files:project.files.filter((_,i)=>i!==active)});setActive(0);}}
  if(loading)return <div className="page muted">Открываем рабочее пространство…</div>;
  if(loadError)return <div className="page"><h1>Не удалось открыть файл</h1><p className="error-text">{loadError}</p><Link to="/projects">Вернуться к проектам</Link></div>;
  const successful=!!result?.results.length&&result.results.every(r=>!r.error&&same(r.actual,lesson?.tests.find(t=>t.id===r.id)?.expected));
  const next=lesson?courses.find(c=>c.id===language)?.lessons.find(l=>l.order===lesson.order+1):undefined;
  return <div className={`workspace${reading?' reading-mode':''}`}>
    {inputPrompt!==null&&<div className="input-overlay" role="dialog" aria-modal="true" aria-label="Программа ожидает ввод"><form className="input-dialog" onSubmit={e=>{e.preventDefault();answerInput(inputValue);}}><h2>Программа ожидает ввод</h2><p>{inputPrompt}</p><label htmlFor="live-program-input">Введите следующую строку</label><input id="live-program-input" aria-label="Введите следующую строку" autoFocus maxLength={1000} value={inputValue} onChange={e=>setInputValue(e.target.value)}/><small>Enter отправляет строку, даже пустую. Каждому input() можно ответить отдельно.</small><div><button type="button" onClick={()=>runner.current?.stop()}>Остановить программу</button><button type="button" onClick={()=>answerInput(null)}>Конец ввода</button><button className="primary" type="submit">Отправить</button></div></form></div>}
    <div className="workspace-heading"><div className="breadcrumb"><Link to={lesson?'/learn':'/projects'}>{lesson?'Обучение':'Лаборатория'}</Link><ChevronRight size={14}/><span>{lesson?.title||project?.name||'Playground'}</span></div><span className="pill">{lesson?'Learning mode':'Developer mode'}</span></div>
    <div className="workspace-body">
      {lesson&&<aside className="lesson-panel"><div className="lesson-topline"><span className="eyebrow">{LANGUAGE_NAMES[language].toUpperCase()}</span><span className="muted">{String(lesson.order).padStart(2,'0')} / {courses.find(c=>c.id===language)?.lessons.length}</span></div><h2>{lesson.title}</h2><button className="reading-toggle" onClick={()=>setReading(!reading)}>{reading?'Показать редактор рядом':'Развернуть объяснение'}</button><div className="lesson-meta"><span>{lesson.level}</span><span>{lesson.minutes} мин</span><span className="xp">+{lesson.xp} XP</span></div><div className="tabs"><button className={tab==='theory'?'selected':''} onClick={()=>setTab('theory')}><BookOpen size={14}/>Теория</button><button className={tab==='task'?'selected':''} onClick={()=>{setTab('task');setReading(false);}}><Code2 size={14}/>Задание</button></div>
      {tab==='theory'?<LessonGuide lesson={lesson} previous={courses.find(c=>c.id===language)?.lessons.find(l=>l.order===lesson.order-1)} onPractice={()=>{setTab('task');setReading(false);}}/>:<div className="prose"><h3>Ваша задача</h3><p>{lesson.task}</p><LessonTaskSupport lesson={lesson}/><div className="note">{lesson.language==='html-css'?'Проверяем элементы и вычисленные стили страницы.':['sql','postgresql'].includes(lesson.language)?'Каждая проверка начинается с исходных данных.':'Тесты выполняют ваш код и проверяют реальные значения.'}</div><h3>Что проверяем</h3>{lesson.tests.map(t=><div className="check-item" key={t.id}><Check size={14}/>{t.label}</div>)}<button className="hint-button" disabled={hint>=3} onClick={()=>setHint(hint+1)}><Lightbulb size={16}/>Подсказка {Math.min(hint+1,3)} / 3</button>{lesson.hints.slice(0,hint).map((h,i)=><div className="hint" key={i}><b>0{i+1}</b>{h}</div>)}<LessonSolution lesson={lesson}/>{(successful||progress.completed.includes(lesson.id))&&<div className="completion"><Check size={20}/><h3>Урок пройден</h3><p>{lesson.solutionExplanation}</p>{next?<button className="primary" onClick={()=>navigate(`/learn/${next.id}`)}>Следующий урок <ArrowRight size={16}/></button>:<Link to="/progress">Посмотреть прогресс →</Link>}</div>}</div>}
      <Link className="reference-link" to={`/documentation?article=${lesson.id}`}>Открыть справочник <ArrowRight size={14}/></Link></aside>}
      <div className="ide"><div className="ide-toolbar"><div className="file-label"><FileCode2 size={16}/><strong>{LANGUAGE_NAMES[language]}</strong><span className="muted">{lesson?'Учебная среда':project?.name||'Playground'}</span></div><div className="toolbar-actions"><button className={showAI?'ai-active':''} onClick={()=>setShowAI(!showAI)} title="Локальный помощник">✦ AI</button><button title="Сохранить · Ctrl+S" aria-label="Сохранить код" onClick={()=>void save()}><Save size={15}/></button><button title={settings.minimap?"Скрыть миникарту":"Показать миникарту"} className={settings.minimap?"ai-active":""} aria-label="Переключить миникарту" onClick={()=>updateSettings({minimap:!settings.minimap})}><Map size={15}/></button><button title="Сбросить" aria-label="Сбросить среду" onClick={reset}><RotateCcw size={15}/></button>{busy?<button className="stop" onClick={()=>runner.current?.stop()}><Square size={14}/>Stop</button>:<button className="run-button" onClick={()=>void run()}><Play size={14} fill="currentColor"/>Run</button>}{lesson&&<button className="primary" disabled={busy} onClick={()=>void run(true)}><Check size={16}/>Check</button>}</div></div>
      <div className="editor-region">{project&&<aside className="file-tree"><div className="tree-heading">ФАЙЛЫ <button aria-label="Добавить файл" onClick={newFile}><Plus size={14}/></button></div>{project.files.map((f,i)=><button className={active===i?'active-file':''} key={f.name} onClick={()=>setActive(i)}><FileCode2 size={14}/>{f.name}</button>)}<div className="file-tools"><button title="Переименовать файл" aria-label="Переименовать файл" onClick={renameFile}><Pencil size={14}/></button><button title="Удалить файл" aria-label="Удалить файл" onClick={deleteFile}><Trash2 size={14}/></button></div></aside>}<div className="editor-main"><div className="file-tabs">{(project?.files||[{name:currentName}]).map((f,i)=><button className={i===active?'active':''} key={f.name} onClick={()=>setActive(i)}><FileCode2 size={14}/>{f.name}{dirty&&i===active&&<span className="dirty-dot"/>}</button>)}</div><div className="monaco-shell"><Suspense fallback={<div className="muted">Загрузка редактора…</div>}><CodeEditor path={`${projectId||lesson?.id||'scratch'}/${currentName}`} language={language==='html-css'?(currentName.endsWith('.css')?'css':'html'):language==='postgresql'?'sql':language==='objc'?'objective-c':language==='1c'?'1c':language} code={currentCode} onChange={changeCode}/></Suspense></div></div></div>
      {((['python','c','cpp','csharp','objc','rust','1c','java'].includes(language)))&&<details className="stdin-panel" open={stdin.length>0||currentCode.includes('input(')||currentCode.includes('scanf(')||currentCode.includes('cin')||currentCode.includes('ReadLine')||currentCode.includes('Scanner')}><summary>Ввод для программы · STDIN</summary><label htmlFor="program-stdin">Можно заранее вписать данные: ввод читает следующую строку.</label><textarea id="program-stdin" aria-label="Ввод для программы" rows={3} value={stdin} onChange={e=>setStdin(e.target.value)} placeholder="Например: 25" spellCheck={false}/><small>Для Python, Java, C#, C++, Rust и 1С строки читаются по очереди. Для C укажите данные здесь перед Run.</small></details>}
      <div className="console"><div className="console-header"><span><Terminal size={14}/> OUTPUT {result?.results.length?' / TESTS':''}</span><div>{result?.duration!==undefined&&<small className="muted">{result.duration.toFixed(0)} мс</small>}<button onClick={()=>{const error=result?.error||result?.stderr||result?.results.find(r=>r.error)?.error||'';setExplanation(localTutor.explain(error));}} disabled={!result}>Explain Error</button><button onClick={()=>{setResult(null);setExplanation('');}} disabled={busy}>Очистить</button></div></div>{busy&&<div className="runtime-status"><span className="pulse-dot"/>{status}</div>}<Output result={result} lesson={lesson}/>{preview&&<iframe className="html-preview" title="Предпросмотр HTML и CSS" sandbox="" srcDoc={preview}/>}{explanation&&<div className="error-explanation"><b>Локальный справочник ошибок</b><p>{explanation}</p></div>}</div>
      {showAI&&<AIHelp code={currentCode} language={language} onInsert={changeCode}/>}<div className="ide-status"><span><i className={busy?'busy-dot':'green-dot'}/>{status}</span><span>{saveState} · UTF-8 · {language==='c'?'C11 / Clang WASM':
language==='cpp'?'C++20 / Clang AST':
language==='csharp'?'C# / .NET Worker':
language==='objc'?'Objective-C Foundation':
language==='rust'?'Rust / Native AST':
language==='1c'?'1С:Предприятие BSL':
language==='python'?'Pyodide CPython':
language==='postgresql'?'PostgreSQL / PGlite':
language==='html-css'?'HTML / CSS Preview':
language==='javascript'?'JavaScript Worker':
language==='typescript'?'TypeScript Worker':
language==='java'?'Java Hybrid/Worker':'SQLite WASM'}</span></div></div>
    </div>
  </div>;
}
