import {useState} from 'react';
import {Link,useNavigate,useSearchParams} from 'react-router-dom';
import {ArrowRight,ArrowUpRight,Check,CheckCircle2,ChevronRight,Clock3,Code2,Copy,Database,FileCode2,Flame,FolderOpen,GraduationCap,Layers,Plus,Search,Sparkles,Target,Trash2,Trophy,BookOpen,Sun,Moon,Terminal,RefreshCw} from 'lucide-react';
import {useStore} from '../services/store';
import {api} from '../services/api';
import AISettings from '../components/AISettings';
import SyncModal from '../components/SyncModal';
import { PlatformAdapter } from '../services/platform';
import { Briefcase, Laptop, Globe } from 'lucide-react';
import type { Track } from '../types';

import {LANGUAGE_NAMES} from '../types';
import type {LanguageId,Project} from '../types';

export function PageHeading({eyebrow,title,description,action}:{eyebrow:string;title:string;description:string;action?:React.ReactNode}){return <div className="page-heading"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{description}</p></div>{action}</div>;}
function LanguageIcon({language}:{language:string}){
  const cls = ['python','sql','postgresql','html-css','c','cpp','csharp','objc','rust','1c','javascript','typescript','java','lua','assembly'].includes(language) ? (language === '1c' ? 'lang-1c' : language) : 'default';
  return <span className={`language-icon ${cls}`}>
    {['sql','postgresql'].includes(language) ? <Database size={23}/> : (language === 'assembly' ? <Terminal size={23}/> : <Code2 size={23}/>)}
  </span>;
}
export function Dashboard(){
  const {courses,progress,settings,projects,plan}=useStore();
  const [showSync,setShowSync]=useState(false);
  const lessons=courses.flatMap(c=>c.lessons),next=lessons.find(l=>l.id===settings.lastLesson&&!progress.completed.includes(l.id))||lessons.find(l=>l.id===plan.courses.find(c=>c.nextLesson)?.nextLesson)||lessons.find(l=>!progress.completed.includes(l.id))||lessons[0];
  const done=progress.completed.length,percent=lessons.length?Math.round(done/lessons.length*100):0;
  return <div className="page dashboard"><PageHeading eyebrow="YOUR PERSONAL PROGRAMMING ACADEMY" title="Хороший день, чтобы создать что-то." description="Продолжайте учиться, экспериментировать и превращать идеи в код." action={<Link className="button secondary" to="/projects"><Plus size={16}/>Новый проект</Link>}/>
  <div className="stats-grid"><Stat icon={<BookOpen size={18}/>} value={`${done}`} label="Уроков пройдено" note={`из ${lessons.length} доступных`}/><Stat icon={<Flame size={18}/>} value={progress.xp.toString()} label="Всего опыта" note="Каждый шаг имеет значение"/><Stat icon={<Target size={18}/>} value={`${percent}%`} label="Прогресс обучения" note="13 направлений обучения"/><Stat icon={<FolderOpen size={18}/>} value={projects.length.toString()} label="Ваших проектов" note="Идеи, которые стали кодом"/></div>
  <div className="dashboard-grid"><div className="dashboard-primary"><section className="continue-card"><div className="hero-grid"/><div className="continue-content"><span className="eyebrow accent"><span className="pulse-dot"/>ПРОДОЛЖИТЬ ОБУЧЕНИЕ</span><div className="course-tag">{LANGUAGE_NAMES[next.language]}<span>УРОК {String(next.order).padStart(2,'0')}</span></div><h2>{next.title}</h2><p>Немного теории. Настоящий код.<br/>Ещё один шаг к уверенному программированию.</p><Link className="button primary" to={`/learn/${next.id}`}>Открыть урок <ArrowRight size={17}/></Link><div className="hero-meta"><span><Clock3 size={13}/>{next.minutes} мин</span><span><Sparkles size={13}/>{next.xp} XP</span><span>{next.level}</span></div></div><div className="hero-code" aria-hidden="true"><div className="code-window-dots"><i/><i/><i/><span>hello_future.py</span></div><pre><span className="code-purple">def</span> <span className="code-blue">build_your_future</span>():{'\n'}    skills = [<span className="code-green">"curiosity"</span>]{'\n'}    <span className="code-purple">while</span> <span className="code-orange">True</span>:{'\n'}        learn(){'\n'}        practice(){'\n'}        <span className="code-blue">create</span>()</pre><div className="code-bottom"><span className="green-dot"/>Возможности начинаются здесь.</div></div></section>
  <div className="section-heading"><h2>Ваши направления</h2><Link to="/learn">Все языки <ArrowUpRight size={14}/></Link></div><div className="course-grid">{courses.map(course=>{const completed=course.lessons.filter(l=>progress.completed.includes(l.id)).length;return <Link to={`/learn?language=${course.id}`} className="course-card" key={course.id}><div className="course-card-top"><LanguageIcon language={course.id}/><span className="pill available">Доступен</span></div><h3>{course.name}</h3><p>{{c:'От первого printf до указателей, памяти и проектов.',python:'От первого print() до собственных классов.',sql:'От первого SELECT до связанных таблиц.',postgresql:'Типы, JSON, CTE и оконные функции.','html-css':'Первая страница, стили и адаптивная сетка.',javascript:'Скрипты, функции, массивы, объекты и замыкания.',
typescript:'Строгая типизация, интерфейсы, объединения и дженерики.',
java:'Классы, методы, инкапсуляция, ООП и наследование.',
cpp:'C++: классы, ссылки, перегрузка операторов, STL vector и шаблоны.',
csharp:'C#: классы, свойства { get; set; }, списки List<T> и основы .NET.',
objc:'Objective-C: Foundation, интерфейсы, сообщения [obj msg] и свойства.',
rust:'Rust: безопасность памяти, владение (ownership), ссылки &mut, match и vec!.',
'1c':'1С:Предприятие: процедуры, функции, Массивы, Структуры и ТаблицыЗначений.',
'lua':'Lua 5.3: таблицы, метатаблицы, замыкания и корутины.',
'assembly':'x86-64 NASM: регистры, системные вызовы, память и флаги процессора.'
}[course.id]||'Учебный курс с практическими задачами.'}</p><div className="course-progress"><span>{completed} / {course.lessons.length} уроков</span><span>{course.lessons.length?Math.round(completed/course.lessons.length*100):0}%</span></div><div className="progress-track"><i style={{width:`${course.lessons.length?Math.round(completed/course.lessons.length*100):0}%`}}/></div></Link>;})}</div>
  <div className="section-heading"><h2>Недавние проекты</h2><Link to="/projects">Лаборатория <ArrowUpRight size={14}/></Link></div><div className="project-list">{projects.length?projects.slice(0,3).map(p=><Link to={`/projects/${p.id}`} className="project-row" key={p.id}><FileCode2 size={20}/><div><strong>{p.name}</strong><small>{LANGUAGE_NAMES[p.language]} · {p.files.length} файлов</small></div><span>{new Date(p.updated_at).toLocaleDateString('ru')}</span><ArrowUpRight size={16}/></Link>):<div className="empty-projects"><FolderOpen size={26}/><div><strong>Место для вашей первой идеи</strong><p>Создайте проект и начните экспериментировать.</p></div><Link className="button secondary" to="/projects"><Plus size={15}/>Создать</Link></div>}</div></div>
  <aside className="dashboard-aside"><section className="journey-card"><span className="eyebrow">ВАШ ПУТЬ</span><div className="journey-emblem"><Layers size={30}/></div><h3>{done>=15?'Elementary':'Beginner'}</h3><p>{done>=15?'Базовые задачи освоены. Продолжайте практику.':'Сильный фундамент начинается с малого.'}</p><div className="journey-line"><span>Освоенные темы</span><b>{done} / {lessons.length}</b></div><div className="progress-track"><i style={{width:`${percent}%`}}/></div><small>Уровень зависит от пройденных проверок, а не только от XP.</small><Link to="/assessment">Индивидуальный маршрут <ArrowRight size={14}/></Link></section>
  <section className="next-topics"><div className="section-heading"><h3>Следующие шаги</h3><GraduationCap size={18}/></div>{lessons.filter(l=>!progress.completed.includes(l.id)).slice(0,3).map((l,i)=><Link key={l.id} to={`/learn/${l.id}`}><span className="step-number">0{i+1}</span><div><strong>{l.title}</strong><small>{LANGUAGE_NAMES[l.language]} · {l.minutes} мин</small></div><ChevronRight size={15}/></Link>)}</section><div className="tip-card"><Terminal size={20}/><h3>Меньше кликов. Больше кода.</h3><p>Запускайте программу прямо из редактора.</p><kbd>Ctrl</kbd><span> + </span><kbd>Enter</kbd></div></aside></div>
  <footer className="page-footer"><span><span className="green-dot"/>Локальная среда готова к работе · <span className={`platform-pill ${PlatformAdapter.isDesktop()?'desktop':'web'}`}>{PlatformAdapter.isDesktop()?<Laptop size={12}/>:<Globe size={12}/>}{PlatformAdapter.isDesktop()?'Desktop (WebView2)':'Web (Браузер)'}</span></span><div style={{display:'flex',gap:12,alignItems:'center'}}><button className="button secondary compact" style={{padding:'4px 10px',fontSize:'12px'}} onClick={()=>setShowSync(true)}><RefreshCw size={13}/>Синхронизация</button><span>DevForge IDE · 1.0.0</span></div></footer><SyncModal isOpen={showSync} onClose={()=>setShowSync(false)}/></div>;
}
function Stat({icon,value,label,note}:{icon:React.ReactNode;value:string;label:string;note:string}){return <div className="stat-card"><div className="stat-label">{label}{icon}</div><strong>{value}</strong><small>{note}</small></div>;}


