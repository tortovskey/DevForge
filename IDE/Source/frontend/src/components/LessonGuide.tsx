import {useEffect,useRef,useState} from 'react';
import {Link} from 'react-router-dom';
import {Play,Square,ChevronRight,ChevronLeft} from 'lucide-react';
import {BrowserRunner} from '../runners/runner';
import {checkHtml,documentSource} from '../runners/html';
import type {Lesson,RunResult} from '../types';

const pretty=(value:unknown)=>typeof value==='string'?value:JSON.stringify(value,null,2);
function DataTables({tables}:{tables:{name:string;columns:string[];values:unknown[][]}[]}){
 return <>{tables.map(t=><div className="teaching-table" key={t.name}><b>{t.name}</b><div className="table-scroll"><table><thead><tr>{t.columns.map(c=><th key={c}>{c}</th>)}</tr></thead><tbody>{t.values.map((row,i)=><tr key={i}>{row.map((value,j)=><td key={j}>{value===null?<em>NULL</em>:String(value)}</td>)}</tr>)}</tbody></table></div></div>)}</>;
}
export default function LessonGuide({lesson,onPractice,previous}:{lesson:Lesson;onPractice:()=>void;previous?:Lesson}){
 if(!lesson.guide)return <div className="teaching-guide"><span className="teaching-kicker">СНАЧАЛА — СМЫСЛ</span><h3>{lesson.title}</h3><p className="teaching-intro">{lesson.theory}</p><button className="primary" onClick={onPractice}>Перейти к заданию</button></div>;
 const guide=lesson.guide;
 const [stage,setStage]=useState(0),[example,setExample]=useState(guide.example.code),[prediction,setPrediction]=useState('');
 const [reveal,setReveal]=useState(false),[result,setResult]=useState<RunResult|null>(null),[busy,setBusy]=useState(false),[status,setStatus]=useState(''),[preview,setPreview]=useState('');
 const runner=useRef<BrowserRunner|null>(null),alive=useRef(true),lock=useRef(false);
 useEffect(()=>{alive.current=true;return()=>{alive.current=false;runner.current?.reset();};},[]);
 async function runExample(){
  if(lock.current)return;lock.current=true;setBusy(true);setResult(null);setPreview('');
  try{
   let output:RunResult;
   if(lesson.language==='html-css'){
    const source=documentSource(example);setPreview(source);
    output=await checkHtml(source,[]);
   }else{
    if(!runner.current)runner.current=new BrowserRunner(lesson.language,text=>{if(alive.current)setStatus(text);});
    output=await runner.current.run({code:example,setupSql:guide.example.setupSql,reset:true,context:'teaching:'+lesson.id});
   }
   if(alive.current)setResult(output);
  }catch(error){if(alive.current)setResult({stdout:'',stderr:'',tables:[],results:[],error:String(error)});}
  finally{lock.current=false;if(alive.current)setBusy(false);}
 }
 const goto=(next:number)=>{setStage(next);document.querySelector('.lesson-panel')?.scrollTo({top:0,behavior:'smooth'});};
 return <div className="teaching-guide">
  <nav className="teaching-steps" aria-label="Шаги объяснения">{['Понять','Разобрать пример','Попробовать'].map((name,i)=><button key={name} aria-current={stage===i?'step':undefined} onClick={()=>goto(i)}><span>{i+1}</span>{name}</button>)}</nav>
  {stage===0?<>
   <span className="teaching-kicker">СНАЧАЛА — СМЫСЛ</span><h3>Что здесь происходит</h3>
   <p className="teaching-intro">{guide.idea}</p>
   {lesson.lifeExample&&<div className="teaching-note"><b>Представьте знакомую ситуацию</b><p>{lesson.lifeExample}</p></div>}
   <details className="teaching-details" open={lesson.level==='Beginner'}><summary>Новые слова и символы — простыми словами</summary><dl>{guide.terms.map(t=><div key={t.term}><dt><code>{t.term}</code></dt><dd>{t.meaning}</dd></div>)}</dl><p>Имена вроде number, coins или name выбирает автор программы. Названия из задания сохраняйте точно: проверка обращается к ним по имени.</p></details>
   <div className="teaching-note"><b>Как проходить этот урок</b><ol><li>Прочитайте маленький пример и разбор его действий.</li><li>Предскажите результат, затем запустите пример.</li><li>Измените одну вещь и сравните результат.</li><li>Перейдите к отдельному заданию справа.</li></ol><p>Ошибка не отнимает XP. Можно повторять запуск и открывать подсказки.</p></div>
   {previous&&<Link className="teaching-backlink" to={`/learn/${previous.id}`}>Нужно повторить предыдущую тему: {previous.title} →</Link>}
  </>:<>
   <span className="teaching-kicker">{stage===1?'УЧЕБНЫЙ ПРИМЕР':'ИЗМЕНИТЕ ОДНУ ВЕЩЬ'}</span>
   <h3>{stage===1?'Проследим каждый шаг':'Небольшой эксперимент'}</h3>
   {stage===2&&<div className="teaching-note"><p>{guide.experiment}</p></div>}
   {guide.example.tables?.length>0&&<details className="teaching-details" open><summary>Данные для этого примера</summary><DataTables tables={guide.example.tables}/><p>Каждый запуск примера начинает с этих данных. Учебное задание справа имеет собственную базу.</p></details>}
   {guide.example.setupSql&&<details className="teaching-details"><summary>Как подготовлена таблица примера</summary><pre>{guide.example.setupSql}</pre></details>}
   <label className="teaching-label" htmlFor="teaching-code">Код примера — его можно менять</label>
   <textarea id="teaching-code" className="teaching-code" onKeyDown={e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();e.stopPropagation();void runExample();}}} spellCheck={false} value={example} onChange={e=>setExample(e.target.value)} rows={Math.min(20,Math.max(4,example.split('\n').length))}/>
   <h3>Разбор исходного примера</h3><ol className="teaching-trace">{guide.steps.map((step,i)=><li key={i}><span>{i+1}</span><p>{step}</p></li>)}</ol>
   <div className="teaching-actions">{busy?<button onClick={()=>runner.current?.stop()}><Square size={14}/>Остановить пример</button>:<button className="primary" onClick={()=>void runExample()}><Play size={14}/>Запустить пример</button>}<button disabled={busy} onClick={()=>{setExample(guide.example.code);setResult(null);setPreview('');}}>Вернуть исходный пример</button></div>
   <p className="teaching-caption">Этот запуск не меняет ваш код справа и не засчитывает урок. {lesson.language==='python'?'Для добавленного вами input() используйте основной редактор с окном ввода.':''}</p>
   {busy&&<p role="status">{status||'Готовим пример…'}</p>}
   {result&&<section className="teaching-output" aria-label="Результат примера"><b>Получилось при запуске</b>{result.error&&<pre className="error-text">{result.error}</pre>}{result.stdout&&<pre>{result.stdout}</pre>}{result.stderr&&<pre>{result.stderr}</pre>}{result.tables.length>0&&<DataTables tables={result.tables.map((t,i)=>({...t,name:`Результат ${i+1}`}))}/>}<p>Если результат отличается от ожидаемого ниже, сравните изменённый код с исходным. Это полезная часть эксперимента.</p></section>}
   {preview&&<iframe title="Учебный пример HTML" className="teaching-preview" sandbox="" srcDoc={preview}/>}
   <label className="teaching-label" htmlFor="teaching-prediction">Мой прогноз: что получится и почему? <span>(можно пропустить)</span></label><textarea id="teaching-prediction" rows={2} value={prediction} onChange={e=>setPrediction(e.target.value)} placeholder="Например: будет 6, потому что к 4 прибавили 2."/>
   <button className="teaching-reveal" aria-expanded={reveal} onClick={()=>setReveal(!reveal)}>{reveal?'Скрыть ожидаемый результат':'Показать ожидаемый результат исходного примера'}</button>
   {reveal&&<div className="teaching-answer"><b>{guide.example.kind==='html'?'Что проверяем в странице':guide.example.kind==='table'?'Строки результата':'Вывод'}</b>{guide.example.dom&&<p><code>{guide.example.dom.selector}</code> · {guide.example.dom.css||guide.example.dom.attribute||guide.example.dom.property}</p>}<pre>{pretty(guide.example.expected)}</pre><p>Этот результат относится к исходному коду выше. После вашего изменения он может быть другим.</p></div>}
   
   <details className="teaching-details"><summary>Дополнительные подробности по теме</summary>{lesson.theory.split('\n\n').map((p,i)=><p key={i}>{p}</p>)}</details>
  </>}
  <div className="teaching-navigation">{stage>0&&<button onClick={()=>goto(stage-1)}><ChevronLeft size={16}/>Назад</button>}{stage<2?<button className="primary" onClick={()=>goto(stage+1)}>{stage===0?'К маленькому примеру':'К эксперименту'}<ChevronRight size={16}/></button>:<button className="primary" onClick={onPractice}>Теперь самостоятельное задание<ChevronRight size={16}/></button>}</div>
  <button className="teaching-skip" onClick={onPractice}>Я уже понял — перейти к заданию</button>
  {!!lesson.resources?.length&&<details className="teaching-details"><summary>Дополнительные материалы (необязательно)</summary><p>Урок можно пройти без видео. Ссылкам нужен интернет; язык указан рядом.</p>{lesson.resources.map(r=><p key={r.url}><a href={r.url} target="_blank" rel="noopener noreferrer">{r.title} ↗</a> · {r.language}</p>)}</details>}
 </div>;
}

