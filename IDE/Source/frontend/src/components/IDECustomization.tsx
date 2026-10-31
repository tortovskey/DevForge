import {useEffect,useRef,useState,type ReactNode} from 'react';
import {X,Search,Palette,Code2,PanelsTopLeft,Keyboard,FolderHeart,Braces,Download,Upload,RotateCcw,Check,Plus} from 'lucide-react';
import {useStore} from '../services/store';
import {api} from '../services/api';
import {ACCENTS,COMMANDS,DEFAULT_IDE,LAYOUT_PRESETS,THEMES,bindings,displayKey,keyString,resolveTheme,shortcutErrors,type IDEPreferences,type IDEProfile,type ProfileDocument,type ProfilePreferences,type ColorToken} from '../ide/config';

const TABS=[['appearance','Оформление',Palette],['editor','Редактор',Code2],['layout','Рабочее место',PanelsTopLeft],['keys','Клавиши',Keyboard],['profiles','Профили',FolderHeart],['json','JSON',Braces]] as const;
type Tab=typeof TABS[number][0];
const clone=<T,>(v:T):T=>structuredClone(v);
function snapshot(settings:ReturnType<typeof useStore>['settings']):ProfilePreferences {
  return clone({theme:settings.theme,fontSize:settings.fontSize,minimap:!!settings.minimap,inlineCompletion:settings.inlineCompletion,ide:settings.ide});
}
function download(name:string,text:string){const url=URL.createObjectURL(new Blob([text],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}

export default function IDECustomization({onClose}:{onClose:()=>void}){
  const {settings,updateSettings,notify}=useStore();
  const [draft,setDraft]=useState(()=>snapshot(settings)),[profiles,setProfiles]=useState(()=>clone(settings.ideProfiles));
  const [tab,setTab]=useState<Tab>('appearance'),[query,setQuery]=useState(''),[name,setName]=useState('Мой профиль');
  const [json,setJson]=useState(''),[error,setError]=useState(''),[message,setMessage]=useState(''),[saving,setSaving]=useState(false);
  const dialog=useRef<HTMLDivElement>(null),file=useRef<HTMLInputElement>(null),returnFocus=useRef<HTMLElement|null>(null);
  const invalid=shortcutErrors(draft.ide),theme=resolveTheme(draft.ide,draft.theme);
  const patch=(p:Partial<IDEPreferences>)=>{setDraft(d=>({...d,ide:{...d.ide,...p}}));setMessage('');setError('');};
  const documentFor=(preferences=draft):ProfileDocument=>({format:'devforge.ide-profile',version:1,profile:{id:'shared',name:name.trim()||'DevForge',preferences}});
  useEffect(()=>{
    returnFocus.current=document.activeElement as HTMLElement;
    dialog.current?.querySelector<HTMLInputElement>('input')?.focus();
    return()=>returnFocus.current?.focus();
  },[]);
  function trap(e:React.KeyboardEvent){
    if(e.key==='Escape'){e.preventDefault();e.stopPropagation();if(!saving)onClose();return;}
    if(e.key!=='Tab')return;
    const controls=Array.from(dialog.current?.querySelectorAll<HTMLElement>('button:not(:disabled),input:not(:disabled),select:not(:disabled),textarea:not(:disabled),a[href]')||[]).filter(el=>el.offsetParent!==null);
    const first=controls[0],last=controls.at(-1);
    if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus();}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus();}
  }
  function selectTab(next:Tab){setTab(next);setQuery('');setError('');setMessage('');if(next==='json')setJson(JSON.stringify(documentFor(),null,2));}
  const visible=(text:string)=>!query||text.toLocaleLowerCase().includes(query.toLocaleLowerCase());
  function row(label:string,description:string,control:ReactNode){return visible(label+' '+description)?<label className="ide-pref-row"><span><strong>{label}</strong><small>{description}</small></span>{control}</label>:null;}
  function toggle(key:keyof IDEPreferences,label:string,description:string){return row(label,description,<input type="checkbox" checked={!!draft.ide[key]} onChange={e=>patch({[key]:e.target.checked})}/>);}
  function select(key:keyof IDEPreferences,label:string,description:string,values:readonly (readonly [string,string])[]){return row(label,description,<select value={String(draft.ide[key])} onChange={e=>patch({[key]:key==='tabSize'?Number(e.target.value):e.target.value})}>{values.map(([v,l])=><option key={v} value={v}>{l}</option>)}</select>);}
  async function validate(text:string){
    if(new Blob([text]).size>65536)throw new Error('Профиль должен быть меньше 64 КБ.');
    let parsed:unknown;try{parsed=JSON.parse(text);}catch{throw new Error('Некорректный JSON. Проверьте запятые и кавычки.');}
    try{return await api<ProfileDocument>('/ide/validate-profile','POST',parsed);}
    catch{throw new Error('Профиль не прошёл проверку: проверьте версию, поля, диапазоны и конфликты клавиш.');}
  }
  async function apply(){
    setSaving(true);setError('');setMessage('');
    try{
      const preferences=tab==='json'?(await validate(json)).profile.preferences:draft;
      await updateSettings({...preferences,ideProfiles:profiles});setDraft(preferences);
      setMessage('Настройки применены и сохранены.');notify('Оформление и настройки IDE сохранены');
    }
    catch(e){setError(tab==='json'?(e as Error).message:'Не удалось сохранить настройки. Изменения остались в этом окне — повторите применение.');}
    finally{setSaving(false);}
  }
  function saveProfile(){
    const title=name.trim();if(!title||title.length>60){setError('Введите имя профиля от 1 до 60 символов.');return;}
    const existing=profiles.find(p=>p.name.toLocaleLowerCase()===title.toLocaleLowerCase());
    if(!existing&&profiles.length>=12){setError('Можно сохранить до 12 профилей. Удалите ненужный профиль.');return;}
    const profile:IDEProfile={id:existing?.id||crypto.randomUUID(),name:title,preferences:clone(draft)};
    setProfiles(p=>existing?p.map(x=>x.id===existing.id?profile:x):[...p,profile]);setError('');setMessage('Профиль подготовлен. Нажмите «Применить», чтобы сохранить коллекцию.');
  }
  return <div className="ide-preferences-overlay">
    <div className="ide-preferences" ref={dialog} role="dialog" aria-modal="true" aria-labelledby="ide-pref-title" onKeyDown={trap}>
      <header className="ide-pref-header"><div><span className="ide-eyebrow">DEVFORGE / WORKBENCH</span><h2 id="ide-pref-title">Ваша среда. Ваши правила.</h2><p>Оформление, поведение и привычки — в одном профиле.</p></div><button aria-label="Закрыть настройки IDE" onClick={onClose}><X size={20}/></button></header>
      <fieldset disabled={saving} className="ide-pref-fieldset">
      <div className="ide-pref-body"><nav className="ide-pref-nav" aria-label="Разделы настроек IDE">{TABS.map(([id,label,Icon])=><button key={id} aria-current={tab===id?'page':undefined} onClick={()=>selectTab(id)}><Icon size={17}/>{label}</button>)}<span className="ide-pref-note">Настройки хранятся в вашей учётной записи. Профилем можно поделиться через JSON.</span></nav>
      <main className="ide-pref-main">
        {!['profiles','json'].includes(tab)&&<label className="ide-pref-search"><Search size={15}/><input aria-label="Поиск настроек" placeholder="Найти настройку в этом разделе…" value={query} onChange={e=>setQuery(e.target.value)}/></label>}
        {tab==='appearance'&&<>
          {visible('цветовые темы оформление')&&<section><h3>Цветовая тема</h3><div className="ide-theme-grid">{THEMES.map(t=><button key={t.id} className={draft.ide.theme===t.id?'selected':''} aria-label={`Тема ${t.name}`} aria-pressed={draft.ide.theme===t.id} onClick={()=>{patch({theme:t.id,colors:{}});setDraft(d=>({...d,theme:t.light?'light':'dark'}));}}><span className="ide-theme-preview" style={{background:t.colors.background,color:t.colors.text}}><i style={{background:t.colors.panel,borderColor:t.colors.border}}/><code style={{background:t.colors.editor}}><span style={{color:t.keyword}}>def</span> forge():<br/>&nbsp; <span style={{color:t.keyword}}>return</span> <span style={{color:t.string}}>"hello"</span></code></span><strong>{t.name}{draft.ide.theme===t.id&&<Check size={14}/>}</strong><small>{t.description}</small></button>)}</div>{row('Тема приложения','Использовать общую светлую или тёмную тему.',<input type="checkbox" checked={draft.ide.theme==='inherit'} onChange={e=>patch({theme:e.target.checked?'inherit':theme.id})}/>)}</section>}
          {visible('акцент цвет')&&<section><h3>Акцент</h3><div className="ide-accent-list">{ACCENTS.map(color=><button key={color} aria-label={`Акцент ${color}`} aria-pressed={draft.ide.accent===color} style={{background:color}} onClick={()=>patch({accent:color})}>{draft.ide.accent===color&&<Check size={16}/>}</button>)}<label>Свой цвет<input aria-label="Свой цвет акцента" type="color" value={draft.ide.accent} onChange={e=>patch({accent:e.target.value})}/></label></div></section>}
          {select('density','Плотность интерфейса','Размер вкладок, строк и отступов.',[['compact','Компактная'],['comfortable','Свободная']])}
          {visible('свои цвета палитра токены')&&<details className="ide-color-overrides"><summary>Свои цвета интерфейса</summary><p>Замените отдельные цвета выбранной темы. Выбор другой темы очищает эти замены.</p>{(['background','panel','editor','text','muted','border'] as ColorToken[]).map((key,i)=>row(['Фон окна','Фон панелей','Фон редактора','Текст','Вторичный текст','Границы'][i],'',<span className="ide-color-control"><input type="color" aria-label={`Цвет ${key}`} value={draft.ide.colors[key]||theme.colors[key]} onChange={e=>patch({colors:{...draft.ide.colors,[key]:e.target.value}})}/><button onClick={e=>{e.preventDefault();const colors={...draft.ide.colors};delete colors[key];patch({colors});}}>Сброс</button></span>))}</details>}
        </>}
        {tab==='editor'&&<>
          <h3>Шрифт и набор кода</h3>
          {row('Размер шрифта','От 12 до 24 px.',<input aria-label="Размер шрифта" type="number" min={12} max={24} value={draft.fontSize} onChange={e=>setDraft(d=>({...d,fontSize:Math.min(24,Math.max(12,Number(e.target.value)||12))}))}/>)}
          {select('fontFamily','Шрифт редактора','Если шрифт не установлен, используется Consolas или monospace.',[['cascadia','Cascadia Code'],['consolas','Consolas'],['jetbrains','JetBrains Mono'],['fira','Fira Code'],['monospace','Системный monospace']])}
          {toggle('ligatures','Лигатуры','Объединять символы, если шрифт поддерживает лигатуры.')}
          {row('Межстрочный интервал','От 1.2 до 2.0 высоты шрифта.',<input aria-label="Межстрочный интервал" type="range" min="1.2" max="2" step="0.1" value={draft.ide.lineHeight} onChange={e=>patch({lineHeight:Number(e.target.value)})}/>)}
          {select('tabSize','Ширина табуляции','Применяется к открытым и новым файлам.',[['2','2'],['4','4'],['8','8']])}
          {toggle('insertSpaces','Вставлять пробелы','Клавиша Tab добавляет пробелы вместо символа табуляции.')}
          {select('wordWrap','Перенос строк','Bounded ограничивает длину строки 100 символами.',[['off','Выключен'],['on','По ширине окна'],['bounded','По ширине, до 100 символов']])}
          {select('lineNumbers','Номера строк','Абсолютная или относительная нумерация.',[['on','Обычные'],['relative','Относительные'],['off','Скрыть']])}
          {select('whitespace','Пробельные символы','Когда показывать пробелы и табуляцию.',[['none','Никогда'],['selection','В выделении'],['all','Всегда']])}
          {row('Миникарта','Обзор документа справа.',<input type="checkbox" checked={draft.minimap} onChange={e=>setDraft(d=>({...d,minimap:e.target.checked}))}/>)}
          {row('Умные подсказки','Встроенные предложения продолжения кода.',<input type="checkbox" checked={draft.inlineCompletion} onChange={e=>setDraft(d=>({...d,inlineCompletion:e.target.checked}))}/>)}
          {toggle('bracketColors','Цветные скобки','Выделять вложенные пары скобок.')}
          {toggle('indentGuides','Направляющие отступов','Показывать вложенность блоков.')}
          {toggle('stickyScroll','Закреплённые строки','Оставлять контекст блока в верхней части редактора.')}
          {toggle('smoothScrolling','Плавная прокрутка','Анимировать прокрутку документа.')}
          {select('cursorStyle','Форма курсора','Курсор ввода в редакторе.',[['line','Линия'],['block','Блок'],['underline','Подчёркивание']])}
          {select('cursorBlinking','Мигание курсора','Анимация курсора ввода.',[['smooth','Плавное'],['blink','Обычное'],['solid','Без мигания']])}
        </>}
        {tab==='layout'&&<>
          {visible('готовые раскладки code studio focus')&&<section><h3>Готовые раскладки</h3><div className="ide-layout-presets">{LAYOUT_PRESETS.map(p=><button key={p.id} onClick={()=>patch(p.patch)}><PanelsTopLeft size={25}/><strong>{p.name}</strong><small>{p.description}</small></button>)}</div><p className="ide-pref-hint">Раскладка также выбирает схему клавиш. Тему и код она сохраняет.</p></section>}
          {select('sidebarSide','Боковая панель','Расположение проводника, поиска и структуры.',[['left','Слева'],['right','Справа']])}
          {select('panelPosition','Панель инструментов','Вывод программы, терминал, REPL и проблемы.',[['bottom','Снизу'],['right','Справа']])}
          {row('Ширина боковой панели','Границу панели также можно перетянуть мышью.',<input aria-label="Ширина боковой панели" type="range" min="180" max="480" step="1" value={draft.ide.sidebarWidth} onChange={e=>patch({sidebarWidth:Number(e.target.value)})}/>)}
          {toggle('activityBar','Панель значков','Вертикальная полоса инструментов.')}
          {toggle('statusBar','Строка состояния','Позиция курсора, язык и состояние сохранения.')}
          {toggle('breadcrumbs','Путь к файлу','Путь и контекст над редактором.')}
          {toggle('centered','Центрированный редактор','Ограничить ширину области кода в больших окнах.')}
          <p className="ide-pref-hint">Режим фокуса временно скрывает инструменты. Для возврата нажмите кнопку «Вернуть панели» или F1 → «Режим фокуса».</p>
        </>}
        {tab==='keys'&&<>
          {select('keymap','Схема клавиш','Переход на другую схему сохраняет ваши переопределения.',[['code','VS Code'],['jetbrains','JetBrains']])}
          <p className="ide-pref-hint">Нажмите поле и введите сочетание. × отключает команду, ↺ возвращает стандартное. F1 всегда открывает палитру; в схеме JetBrains работает двойной Shift. Клавиши определяются по физической раскладке.</p>
          <div className="ide-key-list">{COMMANDS.filter(c=>visible(c.label+' '+c.id)).map(c=><div key={c.id}><span>{c.label}<small>{c.id}</small></span><input readOnly aria-label={`Клавиши: ${c.label}`} value={displayKey(bindings(draft.ide)[c.id])} onKeyDown={e=>{if(e.key==='Tab'||e.key==='Escape')return;e.preventDefault();e.stopPropagation();const key=keyString(e.nativeEvent);if(key)patch({shortcuts:{...draft.ide.shortcuts,[c.id]:key}});}}/><button aria-label={`Отключить: ${c.label}`} onClick={()=>patch({shortcuts:{...draft.ide.shortcuts,[c.id]:''}})}><X size={14}/></button><button aria-label={`Сбросить: ${c.label}`} onClick={()=>{const keys={...draft.ide.shortcuts};delete keys[c.id];patch({shortcuts:keys});}}><RotateCcw size={14}/></button></div>)}</div>
        </>}
        {tab==='profiles'&&<>
          <h3>Профили рабочего места</h3><p className="ide-pref-hint">В профиле: тема, цвета, шрифт, поведение редактора, раскладка и клавиши. Коллекция сохраняется кнопкой «Применить».</p>
          <div className="ide-profile-create"><input aria-label="Имя профиля" maxLength={60} value={name} onChange={e=>setName(e.target.value)}/><button onClick={saveProfile} disabled={invalid.length>0}><Plus size={15}/>Сохранить текущий</button></div>
          <div className="ide-profile-list">{profiles.length===0&&<p>Здесь появятся ваши профили. Создайте первый или импортируйте JSON.</p>}{profiles.map(p=><article key={p.id}><div><strong>{p.name}</strong><small>{resolveTheme(p.preferences.ide,p.preferences.theme).name} · {p.preferences.fontSize}px · {p.preferences.ide.keymap==='code'?'VS Code':'JetBrains'}</small></div><button onClick={()=>{setDraft(clone(p.preferences));setName(p.name);setMessage(`Профиль «${p.name}» загружен в настройки. Нажмите «Применить».`);}}>Загрузить</button><button aria-label={`Удалить профиль ${p.name}`} onClick={()=>setProfiles(ps=>ps.filter(x=>x.id!==p.id))}><X size={15}/></button></article>)}</div>
          <div className="ide-profile-tools"><button onClick={()=>download('devforge-profile.json',JSON.stringify(documentFor(),null,2))} disabled={invalid.length>0}><Download size={16}/>Экспорт текущего</button><button onClick={()=>file.current?.click()}><Upload size={16}/>Импорт JSON</button></div>
          <input ref={file} type="file" accept=".json,application/json" hidden onChange={async e=>{const input=e.currentTarget,f=input.files?.[0];if(!f)return;setSaving(true);setError('');try{if(f.size>65536)throw new Error('Профиль должен быть меньше 64 КБ.');const doc=await validate(await f.text());setDraft(doc.profile.preferences);setName(doc.profile.name);setMessage('Профиль проверен и загружен. Его можно добавить в коллекцию или применить.');}catch(e){setError(String((e as Error).message));}finally{input.value='';setSaving(false);}}}/>
          <p className="ide-pref-hint">Экспорт содержит только настройки IDE. Объём импорта — до 64 КБ; неизвестные поля и конфликты клавиш отклоняются.</p>
        </>}
        {tab==='json'&&<>
          <h3>Настройки как данные</h3><p className="ide-pref-hint">Открытый формат devforge.ide-profile, версия 1. Измените JSON, проверьте его и примените настройки. Шаблоны и схемы описаны в документации исходников.</p>
          <textarea className="ide-json-editor" aria-label="JSON профиля IDE" spellCheck={false} value={json} onChange={e=>setJson(e.target.value)}/>
          <div className="ide-profile-tools"><button onClick={async()=>{setSaving(true);setError('');try{const doc=await validate(json);setDraft(doc.profile.preferences);setName(doc.profile.name);setJson(JSON.stringify(doc,null,2));setMessage('JSON корректен и загружен в настройки. Нажмите «Применить».');}catch(e){setError((e as Error).message);}finally{setSaving(false);}}}><Check size={16}/>Проверить и загрузить JSON</button><button onClick={async()=>{try{const schema=await api('/ide/profile-schema');download('devforge-profile.schema.json',JSON.stringify(schema,null,2));}catch{setError('Не удалось загрузить схему.');}}}><Download size={16}/>Скачать JSON Schema</button></div>
        </>}
      </main></div>
      </fieldset>
      <div className="ide-pref-feedback" aria-live="polite">{(error||invalid.length>0)&&<p role="alert">{error||invalid.join(' ')}</p>}{message&&<p className="success">{message}</p>}</div>
      <footer className="ide-pref-footer"><button disabled={saving} onClick={()=>{setDraft({theme:'dark',fontSize:14,minimap:false,inlineCompletion:true,ide:clone(DEFAULT_IDE)});setError('');setMessage('Стандартные настройки подготовлены. Коллекция профилей сохранится.');if(tab==='json')setJson(JSON.stringify(documentFor({theme:'dark',fontSize:14,minimap:false,inlineCompletion:true,ide:clone(DEFAULT_IDE)}),null,2));}}><RotateCcw size={14}/>Сброс настроек</button><div><button onClick={onClose} disabled={saving}>Закрыть</button><button className="ide-apply" onClick={()=>void apply()} disabled={saving||(invalid.length>0&&tab!=='json')}>{saving?'Сохранение…':'Применить'}</button></div></footer>
    </div>
  </div>;
}
