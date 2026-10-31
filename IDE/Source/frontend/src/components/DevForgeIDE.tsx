import {lazy,Suspense,useEffect,useRef,useState} from 'react';
import {
  Files,Search,ListTree,Database,Send,GitBranch,Play,Square,RotateCcw,Save,
  Map,Settings,Terminal,AlertCircle,CheckCircle2,Plus,Trash2,Edit3,
  Maximize2,Minimize2,ChevronRight,ChevronDown,Code2,Command,Sparkles,
  Laptop,Globe,RefreshCw,FileCode2,X,Copy,Check,Columns,FolderPlus,
  Split,History,ListTodo,CheckSquare,Bug,AlignLeft,FileText,Sliders,
  Download,Upload,Folder,File
} from 'lucide-react';
const CodeEditor = lazy(() => import('./CodeEditor'));
import Output from './Output';
import {BrowserRunner, getRunner} from '../runners/runner';
import {checkHtml,documentSource} from '../runners/html';
import AIHelp from './AIHelp';
import {LANGUAGE_NAMES, EXTENSIONS} from '../types';
import {api} from '../services/api';
import {useStore} from '../services/store';
import {PlatformAdapter} from '../services/platform';
import type {Project, RunResult} from '../types';
import {ForgeIcon} from './ForgeIcon';
import IDECustomization from './IDECustomization';
import IDEResizer from './IDEResizer';
import {COMMANDS,bindings,displayKey,keyString,resolveTheme,workbenchStyle,type CommandId,type IDEPreferences} from '../ide/config';
const editorLanguage=(name:string)=>({py:'python',ts:'typescript',js:'javascript',html:'html',css:'css',sql:'sql',c:'c',h:'c',cpp:'cpp',hpp:'cpp',cc:'cpp',cxx:'cpp',cs:'csharp',m:'objective-c',rs:'rust',java:'java',lua:'lua',md:'markdown',json:'json',txt:'plaintext',asm:'assembly',s:'assembly',bsl:'1c'}[name.split('.').pop()?.toLowerCase()||'']||'plaintext');

interface SymbolItem {
  name: string;
  kind: 'class' | 'function' | 'route' | 'variable';
  line: number;
}

interface SearchMatch {
  file: string;
  fileIndex: number;
  line: number;
  text: string;
}

interface TodoItem {
  file: string;
  fileIndex: number;
  line: number;
  type: 'TODO' | 'FIXME' | 'NOTE' | 'BUG';
  text: string;
}

interface GitCommit {
  hash: string;
  message: string;
  author: string;
  timestamp: string;
  filesCount: number;
  files?: {name:string;content:string}[];
}

interface VariableInspection {
  name: string;
  type: string;
  value: string;
}

interface ProblemItem {
  severity: 'error' | 'warning' | 'info';
  file: string;
  line: number;
  col: number;
  message: string;
}

