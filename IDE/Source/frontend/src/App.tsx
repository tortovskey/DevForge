import {useEffect, useState} from 'react';
import {NavLink,Route,Routes,useLocation,useNavigate} from 'react-router-dom';
import {LayoutDashboard,BookOpen,Code2,Swords,Library,FolderOpen,ChartNoAxesCombined,Settings as SettingsIcon,ChevronDown,Menu,Command,ArrowUpRight,WifiOff} from 'lucide-react';
import {StoreProvider,useStore} from './services/store';
import {Dashboard,Learn,Challenges,Documentation,Projects,ProgressPage,SettingsPage} from './pages/Pages';
import {AuthGate,useAuth} from './services/auth';
import Assessment from './pages/Assessment';
import Workspace from './pages/Workspace';
import {ForgeIcon} from './components/ForgeIcon';

const fullNavigation=[
  ['/','Dashboard',LayoutDashboard],
  ['/learn','Learn',BookOpen],
  ['/assessment','Мой маршрут',BookOpen],
  ['/ide','IDE',Code2],
  ['/challenges','Challenges',Swords],
  ['/documentation','Documentation',Library],
  ['/projects','Projects',FolderOpen],
  ['/progress','Progress',ChartNoAxesCombined]
] as const;

const ideNavigation=[
  ['/ide','Редактор (IDE)',Code2],
  ['/projects','Проекты',FolderOpen],
  ['/documentation','Справочник API',Library],
  ['/settings','Настройки',SettingsIcon],
] as const;