function TracksView({ tracks, progress }: { tracks: Track[]; progress: any }) {
  const completedSet = new Set(progress.completed);

  return (
    <div className="track-cards-grid">
      {tracks.map((track) => {
        const allLessonIds = track.modules.flatMap((m) => m.lessonIds);
        const completedCount = allLessonIds.filter((id) => completedSet.has(id)).length;
        const percent = allLessonIds.length ? Math.round((completedCount / allLessonIds.length) * 100) : 0;

        return (
          <div className="track-card" key={track.id}>
            <div className="track-header">
              <div>
                <span className="track-kicker">{track.kicker}</span>
                <h3 className="track-title">{track.title}</h3>
                <div className="track-badge-tag">{track.targetRole} · {track.level}</div>
              </div>
              <span className="badge-pill">{track.badge}</span>
            </div>

            <p className="track-description">{track.description}</p>

            <div className="track-stack-list">
              {track.stack.map((tech) => (
                <span className="stack-chip" key={tech}>{tech}</span>
              ))}
            </div>

            <div className="course-progress" style={{ margin: '4px 0' }}>
              <span>Прогресс направления: {completedCount} / {allLessonIds.length} уроков освоено</span>
              <strong>{percent}%</strong>
            </div>
            <div className="progress-track"><i style={{ width: `${percent}%` }} /></div>

            <div className="track-modules-accordion">
              {track.modules.map((mod) => (
                <div className="track-module-row" key={mod.id}>
                  <div className="track-module-title">
                    <span>{mod.title}</span>
                    <small className="muted">{mod.lessonIds.filter((id) => completedSet.has(id)).length}/{mod.lessonIds.length}</small>
                  </div>
                  <div className="track-skills-tags">Навыки: {mod.skills.join(' · ')}</div>
                  <div className="track-lessons-strip">
                    {mod.lessonIds.map((lid) => {
                      const isDone = completedSet.has(lid);
                      return (
                        <Link
                          key={lid}
                          to={`/learn/${lid}`}
                          className={`track-lesson-pill ${isDone ? 'completed' : ''}`}
                          title={lid}
                        >
                          {isDone ? <Check size={12} /> : null}
                          <span>{lid.replace(/^(backend-|frontend-|java-|python-|html-css-|javascript-|typescript-|postgresql-)/, '')}</span>
                        </Link>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>

            <div className="track-capstone-banner">
              <div className="track-capstone-info">
                <h4>🏆 {track.capstone.title}</h4>
                <p>{track.capstone.description}</p>
              </div>
              <Link to={`/learn/${track.capstone.id}`} className="button primary">
                {completedSet.has(track.capstone.id) ? 'Повторить проект' : 'Начать проект'}
                <ArrowRight size={16} />
              </Link>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export function Learn(){
  const {courses,languages,progress,tracks}=useStore();const [search,setSearch]=useState(''),[level,setLevel]=useState('all');const [params,setParams]=useSearchParams();const [activeTab,setActiveTab]=useState<'languages'|'tracks'>('languages');const lang=params.get('language')||'python';const course=courses.find(c=>c.id===lang)||courses[0];
  return <div className="page"><PageHeading eyebrow="LEARNING PATHS" title="Практика делает разработчика." description="От самых основ до практики Junior+: объяснения, проверка кода и самостоятельные проекты." action={<Link className="button primary" to="/assessment">Определить уровень <ArrowRight size={16}/></Link>}/>
  <div className="track-switcher">
    <button className={`track-tab-btn ${activeTab==='languages'?'active':''}`} onClick={()=>setActiveTab('languages')}>
      <Code2 size={16}/>Курсы по языкам ({courses.length})
    </button>
    <button className={`track-tab-btn ${activeTab==='tracks'?'active':''}`} onClick={()=>setActiveTab('tracks')}>
      <Briefcase size={16}/>Профессиональные треки ({tracks?.length||3})
    </button>
  </div>
  {activeTab==='tracks' && tracks && <TracksView tracks={tracks} progress={progress}/>}
  {activeTab==='languages' && <><div className="catalog-tabs">{courses.map(c=><button key={c.id} className={course?.id===c.id?'selected':''} onClick={()=>{setParams({language:c.id});setLevel('all');setSearch('');}}><LanguageIcon language={c.id}/><div><strong>{c.name}</strong><small>{c.lessons.length} уроков · с самых основ</small></div></button>)}</div>{course&&<><div className="section-heading"><h2>{course.name}</h2><span className="muted">{course.lessons.filter(l=>progress.completed.includes(l.id)).length} из {course.lessons.length} завершено</span></div><div className="lesson-filters"><label className="search-box"><Search size={16}/><input aria-label="Поиск урока" placeholder="Найти тему или задачу…" value={search} onChange={e=>setSearch(e.target.value)}/></label><select aria-label="Уровень уроков" value={level} onChange={e=>setLevel(e.target.value)}><option value="all">Все уровни</option>{[...new Set(course.lessons.map(l=>l.level))].map(value=><option key={value}>{value}</option>)}</select></div><p className="muted">Junior+ — ориентир программы. Навык закрепляется самостоятельными проектами; одних автопроверок недостаточно.</p>{course.id==='postgresql'&&<p className="note">Если SQL для вас новый, сначала пройдите основы SQLite: SELECT, WHERE, GROUP BY и JOIN. Здесь те же идеи применяются в PostgreSQL.</p>}<div className="lesson-list">{course.lessons.filter(l=>(level==='all'||l.level===level)&&`${l.title} ${l.topic} ${l.task}`.toLowerCase().includes(search.toLowerCase())).map(l=><Link to={`/learn/${l.id}`} key={l.id} className="lesson-row"><span className={progress.completed.includes(l.id)?'lesson-number complete':'lesson-number'}>{progress.completed.includes(l.id)?<Check size={18}/>:String(l.order).padStart(2,'0')}</span><div><span className="eyebrow">{l.section}</span><h3>{l.title}</h3><p>{l.topic}</p></div><span className="pill">{l.level}</span><span className="muted">{l.minutes} мин</span><span className="xp">{l.xp} XP</span><ChevronRight size={18}/></Link>)}</div></>}<div className="section-heading"><h2>Дальше — больше</h2><span className="muted">Будущие направления</span></div><div className="planned-grid">{languages.filter(l=>l.status==='planned').map(l=><div className="planned-card" key={l.id}><Code2 size={18}/><h3>{l.name}</h3><span className="pill">Planned</span><p>{l.description}</p></div>)}</div></>}</div>;
}

export function Challenges(){
  const {courses,progress}=useStore();const [language,setLanguage]=useState('all');
  const lessons=courses.flatMap(c=>c.lessons).filter(l=>language==='all'||l.language===language);
  return <div className="page"><PageHeading eyebrow="PRACTICE LAB" title="Проверьте себя в деле." description="Практические задания курсов. Повторение закрепляет навык; XP за задачу начисляется один раз."/><div className="filter-buttons">{[['all','Все задания'],['python','Python'],['c','C'],['cpp','C++'],['csharp','C#'],['objc','Obj-C'],['rust','Rust'],['1c','1С'],['javascript','JS'],['typescript','TS'],['java','Java'],['sql','SQLite'],['postgresql','PostgreSQL'],['html-css','HTML/CSS']].map(([id,title])=><button className={language===id?'selected':''} key={id} onClick={()=>setLanguage(id)}>{title}</button>)}</div><div className="challenge-grid">{lessons.map(l=><Link className="challenge-card" to={`/learn/${l.id}`} key={l.id}><div className="course-card-top"><LanguageIcon language={l.language}/>{progress.completed.includes(l.id)?<CheckCircle2 className="success" size={20}/>:<span className="xp">+{l.xp} XP</span>}</div><h3>{l.title}</h3><p>{l.task}</p><div className="card-footer"><span>{l.tests.length} проверок · {l.level}</span><ArrowRight size={17}/></div></Link>)}</div></div>;
}
export function Documentation(){
  const {docs,notify,courses}=useStore();const [params,setParams]=useSearchParams(),[search,setSearch]=useState(''),[language,setLanguage]=useState('all');
  const filtered=docs.filter(d=>(language==='all'||d.language===language)&&`${d.title} ${d.explanation}`.toLowerCase().includes(search.toLowerCase()));
  const article=docs.find(d=>d.id===params.get('article'))||filtered[0];
  const copy=async(text:string)=>{try{await navigator.clipboard.writeText(text);notify('Пример скопирован');}catch{notify('Не удалось получить доступ к буферу обмена. Выделите пример вручную.');}};
  return <div className="page"><PageHeading eyebrow="LOCAL KNOWLEDGE BASE" title="Ответы всегда под рукой." description="Короткие объяснения, рабочие примеры и типичные ошибки. Доступно без интернета."/><div className="docs-layout"><aside className="docs-sidebar"><label className="search-box"><Search size={17}/><input aria-label="Поиск по документации" placeholder="Найти в документации…" value={search} onChange={e=>setSearch(e.target.value)}/></label><select aria-label="Язык документации" value={language} onChange={e=>setLanguage(e.target.value)}><option value="all">Все языки</option><option value="python">Python</option><option value="c">C</option><option value="cpp">C++</option><option value="csharp">C#</option><option value="objc">Objective-C</option><option value="rust">Rust</option><option value="1c">1С:Предприятие</option><option value="javascript">JavaScript</option><option value="typescript">TypeScript</option><option value="java">Java</option><option value="lua">Lua</option><option value="assembly">Assembly (x86-64 NASM)</option><option value="sql">SQL / SQLite</option><option value="postgresql">PostgreSQL</option><option value="html-css">HTML / CSS</option></select><nav>{filtered.map(d=><button key={d.id} className={article?.id===d.id?'selected':''} onClick={()=>setParams({article:d.id})}><span className={`doc-dot ${d.language}`}/><div>{d.title}<small>{LANGUAGE_NAMES[d.language]}</small></div><ChevronRight size={13}/></button>)}</nav>{!filtered.length&&<p className="muted">Ничего не найдено. Попробуйте другое слово.</p>}</aside>{article?<article className="doc-article prose"><span className="eyebrow">{LANGUAGE_NAMES[article.language]?.toUpperCase()||'GUIDE'} / {article.category}</span><h2>{article.title}</h2>{article.explanation.split('\n\n').map((p,i)=><p key={i}>{p}</p>)}<h3>Синтаксис</h3><div className="code-example"><button title="Копировать синтаксис" aria-label="Копировать синтаксис" onClick={()=>void copy(article.syntax)}><Copy size={15}/></button><pre>{article.syntax}</pre></div><h3>Рабочий пример</h3><div className="code-example"><button title="Копировать пример" aria-label="Копировать пример" onClick={()=>void copy(article.example)}><Copy size={15}/></button><pre>{article.example}</pre></div><h3>Типичные ошибки</h3><div className="note">{article.mistakes}</div><h3>Закрепите на практике</h3>{article.relatedLessons.map(id=><Link className="related-lesson" to={`/learn/${id}`} key={id}><BookOpen size={18}/>{courses.flatMap(c=>c.lessons).find(l=>l.id===id)?.title}<ArrowRight size={16}/></Link>)}</article>:<div className="empty-state">Статьи не найдены</div>}</div></div>;
}
export function Projects(){
  const {projects,refresh,notify}=useStore(),navigate=useNavigate();const [name,setName]=useState(''),[language,setLanguage]=useState<LanguageId>('python'),[creating,setCreating]=useState(false),[busy,setBusy]=useState(false);
  async function create(e:React.FormEvent){
    e.preventDefault();setBusy(true);
    try{
      const defaultFilename = (
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
        language==='java'?'Main.java':'query.sql'
      );
      const defaultContent = (
        language==='c'?'#include <stdio.h>\nint main(void) { puts("Hello, DevForge!"); return 0; }':
        language==='cpp'?'#include <iostream>\n\nint main() {\n    std::cout << "Hello, DevForge C++!" << std::endl;\n    return 0;\n}':
        language==='csharp'?'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, DevForge C#!");\n    }\n}':
        language==='objc'?'#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSLog(@"Hello, DevForge Objective-C!");\n    }\n    return 0;\n}':
        language==='rust'?'fn main() {\n    println!("Hello, DevForge Rust!");\n}':
        language==='1c'?'Сообщить("Привет, DevForge 1С!");':
        language==='html-css'?'<h1>Моя первая страница</h1>\n<p>Здесь начинается идея.</p>':
        language==='python'?'# Ваш следующий проект начинается здесь\nprint("Hello, DevForge!")':
        language==='javascript'?'// Ваш скрипт JavaScript\nconsole.log("Hello, DevForge!");':
        language==='typescript'?'// Типизированный код TypeScript\nconst greet = (name: string): string => `Привет, ${name}!`;\nconsole.log(greet("DevForge"));':
        language==='java'?'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, DevForge!");\n    }\n}':
        '-- Ваша независимая база SQLite\nSELECT \'Hello, DevForge!\' AS message;'
      );
      const project=await api<Project>('/projects','POST',{name,language,files:[{name:defaultFilename,content:defaultContent}]});
      await refresh();navigate(`/projects/${project.id}`);
    }catch(e){notify(String(e));}finally{setBusy(false);}
  }
  async function remove(project:Project){if(!confirm(`Удалить проект «${project.name}» и все его файлы?`))return;try{await api(`/projects/${project.id}`,'DELETE');localStorage.removeItem(`project:${project.id}`);await refresh();notify('Проект удалён');}catch(e){notify(String(e));}}
  return <div className="page"><PageHeading eyebrow="PROJECT LAB" title="Пространство для ваших идей." description="Создавайте, сохраняйте и запускайте собственный код. Все файлы хранятся локально." action={<button className="primary" onClick={()=>setCreating(!creating)}><Plus size={17}/>Новый проект</button>}/>{creating&&<form className="create-project" onSubmit={create}><label>Название проекта<input autoFocus required maxLength={80} placeholder="Мой первый проект" value={name} onChange={e=>setName(e.target.value)}/></label><label>Язык<select value={language} onChange={e=>setLanguage(e.target.value as LanguageId)}><option value="python">Python</option><option value="c">C</option><option value="cpp">C++</option><option value="csharp">C#</option><option value="objc">Objective-C</option><option value="rust">Rust</option><option value="1c">1С:Предприятие</option><option value="javascript">JavaScript</option><option value="typescript">TypeScript</option><option value="java">Java</option><option value="lua">Lua</option><option value="assembly">Assembly (x86-64 NASM)</option><option value="sql">SQL / SQLite</option><option value="postgresql">PostgreSQL</option><option value="html-css">HTML / CSS</option></select></label><button className="primary" disabled={busy||!name.trim()} type="submit">{busy?'Создание…':'Создать проект'}<ArrowRight size={16}/></button><button type="button" onClick={()=>setCreating(false)}>Отмена</button></form>}<div className="challenge-grid">{projects.map(project=><div className="project-card" key={project.id}><div className="course-card-top"><LanguageIcon language={project.language}/><button aria-label={`Удалить ${project.name}`} title="Удалить проект" onClick={()=>void remove(project)}><Trash2 size={16}/></button></div><Link to={`/projects/${project.id}`}><h3>{project.name}</h3><p>{project.files.length} файлов · {LANGUAGE_NAMES[project.language]}</p><div className="card-footer"><span>{new Date(project.updated_at).toLocaleDateString('ru')}</span><span>Открыть <ArrowUpRight size={16}/></span></div></Link></div>)}</div>{!projects.length&&!creating&&<div className="empty-state"><FolderOpen size={48}/><h2>Всё начинается с идеи</h2><p>Калькулятор, коллекция данных или ваш первый класс.<br/>Создайте проект и проверьте, что получится.</p><button className="primary" onClick={()=>setCreating(true)}><Plus size={17}/>Создать первый проект</button></div>}<div className="note lab-note">Поддерживаются все 15 языков программирования! C, C++, C#, Objective-C, Rust, 1С, Python, JavaScript, TypeScript, Java, Lua, Assembly (x86-64 NASM), SQL, PostgreSQL и HTML/CSS запускаются локально в браузере без обращения к внешним серверам.</div></div>;
}
export function ProgressPage(){
  const {progress,courses}=useStore();const lessons=courses.flatMap(c=>c.lessons),successful=progress.attempts.filter(a=>a.passed===a.total).length;
  return <div className="page"><PageHeading eyebrow="YOUR LEARNING JOURNEY" title="Каждая решённая задача — шаг вперёд." description="Прогресс основан на успешно пройденных проверках. Повторные решения не увеличивают XP."/><div className="stats-grid"><Stat icon={<Trophy size={18}/>} value={progress.xp.toString()} label="Заработано XP" note="За первое прохождение"/><Stat icon={<CheckCircle2 size={18}/>} value={progress.completed.length.toString()} label="Пройдено уроков" note={`Из ${lessons.length} доступных`}/><Stat icon={<Target size={18}/>} value={progress.attemptCount.toString()} label="Всего попыток" note="Каждая попытка — практика"/><Stat icon={<Flame size={18}/>} value={`${successful}/${progress.attempts.length}`} label="Успешных проверок" note="Среди последних 50 попыток"/></div><div className="course-grid">{courses.map(c=><section className="progress-course" key={c.id}><div className="course-card-top"><LanguageIcon language={c.id}/><strong>{c.lessons.filter(l=>progress.completed.includes(l.id)).length} / {c.lessons.length}</strong></div><h2>{c.name}</h2><div className="skill-grid">{c.lessons.map(l=><Link title={l.title} className={progress.completed.includes(l.id)?'complete':''} key={l.id} to={`/learn/${l.id}`}>{progress.completed.includes(l.id)?<Check size={16}/>:l.order}</Link>)}</div><p className="muted">{c.lessons.filter(l=>progress.completed.includes(l.id)).length>=8?'Основные темы освоены':'Развивайте основу — завершайте уроки и проверяйте решения.'}</p></section>)}</div><div className="section-heading"><h2>История практики</h2><span className="muted">Последние 50 попыток</span></div>{progress.attempts.length?<div className="table-scroll history"><table><thead><tr><th>Урок</th><th>Результат</th><th>Время</th></tr></thead><tbody>{progress.attempts.map(a=><tr key={a.id}><td><Link to={`/learn/${a.lesson_id}`}>{lessons.find(l=>l.id===a.lesson_id)?.title}</Link></td><td className={a.passed===a.total?'success':'muted'}>{a.passed} / {a.total} тестов</td><td>{new Date(a.created_at).toLocaleString('ru')}</td></tr>)}</tbody></table></div>:<div className="empty-state compact"><Target size={30}/><p>Первая проверка появится здесь после нажатия Check в уроке.</p><Link to="/learn">Выбрать урок →</Link></div>}</div>;
}
export function SettingsPage(){
  const {settings,updateSettings,notify}=useStore();
  const [showSync,setShowSync]=useState(false);const update=(patch:Partial<typeof settings>)=>updateSettings(patch).catch(e=>notify(String(e)));
  return <div className="page settings-page"><PageHeading eyebrow="MAKE IT YOURS" title="Ваша среда. Ваши правила." description="Настройки сохраняются в локальной базе и восстанавливаются при следующем запуске."/><section className="settings-section"><h2>Внешний вид</h2><p>Выберите комфортную тему для вашей мастерской.</p><div className="theme-options"><button className={settings.theme==='dark'?'selected':''} onClick={()=>void update({theme:'dark'})}><div className="theme-preview dark"><i/><i/><i/></div><Moon size={17}/>Тёмная{settings.theme==='dark'&&<Check size={16}/>}</button><button className={settings.theme==='light'?'selected':''} onClick={()=>void update({theme:'light'})}><div className="theme-preview light"><i/><i/><i/></div><Sun size={17}/>Светлая{settings.theme==='light'&&<Check size={16}/>}</button></div></section><section className="settings-section"><h2>Редактор</h2><label className="setting-row"><div><strong>Размер шрифта</strong><p>Monaco Editor · от 12 до 24 px</p></div><select aria-label="Размер шрифта" value={settings.fontSize} onChange={e=>void update({fontSize:Number(e.target.value)})}>{[12,13,14,15,16,18,20,22,24].map(n=><option key={n} value={n}>{n} px</option>)}</select></label><label className="setting-row"><div><strong>Миникарта кода (Minimap)</strong><p>Отображение обзорного эскиза файла справа от кода</p></div><input type="checkbox" checked={!!settings.minimap} onChange={e=>void update({minimap:e.target.checked})}/></label><div className="setting-row"><div><strong>Горячие клавиши</strong><p>Run: Ctrl + Enter · Save: Ctrl + S · Поиск: Ctrl + F · Миникарта в тулбаре</p></div><Code2 size={22}/></div></section><section className="settings-section"><h2>Синхронизация данных</h2><p>Перенос прогресса, черновиков и проектов между IDE и Desktop.</p><div className="setting-row"><div><strong>Резервное копирование и экспорт</strong><p>Экспорт прогресса в файл JSON или импорт с автоматическим созданием резервной копии базы данных</p></div><button className="button primary compact" onClick={()=>setShowSync(true)}><RefreshCw size={14}/>Синхронизация</button></div></section><AISettings/><section className="settings-section"><h2>О приложении</h2><div className="setting-row"><div><strong>DevForge IDE 1.0.0</strong><p>15 языков: Python · SQL (SQLite) · PostgreSQL · HTML/CSS · C · C++ · C# · Objective-C · Rust · 1С:Предприятие · JavaScript · TypeScript · Java · Lua · Assembly (x86-64 NASM) · 3 карьерных трека · IDE + Desktop</p></div><span className="pill available">Local-first</span></div><p className="muted">Лимит выполнения: 5 секунд. Run выполняет активный файл. Python input() открывает окно ввода; время ожидания ответа не входит в лимит выполнения. Для C и Assembly заполните поле «Ввод для программы» перед Run. Поддерживается инспекция регистров x86-64 в реальном времени. Java выполняется во встроенном изолированном Worker. Lua 5.3 работает нативно в Web Worker. Explain Error использует локальный справочник. Кнопка ✦ AI открывает помощника с выбранной локальной моделью.</p></section><SyncModal isOpen={showSync} onClose={()=>setShowSync(false)}/></div>;
}