export function LessonTaskSupport({lesson}:{lesson:Lesson}){
 if(!lesson.guide)return null;
 return <div className="task-support"><h3>Что сделать по порядку</h3><ol>{lesson.guide.taskSteps.map((s,i)=><li key={i}>{s}</li>)}</ol><div className="teaching-note"><b>Где писать и что нажимать</b><p>Пишите решение в большом редакторе справа. <b>Run</b> запускает его и показывает результат внизу. <b>Check</b> сравнивает решение с условиями задачи и засчитывает урок. Ошибка — повод поправить код и попробовать ещё раз.</p></div>{lesson.guide.taskTables?.length>0&&<details className="teaching-details" open><summary>Исходные данные задания</summary><DataTables tables={lesson.guide.taskTables}/><p>Показаны первые 12 строк каждой таблицы. Полная подготовка базы приведена ниже.</p></details>}{lesson.setupSql&&<details className="teaching-details"><summary>Структура и подготовка учебной базы</summary><pre>{lesson.setupSql}</pre><p>Эти команды уже выполняются средой. В решение переписывать их не нужно.</p></details>}<details className="teaching-details"><summary>Примеры того, что проверяет Check</summary>{lesson.tests.map(t=><div className="teaching-case" key={t.id}><b>{t.label}</b>{t.stdin!==undefined&&<><small>Входные данные</small><pre>{t.stdin||'(пустой ввод)'}</pre></>}{t.expression&&<><small>Вызов или значение, которое проверяют</small><pre>{t.expression}</pre></>}{t.dom&&<p>Элемент <code>{t.dom.selector}</code>: {t.dom.css||t.dom.attribute||t.dom.property}</p>}<small>Ожидаемый результат</small><pre>{pretty(t.expected)}</pre></div>)}</details><details className="teaching-details"><summary>Если не получается — проверьте эти пункты</summary><ul>{lesson.guide.checklist.map(item=><li key={item}>{item}</li>)}</ul><p>{lesson.commonMistakes}</p></details></div>;
}
export function LessonSolution({lesson}:{lesson:Lesson}){
 if(!lesson.guide)return null;
 return <details className="teaching-details solution-details"><summary>Застряли? Открыть готовое решение для сверки</summary><p>Это ответ именно к самостоятельному заданию. Сравните его со своим кодом, найдите одно отличие и объясните его. После этого закройте ответ и попробуйте написать решение заново. Открытие ответа само по себе не завершает урок.</p><pre>{lesson.guide.solution}</pre><h3>Почему это работает</h3>{lesson.solutionExplanation.split('\n\n').map((p,i)=><p key={i}>{p}</p>)}<p>Для закрепления: {lesson.guide.experiment}</p></details>;
}