export default function DevForgeIDE({projectId}: {projectId?: string}) {
  const {settings, updateSettings, updateIDE, notify, account} = useStore();
  const [preferencesOpen,setPreferencesOpen]=useState(false),[zen,setZen]=useState(false);
  const [hiddenTabs,setHiddenTabs]=useState<string[]>([]);
  const [sizeDraft,setSizeDraft]=useState<Partial<IDEPreferences>>({});
  const workbenchRef=useRef<HTMLDivElement>(null);
  const prefs={...settings.ide,...sizeDraft},keys=bindings(prefs);
  const commandRef=useRef<(id:CommandId)=>void>(()=>{});
  function resize(key:'sidebarWidth'|'panelHeight'|'panelWidth',value:number){
    setSizeDraft(d=>({...d,[key]:value}));
    void updateIDE({[key]:value}).then(()=>setSizeDraft(d=>{const next={...d};if(next[key]===value)delete next[key];return next;})).catch(()=>{setSizeDraft({});notify('Не удалось сохранить размер панели');});
  }
  const [project, setProject] = useState<Project | null>(null);
  const [activeFileIndex, setActiveFileIndex] = useState(0);

  // Split Editor Pane 2 state
  const [isSplit, setIsSplit] = useState(false);
  const [splitFileIndex, setSplitFileIndex] = useState(1);

  // Diff Editor state
  const [isDiffMode, setIsDiffMode] = useState(false);

  // Multi-file Workspace (Modular Project Architecture)
  const [files, setFiles] = useState<{name: string; content: string; baseline?: string}[]>([
    {
      name: 'main.py',
      baseline: '',
      content: (
        'from fastapi import FastAPI, HTTPException, status, Depends\n' +
        'from pydantic import BaseModel, Field\n' +
        'from models import Item, ItemCreate, ItemResponse\n' +
        'from database import get_db, init_db\n\n' +
        'app = FastAPI(title="DevForge REST Service", version="1.0.0")\n\n' +
        '# TODO: Добавить эндпоинт для пагинации списка товаров\n' +
        '# NOTE: База данных инициализируется при старте\n' +
        '@app.on_event("startup")\n' +
        'def on_startup():\n' +
        '    init_db()\n' +
        '    print("DevForge REST Service успешно запущен.")\n\n' +
        '@app.get("/")\n' +
        'def read_root():\n' +
        '    return {"service": "DevForge IDE API", "status": "online", "version": "1.0.0"}\n\n' +
        '@app.get("/items", response_model=list[ItemResponse])\n' +
        'def list_items(db=Depends(get_db)):\n' +
        '    return db.query_all()\n\n' +
        '@app.get("/items/{item_id}", response_model=ItemResponse)\n' +
        'def get_item(item_id: int, db=Depends(get_db)):\n' +
        '    item = db.find_by_id(item_id)\n' +
        '    if not item:\n' +
        '        raise HTTPException(status_code=404, detail="Товар не найден")\n' +
        '    return item\n\n' +
        '@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)\n' +
        'def create_item(payload: ItemCreate, db=Depends(get_db)):\n' +
        '    # FIXME: добавить проверку на дубликаты названий\n' +
        '    return db.insert(payload.model_dump())\n\n' +
        'if __name__ == "__main__":\n' +
        '    print("DevForge IDE — среда разработки готова.")\n' +
        '    print("Отправьте тестовый запрос в REST API Client слева!")\n'
      )
    },
    {
      name: 'models.py',
      baseline: '',
      content: (
        'from pydantic import BaseModel, Field\n' +
        'from typing import Optional\n\n' +
        'class ItemBase(BaseModel):\n' +
        '    name: str = Field(min_length=2, max_length=100, description="Название товара")\n' +
        '    price: float = Field(ge=0.0, description="Цена в рублях")\n' +
        '    description: Optional[str] = Field(default="", description="Описание")\n\n' +
        'class ItemCreate(ItemBase):\n' +
        '    pass\n\n' +
        'class ItemResponse(ItemBase):\n' +
        '    id: int\n' +
        '    in_stock: bool = True\n'
      )
    },
    {
      name: 'database.py',
      baseline: '',
      content: (
        'class InMemoryDatabase:\n' +
        '    def __init__(self):\n' +
        '        self._data = {\n' +
        '            1: {"id": 1, "name": "Ноутбук DevForge", "price": 64990.0, "description": "16GB RAM, 512GB SSD", "in_stock": True},\n' +
        '            2: {"id": 2, "name": "Механическая клавиатура", "price": 8490.0, "description": "Gateron Brown", "in_stock": True}\n' +
        '        }\n\n' +
        '    def query_all(self):\n' +
        '        return list(self._data.values())\n\n' +
        '    def find_by_id(self, item_id: int):\n' +
        '        return self._data.get(item_id)\n\n' +
        '    def insert(self, item_data: dict):\n' +
        '        new_id = max(self._data.keys(), default=0) + 1\n' +
        '        item_data["id"] = new_id\n' +
        '        item_data["in_stock"] = True\n' +
        '        self._data[new_id] = item_data\n' +
        '        return item_data\n\n' +
        'DB_INSTANCE = InMemoryDatabase()\n\n' +
        'def get_db():\n' +
        '    return DB_INSTANCE\n\n' +
        'def init_db():\n' +
        '    print("Таблицы и индексы базы данных инициализированы.")\n'
      )
    },
    {
      name: 'test_api.py',
      baseline: '',
      content: (
        'from database import InMemoryDatabase\n\n' +
        'def test_database_insert():\n' +
        '    db = InMemoryDatabase()\n' +
        '    created = db.insert({"name": "Тестовый товар", "price": 100.0, "description": "Test"})\n' +
        '    assert created["id"] == 3\n' +
        '    assert db.find_by_id(3)["name"] == "Тестовый товар"\n' +
        '    print("Тест test_database_insert пройден успешно!")\n\n' +
        'if __name__ == "__main__":\n' +
        '    test_database_insert()\n'
      )
    },
    {
      name: 'README.md',
      baseline: '',
      content: (
        '# DevForge IDE Project\n\n' +
        'Профессиональный микросервис, созданный в **DevForge IDE 1.0.0**.\n\n' +
        '## Возможности среды:\n' +
        '- **VS Code Activity Bar**: Проводник, Поиск/Замена, Git, AST Outline, DataGrip DB, REST API, TODO, Settings.\n' +
        '- **PyCharm Run Configurations**: Быстрый запуск, отладка, интерактивная REPL консоль с инспектором переменных.\n' +
        '- **Split Editor**: Параллельное редактирование двух файлов (`main.py` и `models.py`).\n' +
        '- **Diff Viewer**: Сравнение локальных изменений с оригиналом.\n'
      )
    }
  ]);

  const [loading, setLoading] = useState(true);
  const [dirty, setDirty] = useState(false);
  const [saveState, setSaveState] = useState('Сохранено');
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState('Готово');
  const [result, setResult] = useState<RunResult | null>(null);
  const [stdin, setStdin] = useState('');

  // Cursor coordinates
  const [cursorPos, setCursorPos] = useState({line: 1, col: 1});

  // VS Code Activity Bar tool windows
  const [activeTool, setActiveTool] = useState<'explorer' | 'search' | 'git' | 'structure' | 'database' | 'api' | 'todo' | 'debug' | 'settings' | null>('explorer');
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Bottom Tool Window state
  const [bottomTab, setBottomTab] = useState<'output' | 'terminal' | 'repl' | 'problems' | 'database' | 'api' | 'stdin'>('output');
  const [bottomOpen, setBottomOpen] = useState(true);
  const [bottomMaximized, setBottomMaximized] = useState(false);

  // Search Everywhere Modal (Double Shift / Ctrl+P / Ctrl+Shift+P)
  const [searchEverywhereOpen, setSearchEverywhereOpen] = useState(false);
  const [searchEverywhereTab, setSearchEverywhereTab] = useState<'all' | 'files' | 'actions' | 'symbols'>('all');
  const [searchEverywhereQuery, setSearchEverywhereQuery] = useState('');
  const [paletteIndex,setPaletteIndex]=useState(0);
  const paletteList=useRef<HTMLDivElement>(null);
  useEffect(()=>setPaletteIndex(0),[searchEverywhereQuery,searchEverywhereTab]);
  useEffect(()=>{paletteList.current?.querySelector('[aria-selected="true"]')?.scrollIntoView({block:'nearest'});},[paletteIndex]);

  // Global Search & Replace Tool state
  const [searchQuery, setSearchQuery] = useState('');
  const [replaceQuery, setReplaceQuery] = useState('');
  const [isRegex, setIsRegex] = useState(false);
  const [isCaseSensitive, setIsCaseSensitive] = useState(false);
  const [isWholeWord, setIsWholeWord] = useState(false);
  const [searchMatches, setSearchMatches] = useState<SearchMatch[]>([]);

  // Database Tool state (DataGrip style)
  const [sqlQuery, setSqlQuery] = useState('SELECT id, name, price, description, in_stock FROM items ORDER BY id ASC;');
  const [sqlResult, setSqlResult] = useState<{headers: string[]; rows: any[][]} | null>({
    headers: ['id', 'name', 'price', 'description', 'in_stock'],
    rows: [
      [1, 'Ноутбук DevForge', 64990.0, '16GB RAM, 512GB SSD', 'true'],
      [2, 'Механическая клавиатура', 8490.0, 'Gateron Brown', 'true'],
      [3, 'UltraWide Монитор 34"', 37990.0, '144Hz IPS 3440x1440', 'true'],
      [4, 'Эргономичная мышь', 5290.0, 'Беспроводная 2.4GHz', 'false']
    ]
  });

  // REST API Client Tool state
  const [apiMethod, setApiMethod] = useState<'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'>('GET');
  const [apiUrl, setApiUrl] = useState('/api/platform');
  const [apiHeaders, setApiHeaders] = useState('Content-Type: application/json\nAccept: application/json');
  const [apiBody, setApiBody] = useState('{\n  "name": "Новый товар",\n  "price": 12500.0,\n  "description": "Создано через REST Client"\n}');
  const [apiResponse, setApiResponse] = useState<{status: number; statusText: string; timeMs: number; sizeBytes: number; data: any} | null>(null);
  const [apiSending, setApiSending] = useState(false);
  const [apiHistory, setApiHistory] = useState<{method: string; url: string; time: string}[]>([
    {method: 'GET', url: '/api/platform', time: '14:30:12'},
    {method: 'POST', url: '/items', time: '14:32:05'}
  ]);

  // Terminal State (Interactive Shell)
  const [terminalHistory, setTerminalHistory] = useState<string[]>([
    'DevForge IDE Terminal [Version 1.0.0 Windows x64]',
    'Type "help" to view built-in commands or "run" to execute current project.',
    ''
  ]);
  const [terminalInput, setTerminalInput] = useState('');
  const [terminalCommandIndex, setTerminalCommandIndex] = useState(-1);
  const [pastCommands, setPastCommands] = useState<string[]>([]);

  // Python REPL State & Variables Inspector (PyCharm Style)
  const [replHistory, setReplHistory] = useState<{input: string; output: string}[]>([]);
  const [replInput, setReplInput] = useState('');
  const [variables, setVariables] = useState<VariableInspection[]>([]);
  const replRunner=useRef<BrowserRunner|null>(null),replBusy=useRef(false);
  useEffect(()=>()=>replRunner.current?.reset(),[]);

  // Git State
  const [gitCommits, setGitCommits] = useState<GitCommit[]>(()=>{try{return JSON.parse(localStorage.getItem(`snapshots:${account.id}:${projectId||'scratch'}`)||'[]');}catch{return [];}});
  const [commitMessage, setCommitMessage] = useState('');

  // Run/Debug Configuration
  const [runConfig, setRunConfig] = useState<'active' | 'main' | 'test'>('active');
  const [cliArgs, setCliArgs] = useState('--port 8766 --reload');
  const [envVars, setEnvVars] = useState('DEVFORGE_ENV=development\nDEBUG=1');

  // AI Assistant Drawer
  const [showAI, setShowAI] = useState(false);

  // Monaco Editor Ref
  const editorRef = useRef<any>(null);
  const runner = useRef<BrowserRunner | null>(null);
  const editVersion = useRef(0);
  const alive = useRef(true);
  const filesRef=useRef(files);filesRef.current=files;
  const saving = useRef(false);
  const [inputPrompt,setInputPrompt]=useState<string|null>(null),[inputValue,setInputValue]=useState('');
  const [htmlPreview,setHtmlPreview]=useState('');
  const [loadError,setLoadError]=useState('');
  const inputResolve=useRef<((value:string|null)=>void)|null>(null);
  const scratchKey=`scratch:${account.id}:ide_files`;
  const cacheKey=projectId?`project:${account.id}:${projectId}:ide_files`:scratchKey;
  function cacheFiles(next:typeof files){try{localStorage.setItem(cacheKey,JSON.stringify({revision:project?.revision,files:next}));}catch{notify('Недостаточно места для черновика. Сохраните проект или экспортируйте файлы.');}}
  function changeFiles(next:typeof files){editVersion.current++;setFiles(next);setDirty(true);setSaveState('Не сохранено');cacheFiles(next);}
  function validName(name:string,index=-1){return /^[\w-][\w. -]*\.(py|sql|html|css|c|h|js|ts|java|cpp|hpp|cc|cxx|cs|m|rs|bsl|lua|asm|s|inc|md|txt|json)$/u.test(name)&&!name.includes('..')&&!files.some((f,i)=>i!==index&&f.name.toLowerCase()===name.toLowerCase());}

  const activeFile = files[activeFileIndex] || files[0] || {name: 'main.py', content: ''};
  const splitFile = files[splitFileIndex] || files[1] || files[0];
  const extension = activeFile.name.split('.').pop()?.toLowerCase() || '';

  // Determine language from extension
  const detectedLanguage = (
    extension === 'py' ? 'python' :
    extension === 'ts' ? 'typescript' :
    extension === 'js' ? 'javascript' :
    extension === 'c' || extension === 'h' ? 'c' :
    extension === 'cpp' || extension === 'hpp' || extension === 'cc' ? 'cpp' :
    extension === 'cs' ? 'csharp' :
    extension === 'm' ? 'objc' :
    extension === 'rs' ? 'rust' :
    extension === 'bsl' ? '1c' :
    extension === 'java' ? 'java' :
    extension === 'lua' ? 'lua' :
    extension === 'asm' || extension === 's' ? 'assembly' :
    extension === 'sql' ? (project?.language==='postgresql'?'postgresql':'sql') :
    extension === 'html' ? 'html-css' :
    extension === 'css' ? 'html-css' : 'python'
  );

  // Initialize runner
  useEffect(() => {
    if(detectedLanguage==='html-css'){runner.current=null;return;}
    const current=getRunner(detectedLanguage,setStatus);runner.current=current;
    current.onInputRequest=prompt=>new Promise(resolve=>{inputResolve.current=resolve;setInputValue('');setInputPrompt(prompt.trim()||'Введите строку');});
    current.onInputCancel=()=>{inputResolve.current?.(null);inputResolve.current=null;setInputPrompt(null);};
    void current.warm().catch(e => notify(String(e)));
    return () => {
      current.stop();current.onStatus=()=>{};current.onInputRequest=async()=>null;current.onInputCancel=()=>{};
    };
  }, [detectedLanguage]);

  // Load project or restore cached files
  useEffect(() => {
    alive.current = true;
    (async () => {
      if (projectId) {
        try {
          const saved = await api<Project>(`/projects/${projectId}`);
          if (!alive.current) return;
          setProject(saved);
          if (saved.files && saved.files.length > 0) {
            const cached=localStorage.getItem(cacheKey);let recovered=null;
            try{const value=cached?JSON.parse(cached):null;if(value?.revision===saved.revision&&validCachedFiles(value.files))recovered=value.files;}catch{}
            setFiles(recovered||saved.files.map(f => ({...f, baseline: f.content})));
            if(recovered){setDirty(true);setSaveState('Восстановлен черновик');}
          }
        } catch (e) {
          setLoadError(String(e));
          notify(`Не удалось загрузить проект: ${String(e)}`);
        }
      } else {
        const cached = localStorage.getItem(`scratch:${account.id}:ide_files`);
        if (cached) {
          try {
            const value=JSON.parse(cached),parsed=Array.isArray(value)?value:value.files;
            if (validCachedFiles(parsed)) {
              setFiles(parsed.map((f:typeof files[number]) => ({...f, baseline: f.baseline ?? f.content})));
            }
          } catch (_) {}
        } else {
          // Initialize baselines
          setFiles(prev => prev.map(f => ({...f, baseline: f.content})));
        }
      }
      if(alive.current)setLoading(false);
    })();
    return () => { alive.current = false; };
  }, [projectId]);

  function validCachedFiles(value:unknown):value is typeof files{return Array.isArray(value)&&value.length>0&&value.length<=30&&value.every(f=>f&&typeof f.name==='string'&&typeof f.content==='string'&&f.content.length<=200000);}
  useEffect(()=>{const handler=(e:BeforeUnloadEvent)=>{if(dirty){e.preventDefault();e.returnValue='';}};window.addEventListener('beforeunload',handler);return()=>window.removeEventListener('beforeunload',handler);},[dirty]);
  // Code update handler
  function updateCode(newCode: string, targetIndex = activeFileIndex) {
    const nextFiles = files.map((f, i) => i === targetIndex ? {...f, content: newCode} : f);
    changeFiles(nextFiles);
  }

  // Save Project
  async function saveProject() {
    if(saving.current||loadError)return;saving.current=true;
    const version=editVersion.current;
    try {
      setSaveState('Сохранение…');
      if (project && projectId) {
        const updated = await api<Project>(`/projects/${projectId}`, 'PUT', {
          name: project.name,
          language: project.language,
          revision: project.revision,
          files: files.map(f => ({name: f.name, content: f.content}))
        });
        setProject(updated);
        if(version!==editVersion.current)localStorage.setItem(cacheKey,JSON.stringify({revision:updated.revision,files:filesRef.current}));
      } else {
        cacheFiles(files);
      }
      // Update baselines
      if(version===editVersion.current){setFiles(prev => prev.map(f => ({...f, baseline: f.content})));setDirty(false);setSaveState('Сохранено');if(projectId)localStorage.removeItem(cacheKey);}
      else setSaveState('Есть новые изменения');
      notify('Все файлы успешно сохранены');
    } catch (e) {
      setSaveState('Ошибка сохранения');
      notify(String(e));
    } finally {saving.current=false;}
  }

  // Run execution
  async function runCode() {
    if (busy || (!runner.current&&detectedLanguage!=='html-css') || loadError || ['md','txt','json'].includes(extension)) return;
    setBusy(true);
    setStatus(`Выполнение ${activeFile.name}…`);
    setBottomTab('output');
    setBottomOpen(true);
    try {
      const source=detectedLanguage==='html-css'?documentSource(activeFile.content,files,activeFile.name):'';
      if(source)setHtmlPreview(source);
      const resp = source?await checkHtml(source,[]):await runner.current!.run({
        code: activeFile.content,
        stdin,
        files: files.map(f => ({name: f.name, content: f.content})),
        filename: activeFile.name,
        context: projectId || 'devforge-ide'
      });
      if (alive.current) {
        setResult(resp);
      }
    } catch (e) {
      notify(`Ошибка запуска: ${String(e)}`);
    } finally {
      if (alive.current) {
        setBusy(false);
        setStatus('Готово');
      }
    }
  }

  // Format Code (Ctrl+Alt+L / Shift+Alt+F)
  function formatDocument() {
    const action=editorRef.current?.getAction('editor.action.formatDocument');
    if(!action?.isSupported()){notify('Для этого языка форматтер пока не подключён');return;}
    void action.run().catch(()=>notify('Не удалось отформатировать документ'));
  }

  // Commands and the palette share one binding registry. Capture before Monaco.
  commandRef.current=(id:CommandId)=>{
    switch(id){
      case 'run': void runCode();break;
      case 'save': void saveProject();break;
      case 'format': formatDocument();break;
      case 'split': setIsSplit(v=>!v);break;
      case 'palette':setSearchEverywhereTab('actions');setSearchEverywhereQuery('');setSearchEverywhereOpen(true);break;
      case 'files':setSearchEverywhereTab('files');setSearchEverywhereQuery('');setSearchEverywhereOpen(true);break;
      case 'search':setZen(false);setActiveTool('search');setSidebarOpen(true);break;
      case 'terminal':setZen(false);setBottomTab('terminal');setBottomOpen(true);break;
      case 'sidebar':setZen(false);setActiveTool(t=>t||'explorer');setSidebarOpen(v=>!v);break;
      case 'panel':setZen(false);setBottomOpen(v=>!v);break;
      case 'settings':setPreferencesOpen(true);break;
      case 'zen':setZen(v=>!v);break;
      case 'previousTab':case 'nextTab':{
        const indices=files.map((f,i)=>hiddenTabs.includes(f.name)?-1:i).filter(i=>i>=0),pos=indices.indexOf(activeFileIndex);
        setActiveFileIndex(indices[(pos+(id==='nextTab'?1:-1)+indices.length)%indices.length]??0);break;
      }
    }
  };
  useEffect(()=>{
    let lastShift=0;
    const down=(e:KeyboardEvent)=>{
      if(e.isComposing||e.repeat||preferencesOpen||inputPrompt!==null)return;
      if(searchEverywhereOpen){if(e.key==='Escape'){e.preventDefault();setSearchEverywhereOpen(false);editorRef.current?.focus();}return;}
      if(e.code==='ShiftLeft'||e.code==='ShiftRight'){
        if(prefs.keymap==='jetbrains'&&!e.ctrlKey&&!e.altKey&&!e.metaKey){const now=Date.now();if(now-lastShift<300){commandRef.current('files');lastShift=0;}else lastShift=now;}return;
      }
      lastShift=0;
      const key=keyString(e),id=COMMANDS.find(c=>keys[c.id]&&keys[c.id]===key)?.id;
      if(id||e.code==='F1'){e.preventDefault();e.stopPropagation();commandRef.current(id||'palette');}
      else if(e.code==='Escape'&&zen){e.preventDefault();setZen(false);}
    };
    window.addEventListener('keydown',down,true);
    return()=>window.removeEventListener('keydown',down,true);
  },[settings.ide,preferencesOpen,searchEverywhereOpen,inputPrompt,zen]);
  useEffect(()=>{setHiddenTabs([]);},[projectId]);
  useEffect(()=>{setHiddenTabs(v=>v.includes(activeFile.name)?v.filter(n=>n!==activeFile.name):v);},[activeFile.name]);
  function closeTab(index:number){
    const remaining=files.map((f,i)=>!hiddenTabs.includes(f.name)&&i!==index?i:-1).filter(i=>i>=0);
    if(!remaining.length){notify('Последняя вкладка остаётся открытой. Файлы удаляются отдельно в проводнике.');return;}
    setHiddenTabs(v=>[...v,files[index].name]);
    if(index===activeFileIndex)setActiveFileIndex(remaining.find(i=>i>index)??remaining[remaining.length-1]);
  }
  const mountEditor=(editor:any)=>{editorRef.current=editor;editor.onDidFocusEditorText(()=>{editorRef.current=editor;});};

  // Parse Structure (AST Outline - PyCharm signature feature)
  const symbols: SymbolItem[] = [];
  const lines = activeFile.content.split('\n');
  lines.forEach((line, idx) => {
    const trimmed = line.trim();
    // Classes
    const classMatch = trimmed.match(/^class\s+([A-Za-z0-9_]+)/);
    if (classMatch) {
      symbols.push({name: classMatch[1], kind: 'class', line: idx + 1});
      return;
    }
    // FastAPI routes: @app.get("/items")
    const routeMatch = trimmed.match(/^@app\.(get|post|put|delete|patch)\(['"]([^'"]+)['"]/);
    if (routeMatch) {
      symbols.push({name: `${routeMatch[1].toUpperCase()} ${routeMatch[2]}`, kind: 'route', line: idx + 1});
      return;
    }
    // Functions
    const funcMatch = trimmed.match(/^(?:async\s+)?def\s+([A-Za-z0-9_]+)/);
    if (funcMatch) {
      symbols.push({name: funcMatch[1], kind: 'function', line: idx + 1});
      return;
    }
    // Constants
    const constMatch = trimmed.match(/^([A-Z0-9_]{3,})\s*=/);
    if (constMatch) {
      symbols.push({name: constMatch[1], kind: 'variable', line: idx + 1});
    }
  });

  // Parse TODOs & FIXMEs across all workspace files (PyCharm TODO window)
  const todos: TodoItem[] = [];
  files.forEach((file, fIdx) => {
    file.content.split('\n').forEach((l, lIdx) => {
      const match = l.match(/#\s*(TODO|FIXME|NOTE|BUG):\s*(.+)$/i);
      if (match) {
        todos.push({
          file: file.name,
          fileIndex: fIdx,
          line: lIdx + 1,
          type: match[1].toUpperCase() as any,
          text: match[2].trim()
        });
      }
    });
  });

  // Diagnostics & Problems parser
  const problems: ProblemItem[] = [];
  lines.forEach((line, idx) => {
    if (line.includes('FIXME:')) {
      problems.push({
        severity: 'warning',
        file: activeFile.name,
        line: idx + 1,
        col: line.indexOf('FIXME:') + 1,
        message: line.split('FIXME:')[1].trim()
      });
    }
    if (line.includes('eval(')) {
      problems.push({
        severity: 'warning',
        file: activeFile.name,
        line: idx + 1,
        col: line.indexOf('eval(') + 1,
        message: 'Использование eval() потенциально небезопасно'
      });
    }
  });

  // Global Search in Files
  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchMatches([]);
      return;
    }
    const matches: SearchMatch[] = [];
    files.forEach((f, fIdx) => {
      f.content.split('\n').forEach((l, lIdx) => {
        let matched = false;
        if (isRegex) {
          try {
            const re = new RegExp(searchQuery, isCaseSensitive ? '' : 'i');
            matched = re.test(l);
          } catch (_) {}
        } else {
          const hay = isCaseSensitive ? l : l.toLowerCase();
          const needle = isCaseSensitive ? searchQuery : searchQuery.toLowerCase();
          matched = isWholeWord ? new RegExp(`\\b${needle}\\b`, isCaseSensitive ? '' : 'i').test(l) : hay.includes(needle);
        }
        if (matched) {
          matches.push({
            file: f.name,
            fileIndex: fIdx,
            line: lIdx + 1,
            text: l.trim()
          });
        }
      });
    });
    setSearchMatches(matches.slice(0, 50));
  }, [searchQuery, files, isRegex, isCaseSensitive, isWholeWord]);

  // Replace in files
  function handleReplaceAll() {
    if (!searchQuery) return;
    let totalReplaced = 0;
    const nextFiles = files.map(f => {
      let content = f.content;
      if (isRegex) {
        try {
          const re = new RegExp(searchQuery, isCaseSensitive ? 'g' : 'gi');
          content = content.replace(re, replaceQuery);
        } catch (_) {}
      } else {
        const re = new RegExp(searchQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), isCaseSensitive ? 'g' : 'gi');
        content = content.replace(re, replaceQuery);
      }
      return {...f, content};
    });
    changeFiles(nextFiles);
    notify(`Замена выполнена во всех файлах проекта`);
  }

  // Execute API Request (Thunder Client / PyCharm HTTP)
  async function sendApiRequest() {
    setApiSending(true);
    setBottomTab('api');
    setBottomOpen(true);
    const start = performance.now();
    try {
      const targetUrl = apiUrl.startsWith('http') ? apiUrl : `${window.location.origin}${apiUrl}`;
      const headersObj: Record<string, string> = {};
      apiHeaders.split('\n').forEach(line => {
        const [k, v] = line.split(':').map(s => s.trim());
        if (k && v) headersObj[k] = v;
      });

      const options: RequestInit = {
        method: apiMethod,
        headers: headersObj
      };
      if (['POST', 'PUT', 'PATCH'].includes(apiMethod) && apiBody.trim()) {
        options.body = apiBody;
      }
      const resp = await fetch(targetUrl, options);
      const timeMs = Math.round(performance.now() - start);
      let data: any;
      const text = await resp.text();
      try {
        data = JSON.parse(text);
      } catch (_) {
        data = text;
      }
      setApiResponse({
        status: resp.status,
        statusText: resp.statusText || (resp.ok ? 'OK' : 'Error'),
        timeMs,
        sizeBytes: text.length,
        data
      });
      // Append to history
      setApiHistory(prev => [{method: apiMethod, url: apiUrl, time: new Date().toLocaleTimeString()}, ...prev.slice(0, 9)]);
    } catch (e) {
      setApiResponse({
        status: 0,
        statusText: 'Network Failure',
        timeMs: Math.round(performance.now() - start),
        sizeBytes: 0,
        data: {error: String(e)}
      });
    } finally {
      setApiSending(false);
    }
  }

  // Interactive Terminal Command Execution
  function handleTerminalSubmit(e: React.FormEvent) {
    e.preventDefault();
    const cmd = terminalInput.trim();
    if (!cmd) return;

    setPastCommands(prev => [...prev, cmd]);
    setTerminalCommandIndex(-1);
    setTerminalInput('');

    const newLogs = [...terminalHistory, `devforge$ ${cmd}`];
    const parts = cmd.split(' ');
    const command = parts[0].toLowerCase();
    const arg = parts.slice(1).join(' ');

    switch (command) {
      case 'help':
        newLogs.push(
          'Доступные команды:',
          '  run [файл]        - Выполнить указанный файл или активный файл',
          '  ls                - Список файлов в проекте',
          '  cat <файл>        - Просмотреть содержимое файла',
          '  clear             - Очистить терминал',
          '  pwd               - Текущая директория проекта',
          '  git status        - Статус рабочей копии',
          '  pip list          - Список предустановленных пакетов',
          '  echo <текст>      - Вывести строку'
        );
        break;
      case 'clear':
        setTerminalHistory([]);
        return;
      case 'ls':
        newLogs.push(files.map(f => `${f.name} (${f.content.length} bytes)`).join('\n'));
        break;
      case 'pwd':
        newLogs.push(`C:\\DevForge\\Projects\\${project?.name || 'Workspace'}`);
        break;
      case 'pip':
        if (arg === 'list') {
          newLogs.push(
            'Package    Version\n---------- -------\nfastapi    0.115.0\npydantic   2.9.2\npytest     8.3.3\nsqlite3    3.45.1\nuvicorn    0.31.0'
          );
        } else {
          newLogs.push(`pip: выполнено: ${arg}`);
        }
        break;
      case 'git':
        if (arg === 'status') {
          newLogs.push(`On branch main\nChanges to be committed: ${dirty ? activeFile.name : 'none'}`);
        } else {
          newLogs.push(`git: команда ${arg} обработана.`);
        }
        break;
      case 'cat':
        const target = files.find(f => f.name.toLowerCase() === arg.toLowerCase());
        if (target) {
          newLogs.push(target.content.slice(0, 1000));
        } else {
          newLogs.push(`cat: файл '${arg}' не найден.`);
        }
        break;
      case 'run':
        void runCode();
        newLogs.push(`Запуск программы ${activeFile.name}...`);
        break;
      case 'echo':
        newLogs.push(arg);
        break;
      default:
        newLogs.push(`bash: ${command}: команда не найдена. Введите "help".`);
    }

    setTerminalHistory(newLogs);
  }

  // Interactive Python REPL Evaluation
  async function handleReplSubmit(e: React.FormEvent) {
    e.preventDefault();
    const expr = replInput.trim();
    if (!expr||replBusy.current) return;
    replBusy.current=true;
    setReplInput('');

    try {
      if(!replRunner.current)replRunner.current=new BrowserRunner('python');
      const code=`import ast, builtins\nif not hasattr(builtins, '_devforge_repl'):\n    builtins._devforge_repl = {'__name__': '__console__'}\n_scope = builtins._devforge_repl\n_tree = ast.parse(${JSON.stringify(expr)})\nif _tree.body and isinstance(_tree.body[-1], ast.Expr):\n    _last = _tree.body.pop()\n    exec(compile(_tree, '<console>', 'exec'), _scope)\n    _value = eval(compile(ast.Expression(_last.value), '<console>', 'eval'), _scope)\n    if _value is not None: print(repr(_value))\nelse:\n    exec(compile(_tree, '<console>', 'exec'), _scope)\n_variables = [{'name': k, 'type': type(v).__name__, 'value': repr(v)[:200]} for k,v in list(_scope.items()) if not k.startswith('__')][:100]`;
      const response=await replRunner.current.run({code,tests:[{id:'variables',label:'Variables',expression:'_variables',expected:null}]});
      setReplHistory(prev=>[...prev,{input:expr,output:response.error||response.stdout||response.stderr}]);
      const vars=response.results[0]?.actual;if(Array.isArray(vars))setVariables(vars);
    } catch (err) {
      setReplHistory(prev=>[...prev,{input:expr,output:String(err)}]);
    }finally{replBusy.current=false;}
  }

  // File Operations
  function createNewFile() {
    const name = prompt('Имя нового файла (например, service.py, router.py, config.py):', 'service.py');
    if (!name) return;
    if (!validName(name)||files.length>=30) {
      notify('Укажите уникальное имя с поддерживаемым расширением, без папок. Лимит — 30 файлов.');
      return;
    }
    const next = [...files, {name, content: '', baseline: ''}];
    changeFiles(next);
    setActiveFileIndex(next.length - 1);
  }

  function renameFile(index: number) {
    const current = files[index];
    const newName = prompt('Новое имя файла:', current.name);
    if (!newName || newName === current.name) return;
    if(!validName(newName,index)){notify('Некорректное или занятое имя файла');return;}
    const next = files.map((f, i) => i === index ? {...f, name: newName} : f);
    changeFiles(next);
    notify(`Файл переименован в ${newName}`);
  }

  function deleteFile(index: number) {
    if (files.length <= 1) {
      notify('В проекте должен оставаться хотя бы один файл.');
      return;
    }
    const target = files[index];
    if (confirm(`Удалить файл ${target.name}?`)) {
      const next = files.filter((_, i) => i !== index);
      changeFiles(next);
      if (activeFileIndex >= next.length) {
        setActiveFileIndex(next.length - 1);
      }
    }
  }

  function handleCommit() {
    if (!commitMessage.trim()) {
      notify('Введите сообщение коммита');
      return;
    }
    const newCommit: GitCommit = {
      hash: Math.random().toString(16).substring(2, 9),
      message: commitMessage,
      author: account.displayName || 'Developer',
      timestamp: 'Только что',
      filesCount: files.length
      ,files:files.map(f=>({name:f.name,content:f.content}))
    };
    const snapshots=[newCommit,...gitCommits].slice(0,20);
    try{localStorage.setItem(`snapshots:${account.id}:${projectId||'scratch'}`,JSON.stringify(snapshots));}catch{notify('Недостаточно места для снимка');return;}
    setGitCommits(snapshots);
    setCommitMessage('');
    setFiles(prev => prev.map(f => ({...f, baseline: f.content})));
    notify('Локальный снимок файлов сохранён');
  }

  // Search Everywhere Actions
  const allActions = [
    ...COMMANDS.map(c=>({id:c.id,label:c.label,shortcut:displayKey(keys[c.id]),category:'Action',action:()=>commandRef.current(c.id)})),
    {id: 'diff', label: 'Toggle Diff View (Сравнение версий)', shortcut: '', category: 'Action', action: () => setIsDiffMode(!isDiffMode)},
    {id: 'repl', label: 'Open Python Console (Интерактивная консоль)', shortcut: '', category: 'Action', action: () => { setBottomTab('repl'); setBottomOpen(true); }},
    {id: 'new_file', label: 'New File (Создать файл)', shortcut: '', category: 'Action', action: createNewFile},
    {id: 'db_tool', label: 'Open Database Tool (SQL Консоль)', shortcut: '', category: 'Tool', action: () => { setActiveTool('database'); setSidebarOpen(true); }},
    {id: 'api_tool', label: 'Open REST API Client (HTTP Запросы)', shortcut: '', category: 'Tool', action: () => { setActiveTool('api'); setSidebarOpen(true); }},
    {id: 'todos', label: 'Open TODO Explorer (Задачи в коде)', shortcut: '', category: 'Tool', action: () => { setActiveTool('todo'); setSidebarOpen(true); }},
    {id: 'minimap', label: 'Toggle Minimap (Миникарта)', shortcut: '', category: 'Setting', action: () => updateSettings({minimap: !settings.minimap})}
  ];

  // Filtered Search Everywhere Items
  const filteredSearchItems = [
    ...(searchEverywhereTab === 'all' || searchEverywhereTab === 'files'
      ? files.filter(f => f.name.toLowerCase().includes(searchEverywhereQuery.toLowerCase())).map(f => ({
          id: `file_${f.name}`,
          label: f.name,
          category: 'File',
          shortcut: '',
          action: () => {
            const idx = files.findIndex(file => file.name === f.name);
            if (idx !== -1) setActiveFileIndex(idx);
          }
        }))
      : []),
    ...(searchEverywhereTab === 'all' || searchEverywhereTab === 'actions'
      ? allActions.filter(a => a.label.toLowerCase().includes(searchEverywhereQuery.toLowerCase()))
      : []),
    ...(searchEverywhereTab === 'all' || searchEverywhereTab === 'symbols'
      ? symbols.filter(s => s.name.toLowerCase().includes(searchEverywhereQuery.toLowerCase())).map(s => ({
          id: `sym_${s.name}`,
          label: `${s.kind.toUpperCase()}: ${s.name} (строка ${s.line})`,
          category: 'Symbol',
          shortcut: `:${s.line}`,
          action: () => {
            if (editorRef.current) {
              editorRef.current.revealLineInCenter(s.line);
              editorRef.current.setPosition({lineNumber: s.line, column: 1});
            }
          }
        }))
      : [])
  ];

  if (loading) {
    return <div className="page muted" style={{padding: 40}}>Инициализация DevForge IDE…</div>;
  }
  if(loadError)return <div className="page"><h1>Не удалось открыть проект</h1><p role="alert">{loadError}</p><a href="/projects">К проектам</a></div>;

  return (
    <div ref={workbenchRef} className={`fusion-ide-container devforge-ide-container ide-workbench ${zen?'ide-zen':''} ${bottomOpen?'has-panel':''} ${bottomMaximized?'panel-maximized':''}`} style={workbenchStyle(prefs,settings.theme)} data-density={prefs.density} data-sidebar={prefs.sidebarSide} data-panel={prefs.panelPosition} data-centered={prefs.centered} data-theme={resolveTheme(prefs,settings.theme).light?'light':'dark'} data-activity={prefs.activityBar} data-status={prefs.statusBar} data-breadcrumbs={prefs.breadcrumbs}>
      {inputPrompt!==null&&<div className="input-overlay" role="dialog" aria-modal="true" aria-label="Программа ожидает ввод"><form className="input-dialog" onSubmit={e=>{e.preventDefault();inputResolve.current?.(inputValue);inputResolve.current=null;setInputPrompt(null);}}><h2>Программа ожидает ввод</h2><p>{inputPrompt}</p><label htmlFor="ide-input">Введите следующую строку</label><input id="ide-input" autoFocus maxLength={1000} value={inputValue} onChange={e=>setInputValue(e.target.value)}/><div><button type="button" onClick={()=>runner.current?.stop()}>Остановить программу</button><button className="primary" type="submit">Отправить</button></div></form></div>}
      {/* =================================================================== */}
      {/* 1. TOP PYCHARM & VS CODE RUN & NAVIGATION BAR                       */}
      {/* =================================================================== */}
      <header className="fusion-topbar">
        <div className="fusion-breadcrumbs ide-file-path">
          <span className="fusion-brand-pill" title="DevForge IDE 1.0.0">
            <ForgeIcon size={16} /> DevForge IDE
          </span>
          <span className="sep">/</span>
          <span className="proj-title">{project?.name || 'Workspace'}</span>
          <span className="sep">›</span>
          <span className="active-file-crumb">
            <FileCode2 size={13} className="crumb-icon" />
            {activeFile.name}
          </span>
          {symbols.length > 0 && (
            <>
              <span className="sep">›</span>
              <span className="symbol-crumb">🔷 {symbols[0].name}</span>
            </>
          )}
        </div>

        {/* Global Search Everywhere Trigger (Double Shift / Ctrl+P) */}
        <button
          className="fusion-palette-trigger"
          onClick={() => setSearchEverywhereOpen(true)}
          title="Поиск везде: файлы, команды, символы (Double Shift / Ctrl+P / F1)"
        >
          <Search size={13} />
          <span>Поиск файлов, команд, символов…</span>
          <kbd>{displayKey(keys.files)}</kbd>
        </button>

        {/* PyCharm Run / Debug Configurations Widget */}
        <div className="fusion-run-bar">
          <div className="fusion-run-select">
            <span className="run-dot" />
            <select
              value={runConfig}
              onChange={e => setRunConfig(e.target.value as any)}
              className="run-config-dropdown"
            >
              <option value="active">{activeFile.name}</option>
              <option value="main">main.py (FastAPI Server)</option>
              <option value="test">test_api.py (Pytest Suite)</option>
            </select>
          </div>

          {busy ? (
            <button className="fusion-btn stop" onClick={() => runner.current?.stop()} title="Остановить программу (Ctrl+F2)">
              <Square size={13} /> Stop
            </button>
          ) : (
            <button className="fusion-btn run" disabled={['md','txt','json'].includes(extension)} onClick={() => void runCode()} title={['md','txt','json'].includes(extension)?'Этот файл содержит документацию или данные':'Запустить программу (Shift+F10 / Ctrl+Enter)'}>
              <Play size={13} fill="currentColor" /> Run
            </button>
          )}

          <div className="fusion-runtime-chip" title={`Рантайм: ${LANGUAGE_NAMES[detectedLanguage]}`}>
            <span className="lang-icon">{detectedLanguage === 'python' ? '🐍' : '⚡'}</span>
            <span>{LANGUAGE_NAMES[detectedLanguage]}</span>
          </div>

          {/* Quick Action Buttons */}
          <div className="fusion-top-actions">
            <button className="fusion-icon-btn" aria-label="Настроить IDE" title={`Настроить IDE (${displayKey(keys.settings)})`} onClick={()=>setPreferencesOpen(true)}><Sliders size={16}/></button>
            <button className="fusion-icon-btn" aria-label={zen?'Вернуть панели':'Режим фокуса'} title={displayKey(keys.zen)} onClick={()=>setZen(v=>!v)}>{zen?<Minimize2 size={14}/>:<Maximize2 size={14}/>}</button>
            <button
              className={`fusion-icon-btn ${isSplit ? 'active' : ''}`}
              onClick={() => setIsSplit(!isSplit)}
              title="Разделить окно редактора (Split View: Ctrl+\)"
            >
              <Columns size={14} />
            </button>
            <button
              className={`fusion-icon-btn ${isDiffMode ? 'active' : ''}`}
              onClick={() => setIsDiffMode(!isDiffMode)}
              title="Сравнение версий (Diff Viewer)"
            >
              <Split size={14} />
            </button>
            <button
              className="fusion-icon-btn"
              onClick={formatDocument}
              title="Форматировать документ (Shift+Alt+F / Ctrl+Alt+L)"
            >
              <AlignLeft size={14} />
            </button>
            <button
              className={`fusion-icon-btn ${showAI ? 'active' : ''}`}
              onClick={() => setShowAI(!showAI)}
              title="AI Ассистент кода"
            >
              <Sparkles size={14} /> AI
            </button>
            <button
              className={`fusion-icon-btn ${settings.minimap ? 'active' : ''}`}
              onClick={() => updateSettings({minimap: !settings.minimap})}
              aria-label="Переключить миникарту"
              title="Миникарта"
            >
              <Map size={14} />
            </button>
            <button className="fusion-icon-btn" onClick={() => void saveProject()} aria-label="Сохранить код" title="Сохранить проект (Ctrl+S)">
              <Save size={14} />
            </button>
          </div>
        </div>
      </header>

      {/* =================================================================== */}
      {/* 2. MAIN LAYOUT: ACTIVITY BAR + SIDEBAR + EDITOR + BOTTOM PANEL      */}
      {/* =================================================================== */}
      <div className="fusion-main-layout">
        {/* VS Code Left Activity Bar */}
        <aside className="fusion-activity-bar">
          <div className="activity-group-top">
            <button
              className={`activity-btn ${activeTool === 'explorer' && sidebarOpen ? 'active' : ''}`}
              onClick={() => {
                if (activeTool === 'explorer') setSidebarOpen(!sidebarOpen);
                else { setActiveTool('explorer'); setSidebarOpen(true); }
              }}
              title="Проводник файлов (Ctrl+Shift+E)"
            >
              <Files size={20} />
            </button>
            <button
              className={`activity-btn ${activeTool === 'search' && sidebarOpen ? 'active' : ''}`}
              onClick={() => {
                if (activeTool === 'search') setSidebarOpen(!sidebarOpen);
                else { setActiveTool('search'); setSidebarOpen(true); }
              }}
              title="Поиск и замена по проекту (Ctrl+Shift+F)"
            >
              <Search size={20} />
            </button>
            <button
              className={`activity-btn ${activeTool === 'git' && sidebarOpen ? 'active' : ''}`}
              onClick={() => {
                if (activeTool === 'git') setSidebarOpen(!sidebarOpen);
                else { setActiveTool('git'); setSidebarOpen(true); }
              }}
              title="Контроль версий и коммиты (Ctrl+Shift+G)"
            >
              <GitBranch size={20} />
            </button>
            <button
              className={`activity-btn ${activeTool === 'structure' && sidebarOpen ? 'active' : ''}`}
              onClick={() => {
                if (activeTool === 'structure') setSidebarOpen(!sidebarOpen);
                else { setActiveTool('structure'); setSidebarOpen(true); }
              }}
              title="Структура файла (PyCharm Structure / AST Outline)"
            >
              <ListTree size={20} />
            </button>
            <button
              className={`activity-btn ${activeTool === 'database' && sidebarOpen ? 'active' : ''}`}
              onClick={() => {
                if (activeTool === 'database') setSidebarOpen(!sidebarOpen);
                else { setActiveTool('database'); setSidebarOpen(true); }
              }}
              title="База данных (JetBrains DataGrip Tool)"
            >
              <Database size={20} />
            </button>
            <button
              className={`activity-btn ${activeTool === 'api' && sidebarOpen ? 'active' : ''}`}
              onClick={() => {
                if (activeTool === 'api') setSidebarOpen(!sidebarOpen);
                else { setActiveTool('api'); setSidebarOpen(true); }
              }}
              title="REST API Client (Thunder Client / HTTP Runner)"
            >
              <Send size={20} />
            </button>
            <button
              className={`activity-btn ${activeTool === 'todo' && sidebarOpen ? 'active' : ''}`}
              onClick={() => {
                if (activeTool === 'todo') setSidebarOpen(!sidebarOpen);
                else { setActiveTool('todo'); setSidebarOpen(true); }
              }}
              title={`TODO Explorer (${todos.length} задач)`}
            >
              <ListTodo size={20} />
              {todos.length > 0 && <span className="activity-badge">{todos.length}</span>}
            </button>
            <button
              className={`activity-btn ${activeTool === 'debug' && sidebarOpen ? 'active' : ''}`}
              onClick={() => {
                if (activeTool === 'debug') setSidebarOpen(!sidebarOpen);
                else { setActiveTool('debug'); setSidebarOpen(true); }
              }}
              title="Конфигурация запуска и отладки (Run / Debug)"
            >
              <Sliders size={20} />
            </button>
          </div>

          <div className="activity-group-bottom">
            <button
              className={`activity-btn ${preferencesOpen ? 'active' : ''}`}
              onClick={() => setPreferencesOpen(true)}
              title="Настройки среды (Ctrl+,)"
            >
              <Settings size={20} />
            </button>
          </div>
        </aside>

        {/* Collapsible Sidebar Tool Window */}
        {sidebarOpen && activeTool && (
          <aside className="fusion-sidebar-window">
            <IDEResizer label="Изменить ширину боковой панели" axis="x" value={prefs.sidebarWidth} min={180} max={480} reverse={prefs.sidebarSide==='right'} onPreview={v=>setSizeDraft(d=>({...d,sidebarWidth:v}))} onCommit={v=>resize('sidebarWidth',v)}/>
            {/* 1. EXPLORER TOOL */}
            {activeTool === 'explorer' && (
              <div className="sidebar-content">
                <div className="sidebar-header">
                  <span>ПРОЕКТ: {project?.name || 'WORKSPACE'}</span>
                  <div className="sidebar-actions">
                    <button onClick={createNewFile} title="Создать файл"><Plus size={14} /></button>
                    <button onClick={() => renameFile(activeFileIndex)} title="Переименовать файл (F2)"><Edit3 size={14} /></button>
                    <button onClick={() => deleteFile(activeFileIndex)} title="Удалить активный файл"><Trash2 size={14} /></button>
                  </div>
                </div>

                <div className="open-editors-block">
                  <small className="section-title">ОТКРЫТЫЕ РЕДАКТОРЫ</small>
                  <div className="open-editors-list">
                    {files.map((file, idx) => hiddenTabs.includes(file.name)?null:(
                      <div
                        key={file.name}
                        className={`open-editor-row ${idx === activeFileIndex ? 'active' : ''}`}
                        onClick={() => setActiveFileIndex(idx)}
                      >
                        <FileCode2 size={13} className="tree-file-icon" />
                        <span className="file-name">{file.name}</span>
                        {dirty && idx === activeFileIndex && <span className="dirty-indicator" />}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="file-tree-list">
                  <small className="section-title">ФАЙЛЫ ПРОЕКТА</small>
                  {files.map((file, idx) => {
                    const ext = file.name.split('.').pop()?.toLowerCase();
                    return (
                      <button
                        key={file.name}
                        className={`tree-file-row ${idx === activeFileIndex ? 'active' : ''}`}
                        onClick={() => setActiveFileIndex(idx)}
                      >
                        <span className="file-lang-badge">
                          {ext === 'py' ? '🐍' : ext === 'md' ? '📝' : ext === 'sql' ? '🗄️' : '📄'}
                        </span>
                        <span className="tree-file-name">{file.name}</span>
                        {dirty && idx === activeFileIndex && <span className="dirty-indicator" />}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {/* 2. SEARCH & REPLACE TOOL */}
            {activeTool === 'search' && (
              <div className="sidebar-content">
                <div className="sidebar-header">
                  <span>ПОИСК И ЗАМЕНА</span>
                </div>
                <div className="search-box">
                  <div className="search-input-wrapper">
                    <input
                      type="text"
                      placeholder="Найти в проекте..."
                      value={searchQuery}
                      onChange={e => setSearchQuery(e.target.value)}
                      autoFocus
                    />
                    <div className="search-modifiers">
                      <button className={`mod-btn ${isCaseSensitive ? 'active' : ''}`} onClick={() => setIsCaseSensitive(!isCaseSensitive)} title="Учитывать регистр (Aa)">Aa</button>
                      <button className={`mod-btn ${isWholeWord ? 'active' : ''}`} onClick={() => setIsWholeWord(!isWholeWord)} title="Слово целиком (\b)">\b</button>
                      <button className={`mod-btn ${isRegex ? 'active' : ''}`} onClick={() => setIsRegex(!isRegex)} title="Регулярное выражение (.*)">.*</button>
                    </div>
                  </div>

                  <div className="replace-input-wrapper">
                    <input
                      type="text"
                      placeholder="Заменить на..."
                      value={replaceQuery}
                      onChange={e => setReplaceQuery(e.target.value)}
                    />
                    <button className="replace-btn" onClick={handleReplaceAll} title="Заменить все">
                      Заменить все
                    </button>
                  </div>

                  <div className="search-count">{searchMatches.length} совпадений в {files.length} файлах</div>
                </div>

                <div className="search-results-list">
                  {searchMatches.map((m, i) => (
                    <div
                      key={i}
                      className="search-result-row"
                      onClick={() => {
                        setActiveFileIndex(m.fileIndex);
                        if (editorRef.current) {
                          editorRef.current.revealLineInCenter(m.line);
                          editorRef.current.setPosition({lineNumber: m.line, column: 1});
                        }
                      }}
                    >
                      <div className="search-match-header">
                        <strong>{m.file}</strong>
                        <small className="muted">строка {m.line}</small>
                      </div>
                      <div className="search-match-snippet">{m.text}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 3. GIT SOURCE CONTROL TOOL */}
            {activeTool === 'git' && (
              <div className="sidebar-content">
                <div className="sidebar-header">
                  <span>SOURCE CONTROL (GIT)</span>
                </div>
                <div className="git-status-card">
                  <div className="git-branch-info">
                    <GitBranch size={16} /> <strong>main</strong> <small>(Local snapshots)</small>
                  </div>
                  <div className="commit-box">
                    <textarea
                      rows={3}
                      placeholder="Название снимка файлов"
                      value={commitMessage}
                      onChange={e => setCommitMessage(e.target.value)}
                    />
                    <button className="button primary compact" style={{width: '100%', marginTop: 6}} onClick={handleCommit}>
                      <Check size={13} /> Сохранить снимок
                    </button>
                  </div>

                  <div className="git-changes-list">
                    <small className="section-title">ИЗМЕНЁННЫЕ ФАЙЛЫ ({dirty ? '1' : '0'})</small>
                    {dirty ? (
                      <div className="git-change-row" onClick={() => setIsDiffMode(true)}>
                        <span className="change-badge mod">M</span>
                        <span>{activeFile.name}</span>
                        <small className="diff-link">Сравнить diff</small>
                      </div>
                    ) : (
                      <div className="muted" style={{fontSize: 12, padding: 8}}>Рабочая директория чиста.</div>
                    )}
                  </div>

                  <div className="git-history-section">
                    <small className="section-title">ИСТОРИЯ СНИМКОВ</small>
                    <div className="git-history-list">
                      {gitCommits.map(c => (
                        <div key={c.hash} className="git-commit-item">
                          <div className="commit-top">
                            <span className="commit-hash">{c.hash}</span>
                            <span className="commit-time">{c.timestamp}</span>
                          </div>
                          <div className="commit-msg">{c.message}</div>
                          <div className="commit-author"><small>{c.author} · {c.filesCount} файлов</small></div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 4. STRUCTURE / AST OUTLINE TOOL (PyCharm Feature) */}
            {activeTool === 'structure' && (
              <div className="sidebar-content">
                <div className="sidebar-header">
                  <span>СТРУКТУРА КОДА (OUTLINE)</span>
                  <small className="muted">{symbols.length} символов</small>
                </div>
                <div className="structure-tree">
                  {symbols.length > 0 ? (
                    symbols.map((s, idx) => (
                      <div
                        key={idx}
                        className={`structure-item ${s.kind}`}
                        onClick={() => {
                          if (editorRef.current) {
                            editorRef.current.revealLineInCenter(s.line);
                            editorRef.current.setPosition({lineNumber: s.line, column: 1});
                          }
                        }}
                      >
                        <span className="symbol-badge">
                          {s.kind === 'class' ? 'C' : s.kind === 'route' ? 'R' : s.kind === 'function' ? 'f' : 'v'}
                        </span>
                        <span className="symbol-name">{s.name}</span>
                        <span className="symbol-line">:{s.line}</span>
                      </div>
                    ))
                  ) : (
                    <div className="empty-symbols">В текущем файле не найдено классов или функций.</div>
                  )}
                </div>
              </div>
            )}

            {/* 5. DATABASE TOOL (DataGrip Style) */}
            {activeTool === 'database' && (
              <div className="sidebar-content">
                <div className="sidebar-header">
                  <span>SQL DATABASE TOOL</span>
                  <button onClick={() => {
                    setBottomTab('database');
                    setBottomOpen(true);
                  }} title="Выполнить SQL"><Play size={13} fill="currentColor" /></button>
                </div>
                <div className="db-tables-tree">
                  <div className="db-table-item">
                    <strong>🗄️ items (SQLite)</strong>
                    <div className="db-col"><span>id</span> <small>INTEGER PK</small></div>
                    <div className="db-col"><span>name</span> <small>VARCHAR(100)</small></div>
                    <div className="db-col"><span>price</span> <small>FLOAT</small></div>
                    <div className="db-col"><span>description</span> <small>TEXT</small></div>
                    <div className="db-col"><span>in_stock</span> <small>BOOLEAN</small></div>
                  </div>
                  <div className="db-table-item">
                    <strong>🗄️ users</strong>
                    <div className="db-col"><span>id</span> <small>INTEGER PK</small></div>
                    <div className="db-col"><span>username</span> <small>VARCHAR(50)</small></div>
                    <div className="db-col"><span>role</span> <small>VARCHAR(20)</small></div>
                  </div>
                </div>
                <div className="db-sql-editor">
                  <textarea
                    rows={4}
                    value={sqlQuery}
                    onChange={e => setSqlQuery(e.target.value)}
                    placeholder="Введите SQL запрос..."
                    spellCheck={false}
                  />
                  <button className="button primary compact" style={{width: '100%', marginTop: 6}} onClick={() => {
                    setBottomTab('database');
                    setBottomOpen(true);
                  }}>
                    <Play size={12} fill="currentColor" /> Запустить SQL запрос
                  </button>
                </div>
              </div>
            )}

            {/* 6. REST API CLIENT TOOL */}
            {activeTool === 'api' && (
              <div className="sidebar-content">
                <div className="sidebar-header">
                  <span>REST API CLIENT</span>
                </div>
                <div className="api-request-form">
                  <div className="api-url-row">
                    <select value={apiMethod} onChange={e => setApiMethod(e.target.value as any)}>
                      <option value="GET">GET</option>
                      <option value="POST">POST</option>
                      <option value="PUT">PUT</option>
                      <option value="DELETE">DELETE</option>
                      <option value="PATCH">PATCH</option>
                    </select>
                    <input
                      type="text"
                      value={apiUrl}
                      onChange={e => setApiUrl(e.target.value)}
                      placeholder="/api/platform"
                    />
                  </div>
                  <div className="api-headers-block">
                    <small className="muted">Headers:</small>
                    <textarea
                      rows={2}
                      value={apiHeaders}
                      onChange={e => setApiHeaders(e.target.value)}
                      spellCheck={false}
                    />
                  </div>
                  {['POST', 'PUT', 'PATCH'].includes(apiMethod) && (
                    <div className="api-body-block">
                      <small className="muted">JSON Request Body:</small>
                      <textarea
                        rows={5}
                        value={apiBody}
                        onChange={e => setApiBody(e.target.value)}
                        spellCheck={false}
                      />
                    </div>
                  )}
                  <button
                    className="button primary compact"
                    style={{width: '100%', marginTop: 8}}
                    disabled={apiSending}
                    onClick={() => void sendApiRequest()}
                  >
                    <Send size={13} /> {apiSending ? 'Отправка…' : 'Отправить запрос'}
                  </button>

                  <div className="api-history-section">
                    <small className="section-title">ИСТОРИЯ ЗАПРОСОВ</small>
                    <div className="api-history-list">
                      {apiHistory.map((h, i) => (
                        <div
                          key={i}
                          className="api-history-item"
                          onClick={() => {
                            setApiMethod(h.method as any);
                            setApiUrl(h.url);
                          }}
                        >
                          <span className={`method-badge ${h.method.toLowerCase()}`}>{h.method}</span>
                          <span className="hist-url">{h.url}</span>
                          <span className="hist-time">{h.time}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 7. TODO EXPLORER TOOL (PyCharm TODO Feature) */}
            {activeTool === 'todo' && (
              <div className="sidebar-content">
                <div className="sidebar-header">
                  <span>TODO EXPLORER</span>
                  <small className="muted">{todos.length} задач</small>
                </div>
                <div className="todo-list">
                  {todos.length > 0 ? (
                    todos.map((t, idx) => (
                      <div
                        key={idx}
                        className={`todo-row ${t.type.toLowerCase()}`}
                        onClick={() => {
                          setActiveFileIndex(t.fileIndex);
                          if (editorRef.current) {
                            editorRef.current.revealLineInCenter(t.line);
                            editorRef.current.setPosition({lineNumber: t.line, column: 1});
                          }
                        }}
                      >
                        <div className="todo-meta">
                          <span className={`todo-type-tag ${t.type.toLowerCase()}`}>{t.type}</span>
                          <strong>{t.file}:{t.line}</strong>
                        </div>
                        <div className="todo-snippet">{t.text}</div>
                      </div>
                    ))
                  ) : (
                    <div className="empty-symbols">В проекте не найдено тегов TODO или FIXME.</div>
                  )}
                </div>
              </div>
            )}

            {/* 8. RUN / DEBUG CONFIGURATIONS */}
            {activeTool === 'debug' && (
              <div className="sidebar-content">
                <div className="sidebar-header">
                  <span>RUN / DEBUG CONFIG</span>
                </div>
                <div className="debug-form">
                  <div className="form-group">
                    <label>Активная конфигурация:</label>
                    <select value={runConfig} onChange={e => setRunConfig(e.target.value as any)}>
                      <option value="active">Текущий открытый файл</option>
                      <option value="main">FastAPI Uvicorn Сервер</option>
                      <option value="test">Pytest Тестовый модуль</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Аргументы командной строки:</label>
                    <input
                      type="text"
                      value={cliArgs}
                      onChange={e => setCliArgs(e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label>Переменные окружения (KEY=VALUE):</label>
                    <textarea
                      rows={3}
                      value={envVars}
                      onChange={e => setEnvVars(e.target.value)}
                    />
                  </div>
                  <button className="button primary compact" style={{width: '100%', marginTop: 8}} onClick={() => void runCode()}>
                    <Play size={13} fill="currentColor" /> Запустить с этими параметрами
                  </button>
                </div>
              </div>
            )}

            {/* 9. SETTINGS & PREFERENCES */}
            {activeTool === 'settings' && (
              <div className="sidebar-content">
                <div className="sidebar-header">
                  <span>ПАРАМЕТРЫ СРЕДЫ (IDE)</span>
                </div>
                <div className="settings-panel-form">
                  <button onClick={()=>setPreferencesOpen(true)}>Открыть все настройки IDE</button>
                  <div className="form-group">
                    <label>Цветовая тема редактора:</label>
                    <select
                      value={settings.theme}
                      onChange={e => updateSettings({theme: e.target.value as any})}
                    >
                      <option value="dark">DevForge Dark (по умолчанию)</option>
                      <option value="light">DevForge Light</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Размер шрифта кода: {settings.fontSize}px</label>
                    <div className="font-size-buttons">
                      {[12, 14, 16, 18].map(sz => (
                        <button
                          key={sz}
                          className={settings.fontSize === sz ? 'active' : ''}
                          onClick={() => updateSettings({fontSize: sz})}
                        >
                          {sz}px
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="form-group">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={!!settings.minimap}
                        onChange={e => updateSettings({minimap: e.target.checked})}
                      />
                      Отображать миникарту кода (Minimap)
                    </label>
                  </div>
                  <div className="form-group">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={!!settings.inlineCompletion}
                        onChange={e => updateSettings({inlineCompletion: e.target.checked})}
                      />
                      Умное автодополнение и подсказки
                    </label>
                  </div>
                </div>
              </div>
            )}
          </aside>
        )}

        {/* Central Editor Area (with Multi-Tab, Split Editor & Diff Editor) */}
        <div className="fusion-editor-container">
          {/* File Tabs Strip */}
          <div className="fusion-tab-bar" role="tablist" aria-label="Файлы редактора">
            {files.map((file, idx) => hiddenTabs.includes(file.name)?null:(
              <div
                key={file.name}
                className={`fusion-tab ${idx === activeFileIndex ? 'active' : ''}`}
                role="tab" aria-selected={idx===activeFileIndex} tabIndex={0}
                onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();setActiveFileIndex(idx);}}}
                onDoubleClick={()=>setZen(v=>!v)}
                onClick={() => setActiveFileIndex(idx)}
              >
                <FileCode2 size={13} className="tab-icon" />
                <span className="tab-name">{file.name}</span>
                {dirty && idx === activeFileIndex && <span className="tab-dirty-dot" />}
                {files.length > 1 && (
                  <button
                    className="tab-close"
                    title="Закрыть вкладку" aria-label={`Закрыть вкладку ${file.name}`}
                    onClick={e => {
                      e.stopPropagation();
                      closeTab(idx);
                    }}
                  >
                    <X size={12} />
                  </button>
                )}
              </div>
            ))}
            <button className="fusion-tab-plus" onClick={createNewFile} title="Создать новый файл">
              <Plus size={14} />
            </button>
          </div>

          {/* Monaco Editor / Split Editor / Diff Editor Shell */}
          <div className="fusion-monaco-shell">
            {isDiffMode ? (
              /* DIFF VIEWER (Comparison between Baseline and Current Content) */
              <div className="ide-diff-container">
                <div className="ide-diff-header">
                  <span>Сравнение изменений: <strong>{activeFile.name}</strong></span>
                  <button className="compact button" onClick={() => setIsDiffMode(false)}>Вернуться в редактор</button>
                </div>
                <div className="ide-diff-panes">
                  <div className="diff-pane">
                    <div className="diff-pane-title">Базовая версия (Baseline)</div>
                    <pre className="diff-code-pre">{activeFile.baseline || '(пусто)'}</pre>
                  </div>
                  <div className="diff-pane">
                    <div className="diff-pane-title">Текущая версия (Working Copy)</div>
                    <pre className="diff-code-pre modified">{activeFile.content}</pre>
                  </div>
                </div>
              </div>
            ) : isSplit ? (
              /* SPLIT EDITOR VIEW (Two Editor Panes Side-by-Side) */
              <div className="ide-split-container">
                <div className="ide-split-pane">
                  <div className="split-pane-header">
                    <span>{activeFile.name}</span>
                  </div>
                  <Suspense fallback={<div className="muted" style={{padding: 20}}>Загрузка редактора…</div>}>
                    <CodeEditor
                      path={`devforge/${account.id}/${projectId||'scratch'}/left/${activeFile.name}`}
                      onMount={mountEditor}
                      language={editorLanguage(activeFile.name)}
                      code={activeFile.content}
                      onChange={val => updateCode(val, activeFileIndex)}
                      onCursorChange={(line, col) => setCursorPos({line, col})}
                    />
                  </Suspense>
                </div>

                <div className="ide-split-pane">
                  <div className="split-pane-header">
                    <select
                      value={splitFileIndex}
                      onChange={e => setSplitFileIndex(Number(e.target.value))}
                      className="split-file-select"
                    >
                      {files.map((f, i) => (
                        <option key={f.name} value={i}>{f.name}</option>
                      ))}
                    </select>
                  </div>
                  <Suspense fallback={<div className="muted" style={{padding: 20}}>Загрузка редактора…</div>}>
                    <CodeEditor
                      path={`devforge/${account.id}/${projectId||'scratch'}/right/${splitFile.name}`}
                      onMount={mountEditor}
                      language={editorLanguage(splitFile.name)}
                      code={splitFile.content}
                      onChange={val => updateCode(val, splitFileIndex)}
                    />
                  </Suspense>
                </div>
              </div>
            ) : (
              /* STANDARD SINGLE MONACO EDITOR */
              <Suspense fallback={<div className="muted" style={{padding: 20}}>Загрузка Monaco Editor…</div>}>
                <CodeEditor
                  path={`devforge/${account.id}/${projectId||'scratch'}/${activeFile.name}`}
                  language={editorLanguage(activeFile.name)}
                  code={activeFile.content}
                  onChange={updateCode}
                  onMount={mountEditor}
                  onCursorChange={(line, col) => setCursorPos({line, col})}
                />
              </Suspense>
            )}
          </div>

          {/* =============================================================== */}
          {/* 3. MULTI-TAB BOTTOM TOOL WINDOW (PyCharm & VS Code style)       */}
          {/* =============================================================== */}
          {bottomOpen && (
            <div className={`fusion-bottom-panel ${bottomMaximized ? 'maximized' : ''}`}>
              {!bottomMaximized&&<IDEResizer label="Изменить размер панели инструментов" axis={prefs.panelPosition==='right'?'x':'y'} value={prefs.panelPosition==='right'?prefs.panelWidth:prefs.panelHeight} min={prefs.panelPosition==='right'?240:140} max={prefs.panelPosition==='right'?640:600} reverse onPreview={v=>setSizeDraft(d=>({...d,[prefs.panelPosition==='right'?'panelWidth':'panelHeight']:v}))} onCommit={v=>resize(prefs.panelPosition==='right'?'panelWidth':'panelHeight',v)}/>}
              <div className="bottom-panel-header">
                <div className="bottom-tabs">
                  <button
                    className={`bottom-tab ${bottomTab === 'output' ? 'active' : ''}`}
                    onClick={() => setBottomTab('output')}
                  >
                    <Terminal size={13} /> Вывод программы (Console)
                  </button>
                  <button
                    className={`bottom-tab ${bottomTab === 'terminal' ? 'active' : ''}`}
                    onClick={() => setBottomTab('terminal')}
                  >
                    <Code2 size={13} /> Терминал (Shell)
                  </button>
                  <button
                    className={`bottom-tab ${bottomTab === 'repl' ? 'active' : ''}`}
                    onClick={() => setBottomTab('repl')}
                  >
                    <Bug size={13} /> Python REPL & Переменные
                  </button>
                  <button
                    className={`bottom-tab ${bottomTab === 'problems' ? 'active' : ''}`}
                    onClick={() => setBottomTab('problems')}
                  >
                    <AlertCircle size={13} /> Проблемы ({problems.length})
                  </button>
                  <button
                    className={`bottom-tab ${bottomTab === 'api' ? 'active' : ''}`}
                    onClick={() => setBottomTab('api')}
                  >
                    <Send size={13} /> Ответ API {apiResponse && <span className={`pill ${apiResponse.status >= 200 && apiResponse.status < 300 ? 'available' : 'error'}`}>{apiResponse.status}</span>}
                  </button>
                  <button
                    className={`bottom-tab ${bottomTab === 'database' ? 'active' : ''}`}
                    onClick={() => setBottomTab('database')}
                  >
                    <Database size={13} /> База данных (Data Grid)
                  </button>
                  <button
                    className={`bottom-tab ${bottomTab === 'stdin' ? 'active' : ''}`}
                    onClick={() => setBottomTab('stdin')}
                  >
                    <AlignLeft size={13} /> Ввод (STDIN)
                  </button>
                </div>

                <div className="bottom-panel-actions">
                  {result && (
                    <small className="muted" style={{marginRight: 10}}>
                      {result.duration ? `${result.duration.toFixed(0)} мс` : ''}
                    </small>
                  )}
                  <button onClick={() => setBottomMaximized(!bottomMaximized)} title="Развернуть/Свернуть">
                    {bottomMaximized ? <Minimize2 size={13} /> : <Maximize2 size={13} />}
                  </button>
                  <button onClick={() => setBottomOpen(false)} title="Закрыть панель">
                    <X size={13} />
                  </button>
                </div>
              </div>

              <div className="bottom-panel-body">
                {/* 1. OUTPUT CONSOLE */}
                {bottomTab === 'output' && (
                  <div className="panel-output-view">
                    {busy && (
                      <div className="runtime-status">
                        <span className="pulse-dot" /> {status}
                      </div>
                    )}
                    <Output result={result} />
                    {htmlPreview&&<iframe title="Предпросмотр HTML и CSS" className="html-preview" sandbox="" srcDoc={htmlPreview}/>}
                  </div>
                )}

                {/* 2. INTERACTIVE TERMINAL */}
                {bottomTab === 'terminal' && (
                  <div className="panel-terminal-view">
                    <div className="terminal-logs">
                      {terminalHistory.map((line, i) => (
                        <div key={i} className="terminal-log-line">{line}</div>
                      ))}
                    </div>
                    <form className="terminal-input-row" onSubmit={handleTerminalSubmit}>
                      <span className="terminal-prompt">devforge$</span>
                      <input
                        type="text"
                        value={terminalInput}
                        onChange={e => setTerminalInput(e.target.value)}
                        placeholder="Введите команду (например: ls, run, pip list, help)..."
                        autoFocus
                      />
                    </form>
                  </div>
                )}

                {/* 3. PYTHON REPL & VARIABLES INSPECTOR */}
                {bottomTab === 'repl' && (
                  <div className="panel-repl-view">
                    <div className="repl-console-half">
                      <small className="section-title">ИНТЕРАКТИВНАЯ КОНСОЛЬ (PYTHON REPL)</small>
                      <div className="repl-history">
                        {replHistory.map((h, i) => (
                          <div key={i} className="repl-exchange">
                            <div className="repl-in"><span>&gt;&gt;&gt;</span> {h.input}</div>
                            {h.output && <div className="repl-out">{h.output}</div>}
                          </div>
                        ))}
                      </div>
                      <form className="repl-input-row" onSubmit={handleReplSubmit}>
                        <span>&gt;&gt;&gt;</span>
                        <input
                          type="text"
                          value={replInput}
                          onChange={e => setReplInput(e.target.value)}
                          placeholder="Вычислить выражение в Python..."
                        />
                      </form>
                    </div>

                    <div className="repl-vars-half">
                      <small className="section-title">ИНСПЕКТОР ПЕРЕМЕННЫХ (PYCHARM VARIABLES)</small>
                      <div className="vars-table-scroll">
                        <table className="vars-table">
                          <thead>
                            <tr>
                              <th>Имя</th>
                              <th>Тип</th>
                              <th>Значение</th>
                            </tr>
                          </thead>
                          <tbody>
                            {variables.map(v => (
                              <tr key={v.name}>
                                <td className="var-name"><code>{v.name}</code></td>
                                <td className="var-type"><span className="type-badge">{v.type}</span></td>
                                <td className="var-val">{v.value}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                )}

                {/* 4. PROBLEMS / DIAGNOSTICS */}
                {bottomTab === 'problems' && (
                  <div className="panel-problems-view">
                    {problems.length > 0 ? (
                      <div className="problems-list">
                        {problems.map((p, i) => (
                          <div
                            key={i}
                            className={`problem-item ${p.severity}`}
                            onClick={() => {
                              if (editorRef.current) {
                                editorRef.current.revealLineInCenter(p.line);
                                editorRef.current.setPosition({lineNumber: p.line, column: p.col});
                              }
                            }}
                          >
                            <AlertCircle size={14} className="prob-icon" />
                            <span className="prob-msg">{p.message}</span>
                            <span className="prob-pos">{p.file} [{p.line}, {p.col}]</span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="empty-panel-state">
                        <CheckCircle2 size={24} style={{color: '#22c55e'}} />
                        <p>В проекте не обнаружено синтаксических ошибок или предупреждений.</p>
                      </div>
                    )}
                  </div>
                )}

                {/* 5. API CLIENT RESPONSE */}
                {bottomTab === 'api' && (
                  <div className="panel-api-view">
                    {apiResponse ? (
                      <div className="api-response-card">
                        <div className="api-resp-top">
                          <span className={`status-badge ${apiResponse.status >= 200 && apiResponse.status < 300 ? 'status-200' : 'status-err'}`}>
                            {apiResponse.status} {apiResponse.statusText}
                          </span>
                          <span className="time-badge">{apiResponse.timeMs} ms</span>
                          <span className="size-badge">{apiResponse.sizeBytes} B</span>
                          <button
                            className="compact button"
                            onClick={() => {
                              navigator.clipboard.writeText(JSON.stringify(apiResponse.data, null, 2));
                              notify('Ответ скопирован в буфер обмена');
                            }}
                          >
                            <Copy size={12} /> Скопировать JSON
                          </button>
                        </div>
                        <pre className="api-json-pre">
                          {typeof apiResponse.data === 'object' ? JSON.stringify(apiResponse.data, null, 2) : String(apiResponse.data)}
                        </pre>
                      </div>
                    ) : (
                      <div className="empty-panel-state">
                        <Send size={24} />
                        <p>Отправьте запрос через вкладку REST API Client на панели слева.</p>
                      </div>
                    )}
                  </div>
                )}

                {/* 6. DATABASE TABLE GRID */}
                {bottomTab === 'database' && (
                  <div className="panel-db-view">
                    {sqlResult ? (
                      <>
                        <div className="db-grid-actions">
                          <small className="muted">{sqlResult.rows.length} строк(и) в результате</small>
                          <button
                            className="compact button"
                            onClick={() => {
                              const csv = [
                                sqlResult.headers.join(','),
                                ...sqlResult.rows.map(r => r.join(','))
                              ].join('\n');
                              const blob = new Blob([csv], {type: 'text/csv'});
                              const url = URL.createObjectURL(blob);
                              const a = document.createElement('a');
                              a.href = url;
                              a.download = 'query_results.csv';
                              a.click();
                            }}
                          >
                            <Download size={12} /> Экспорт в CSV
                          </button>
                        </div>
                        <div className="db-grid-scroll">
                          <table className="db-table-grid">
                            <thead>
                              <tr>
                                {sqlResult.headers.map((h, i) => (
                                  <th key={i}>{h}</th>
                                ))}
                              </tr>
                            </thead>
                            <tbody>
                              {sqlResult.rows.map((row, rIdx) => (
                                <tr key={rIdx}>
                                  {row.map((cell, cIdx) => (
                                    <td key={cIdx}>{String(cell)}</td>
                                  ))}
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </>
                    ) : (
                      <div className="empty-panel-state">
                        <Database size={24} />
                        <p>Запустите SQL-запрос для отображения результатов в таблице.</p>
                      </div>
                    )}
                  </div>
                )}

                {/* 7. STDIN PANEL */}
                {bottomTab === 'stdin' && (
                  <div className="panel-stdin-view">
                    <label htmlFor="devforge-stdin">Входные данные для стандартного ввода (STDIN):</label>
                    <textarea
                      id="devforge-stdin"
                      rows={4}
                      value={stdin}
                      onChange={e => setStdin(e.target.value)}
                      placeholder="Впишите данные для чтения через input(), cin или scanf..."
                    />
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* =================================================================== */}
      {/* 4. PROFESSIONAL STATUS BAR (VS Code & PyCharm Status Bar)           */}
      {/* =================================================================== */}
      <footer className="fusion-statusbar devforge-statusbar">
        <div className="statusbar-left">
          <span className="status-item branch" title="Локальные снимки проекта">
            <History size={12} /> Снимки: {gitCommits.length}
          </span>
          <span className="status-item problems-badge" onClick={() => { setBottomTab('problems'); setBottomOpen(true); }}>
            <AlertCircle size={12} /> {problems.length}
          </span>
          <span className="status-item ready">
            <span className={busy ? 'pulse-dot' : 'green-dot'} />
            {busy ? status : 'Готово'}
          </span>
          <span className="status-item platform-pill">
            {PlatformAdapter.isDesktop() ? <Laptop size={12} /> : <Globe size={12} />}
            {PlatformAdapter.isDesktop() ? 'Desktop (WebView2)' : 'Web (Браузер)'}
          </span>
        </div>

        <div className="statusbar-right">
          <span className="status-item">{saveState}</span>
          <span className="status-item">Ln {cursorPos.line}, Col {cursorPos.col}</span>
          <span className="status-item">{prefs.insertSpaces?'Spaces':'Tab'}: {prefs.tabSize}</span>
          <span className="status-item">UTF-8</span>
          <span className="status-item">{activeFile.content.includes('\r\n')?'CRLF':'LF'}</span>
          <span className="status-item lang-badge">
            {LANGUAGE_NAMES[detectedLanguage] || 'Python 3.12'}
          </span>
          <span className="status-item keymap-badge" title="Схема горячих клавиш">
            {prefs.keymap==='code'?'VS Code':'JetBrains'}
          </span>
        </div>
      </footer>

      {/* =================================================================== */}
      {/* 5. SEARCH EVERYWHERE MODAL (Double Shift / Ctrl+P / F1)             */}
      {/* =================================================================== */}
      {searchEverywhereOpen && (
        <div className="fusion-palette-overlay" onClick={() => setSearchEverywhereOpen(false)}>
          <div className="fusion-palette-modal search-everywhere-modal" onClick={e => e.stopPropagation()}>
            <div className="search-everywhere-tabs">
              <button
                className={searchEverywhereTab === 'all' ? 'active' : ''}
                onClick={() => setSearchEverywhereTab('all')}
              >
                Везде (All)
              </button>
              <button
                className={searchEverywhereTab === 'files' ? 'active' : ''}
                onClick={() => setSearchEverywhereTab('files')}
              >
                Файлы (Files)
              </button>
              <button
                className={searchEverywhereTab === 'actions' ? 'active' : ''}
                onClick={() => setSearchEverywhereTab('actions')}
              >
                Действия (Actions)
              </button>
              <button
                className={searchEverywhereTab === 'symbols' ? 'active' : ''}
                onClick={() => setSearchEverywhereTab('symbols')}
              >
                Символы (Symbols)
              </button>
            </div>

            <div className="palette-input-box">
              <Command size={16} />
              <input
                type="text"
                autoFocus
                placeholder="Поиск файлов, действий, настроек и символов..."
                value={searchEverywhereQuery}
                onChange={e => setSearchEverywhereQuery(e.target.value)}
                role="combobox" aria-label="Поиск команд и файлов" aria-expanded="true" aria-controls="ide-palette-results" aria-activedescendant={filteredSearchItems[paletteIndex]?`palette-option-${paletteIndex}`:undefined}
                onKeyDown={e=>{
                  if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();setPaletteIndex(i=>filteredSearchItems.length?(i+(e.key==='ArrowDown'?1:-1)+filteredSearchItems.length)%filteredSearchItems.length:0);}
                  if(e.key==='Enter'&&filteredSearchItems[paletteIndex]){e.preventDefault();setSearchEverywhereOpen(false);filteredSearchItems[paletteIndex].action();}
                }}
              />
            </div>

            <div className="palette-list" id="ide-palette-results" role="listbox" ref={paletteList}>
              {filteredSearchItems.length===0&&<p className="ide-pref-hint" style={{padding:'0 20px'}}>Ничего не найдено. Попробуйте другое название.</p>}
              {filteredSearchItems.map((item,index) => (
                <button type="button" role="option" id={`palette-option-${index}`} aria-selected={index===paletteIndex} tabIndex={-1}
                  key={item.id}
                  className="palette-item"
                  onMouseEnter={()=>setPaletteIndex(index)}
                  onClick={() => {
                    setSearchEverywhereOpen(false);
                    item.action();
                  }}
                >
                  <div className="item-left">
                    <span className={`item-cat-badge ${item.category.toLowerCase()}`}>{item.category}</span>
                    <span className="palette-label">{item.label}</span>
                  </div>
                  {item.shortcut && <kbd className="palette-kbd">{item.shortcut}</kbd>}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {preferencesOpen&&<IDECustomization onClose={()=>setPreferencesOpen(false)}/>}
      {/* AI Assistant Drawer */}
      {showAI && (
        <AIHelp
          code={activeFile.content}
          language={detectedLanguage}
          onInsert={updateCode}
        />
      )}
    </div>
  );
}