function Shell(){
  const {account,courses,settings,updateSettings,notify,progress}=useStore();
  const {logout,isIde}=useAuth(),location=useLocation(),navigate=useNavigate();
  const [menu,setMenu]=useState(false);

  useEffect(() => {
    document.title = isIde ? 'DevForge IDE' : 'DevForge Academy';
  }, [isIde]);

  const activeNav = isIde ? ideNavigation : fullNavigation;
  const currentEntry = activeNav.find(([path])=>path==='/'?location.pathname==='/':location.pathname.startsWith(path));
  const title = currentEntry ? currentEntry[1] : (isIde ? 'DevForge IDE' : 'Settings');
  const workspace = isIde || location.pathname==='/ide'||/^\/(learn|projects)\/.+/.test(location.pathname);

  return (
    <div className={`app-shell ${isIde ? 'ide-only-edition' : ''} ${isIde&&workspace?'ide-focused':''}`}>
      <aside className={`sidebar ${menu?'mobile-open':''}`}>
        <NavLink className="brand" to={isIde ? "/ide" : "/"} onClick={()=>setMenu(false)}>
          <span className="brand-mark" style={isIde ? {background:'rgba(0,194,255,0.15)',borderColor:'#00c2ff'} : {}}>
            <ForgeIcon size={26}/>
          </span>
          <span>
            devforge
            <span className="brand-suffix" style={isIde ? {color:'#00c2ff',fontWeight:700} : {}}>
              {isIde ? ' IDE' : ' IDE'}
            </span>
          </span>
        </NavLink>

        <div className="workspace-switch">
          <span className="avatar-mini" style={isIde ? {background:'linear-gradient(135deg, #00c2ff, #0284c7)',color:'#07192f'} : {}}>
            {isIde ? '⚡' : 'D'}
          </span>
          <div>
            <strong>{account.displayName}</strong>
            <small>{isIde ? 'Рабочая среда разработчика' : 'Ваша мастерская кода'}</small>
          </div>
          <ChevronDown size={14}/>
        </div>

        <span className="nav-label">{isIde ? 'DEVELOPER ENVIRONMENT' : 'WORKSPACE'}</span>
        <nav>
          {activeNav.map(([path,label,Icon])=>(
            <NavLink end={path==='/'||path==='/ide'} key={path} to={path} onClick={()=>setMenu(false)}>
              <Icon size={18}/>
              <span>{label}</span>
              {!isIde && label==='Learn' && (
                <small className="nav-count">{courses.reduce((n,c)=>n+c.lessons.length,0)}</small>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="local-card" style={isIde ? {borderLeftColor:'#00c2ff'} : {}}>
            <span className="green-dot" style={isIde ? {background:'#00c2ff',boxShadow:'0 0 8px #00c2ff'} : {}}/>
            <strong>{isIde ? 'DevForge IDE' : 'Всё на вашем устройстве'}</strong>
            <p>
              {isIde ? (
                <>15 языков, AST-структура,<br/>SQL и REST API в одном окне.</>
              ) : (
                <>Ваш код. Ваш темп.<br/>Без облачных сервисов.</>
              )}
            </p>
            {isIde ? <ForgeIcon size={16}/> : <WifiOff size={15}/>}
          </div>

          {!isIde && (
            <NavLink className="settings-link" to="/settings" onClick={()=>setMenu(false)}>
              <SettingsIcon size={18}/>Settings
            </NavLink>
          )}

          <div className="profile">
            <span className="avatar" style={isIde ? {background:'linear-gradient(135deg, #00c2ff, #0284c7)',color:'#07192f'} : {}}>
              {isIde ? <ForgeIcon size={16}/> : 'Y'}
            </span>
            <div>
              <strong>{account.displayName}</strong>
              <small style={isIde ? {color:'#00c2ff'} : {}}>
                {isIde ? 'Developer · Local Mode' : `${progress.xp} XP · Local account`}
              </small>
            </div>
            <button aria-label="Выйти" title="Выйти" onClick={()=>void logout().catch(e=>notify(String(e)))}>↪</button>
          </div>
        </div>
      </aside>

      <div className="app-main">
        <header className="topbar">
          <div className="topbar-left">
            {isIde&&workspace&&<ForgeIcon size={27}/>}
            <button className="mobile-menu" aria-label="Меню" onClick={()=>setMenu(!menu)}><Menu size={20}/></button>
            <span className="muted">{isIde ? 'DevForge IDE' : 'Workspace'}</span>
            <span className="slash">/</span>
            <strong>{title}</strong>
          </div>

          <div className="topbar-right">
            {isIde&&workspace&&<nav className="ide-quick-nav"><NavLink to="/ide">Редактор</NavLink><NavLink to="/projects">Проекты</NavLink><NavLink to="/settings">Настройки</NavLink></nav>}
            {isIde ? (
              <div style={{display:'flex',alignItems:'center',gap:'10px'}}>
                <span style={{display:'inline-flex',alignItems:'center',gap:'6px',padding:'4px 10px',borderRadius:'16px',background:'rgba(0,194,255,0.1)',border:'1px solid rgba(0,194,255,0.3)',color:'#00c2ff',fontSize:'12px',fontWeight:600}}>
                  <ForgeIcon size={14}/> Standalone IDE
                </span>
                <span className="build-label">v1.0.0 <ArrowUpRight size={12}/></span>
              </div>
            ) : (
              <>
                <div className="mode-switch">
                  <button className={settings.mode==='learning'?'selected':''} onClick={()=>updateSettings({mode:'learning'}).then(()=>navigate('/learn')).catch(e=>notify(String(e)))}>Learning</button>
                  <button className={settings.mode==='developer'?'selected':''} onClick={()=>updateSettings({mode:'developer'}).then(()=>navigate('/projects')).catch(e=>notify(String(e)))}>Developer</button>
                </div>
                <span className="build-label">v1.0.0 <ArrowUpRight size={12}/></span>
              </>
            )}
          </div>
        </header>

        <main className={workspace?'main-workspace':'main-content'}>
          {isIde ? (
            <Routes>
              <Route path="/" element={<Workspace/>}/>
              <Route path="/ide" element={<Workspace/>}/>
              <Route path="/projects" element={<Projects/>}/>
              <Route path="/projects/:projectId" element={<Workspace/>}/>
              <Route path="/documentation" element={<Documentation/>}/>
              <Route path="/settings" element={<SettingsPage/>}/>
              <Route path="*" element={<Workspace/>}/>
            </Routes>
          ) : (
            <Routes>
              <Route path="/" element={<Dashboard/>}/>
              <Route path="/assessment" element={<Assessment/>}/>
              <Route path="/learn" element={<Learn/>}/>
              <Route path="/learn/:lessonId" element={<Workspace/>}/>
              <Route path="/ide" element={<Workspace/>}/>
              <Route path="/challenges" element={<Challenges/>}/>
              <Route path="/documentation" element={<Documentation/>}/>
              <Route path="/projects" element={<Projects/>}/>
              <Route path="/projects/:projectId" element={<Workspace/>}/>
              <Route path="/progress" element={<ProgressPage/>}/>
              <Route path="/settings" element={<SettingsPage/>}/>
              <Route path="*" element={<div className="page"><h1>Страница не найдена</h1><NavLink to="/">На главную</NavLink></div>}/>
            </Routes>
          )}
        </main>
      </div>
    </div>
  );
}

export default function App(){
  return (
    <AuthGate>
      <StoreProvider>
        <Shell/>
      </StoreProvider>
    </AuthGate>
  );
}
