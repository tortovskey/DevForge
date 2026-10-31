import {createContext,useContext,useEffect,useState,type ReactNode} from 'react';
import {useNavigate} from 'react-router-dom';
import {ArrowRight,LockKeyhole,UserRound,Monitor,Code2} from 'lucide-react';
import {api} from './api';
import type {Account} from '../types';
import {ForgeIcon} from '../components/ForgeIcon';

const AuthContext=createContext<{account:Account;logout:()=>Promise<void>;isIde:boolean}|null>(null);
export function useAuth(){const auth=useContext(AuthContext);if(!auth)throw new Error('Authentication required');return auth;}

export function AuthGate({children}:{children:ReactNode}){
  const [account,setAccount]=useState<Account|null>(null),[ready,setReady]=useState(false),[isIde,setIsIde]=useState(false),[mode,setMode]=useState<'login'|'register'>('login');
  const [name,setName]=useState(''),[username,setUsername]=useState(''),[password,setPassword]=useState(''),[error,setError]=useState(''),[busy,setBusy]=useState(false);
  const navigate=useNavigate();

  useEffect(()=>{
    (async()=>{
      try {
        const [status, platform] = await Promise.all([
          api<{hasAccounts:boolean; isIde?:boolean; authOptional?:boolean}>('/auth/status').catch(()=>({hasAccounts:false,isIde:false,authOptional:false})),
          api<{platform:string; mode?:string}>('/platform').catch(()=>({platform:'desktop',mode:'full'}))
        ]);

        const ideMode = Boolean(status.isIde || status.authOptional || platform.mode === 'ide' || window.location.pathname === '/ide');
        setIsIde(ideMode);

        if(!status.hasAccounts) setMode('register');

        const response = await fetch('/api/auth/me');
        if (response.ok) {
          setAccount(await response.json());
        } else if (ideMode) {
          // In IDE mode, registration is NOT required: auto-enter as local Developer profile
          const guest = await api<Account>('/auth/guest', 'POST', {}).catch(()=>null);
          if (guest) setAccount(guest);
        }
      } catch(e) {
        setError('Не удалось подключиться к локальному серверу. '+String(e));
      } finally {
        setReady(true);
      }
    })();

    const expired=()=>setAccount(null);
    window.addEventListener('devforge:session-expired',expired);
    return()=>window.removeEventListener('devforge:session-expired',expired);
  },[]);

  async function submit(e:React.FormEvent){
    e.preventDefault();setBusy(true);setError('');
    try {
      const next=await api<Account>(`/auth/${mode}`,'POST',mode==='register'?{username,password,displayName:name}:{username,password});
      setAccount(next);setPassword('');
      if(mode==='register')navigate(isIde ? '/ide' : '/assessment');
    } catch(e){setError(String(e));}
    finally{setBusy(false);}
  }

  async function loginAsGuest(){
    setBusy(true);setError('');
    try {
      const guest = await api<Account>('/auth/guest', 'POST', {});
      setAccount(guest);
      navigate(isIde ? '/ide' : '/');
    } catch(e) {
      setError(String(e));
    } finally {
      setBusy(false);
    }
  }

  async function logout(){
    await api('/auth/logout','POST',{});
    setAccount(null);setMode('login');setPassword('');navigate('/');
  }

  if(!ready) return (
    <div className="boot">
      <span className="brand-mark"><ForgeIcon size={32}/></span>
      <p>Запуск DevForge {isIde ? 'Fusion IDE' : '1.0.0'}…</p>
    </div>
  );

  if(!account) return (
    <div className="auth-page">
      <div className="auth-intro">
        <span className="brand">
          <span className="brand-mark"><ForgeIcon size={30}/></span>
          devforge {isIde ? 'FUSION IDE' : 'IDE'} <small>1.0.0</small>
        </span>
        <span className="eyebrow">
          {isIde ? 'PROFESSIONAL MULTI-LANGUAGE IDE' : 'FROM YOUR FIRST LINE TO YOUR NEXT IDEA'}
        </span>
        <h1>
          {isIde ? (
            <>Среда разработки.<br/><span>Без лишних ограничений.</span></>
          ) : (
            <>Ваш путь в программирование.<br/><span>С самого начала.</span></>
          )}
        </h1>
        <p>
          {isIde
            ? 'Полноценный редактор кода, AST-структура, SQL-консоль, REST API клиент и запуск программ на 15 языках — всё автономно на вашем компьютере.'
            : '377 уроков и 3 карьерных трека: Backend, Frontend и Java. 15 языков, интерактивные подсказки и проекты — всё на вашем компьютере.'}
        </p>
        <div className="auth-features">
          <span><ForgeIcon size={18}/>Fusion IDE</span>
          <span><Monitor size={18}/>Desktop + Web</span>
          <span><LockKeyhole size={18}/>100% Offline</span>
        </div>
      </div>

      <form className="auth-card" onSubmit={submit}>
        <span className="eyebrow">{isIde ? 'БЫСТРЫЙ СТАРТ В IDE' : 'ВАША ЛИЧНАЯ МАСТЕРСКАЯ'}</span>
        <h2>{isIde ? 'Добро пожаловать в IDE' : (mode==='register'?'Начнём знакомство':'С возвращением')}</h2>
        <p>
          {isIde
            ? 'В DevForge IDE регистрация не обязательна. Вы можете начать кодить сразу.'
            : (mode==='register'?'Аккаунт создаётся только на этом устройстве.':'Войдите, чтобы продолжить с того же места.')}
        </p>

        {/* Prominent Instant Guest Access Button */}
        <button
          type="button"
          className="primary wide"
          style={{background:'linear-gradient(135deg, #00c2ff 0%, #0284c7 100%)',color:'#07192f',fontWeight:700,marginBottom:'12px'}}
          disabled={busy}
          onClick={loginAsGuest}
        >
          <Code2 size={18}/> Продолжить без регистрации (Гость)
        </button>

        <div style={{display:'flex',alignItems:'center',gap:'10px',margin:'10px 0',color:'#64748b',fontSize:'12px'}}>
          <hr style={{flex:1,borderColor:'#334155'}}/> или войти в локальный профиль <hr style={{flex:1,borderColor:'#334155'}}/>
        </div>

        {mode==='register'&&<label>Ваше имя<input autoComplete="name" maxLength={60} required value={name} onChange={e=>setName(e.target.value)}/></label>}
        <label>Логин<input autoComplete="username" pattern="[a-zA-Z0-9_]+" minLength={3} maxLength={32} title="Латинские буквы, цифры и подчёркивание" required value={username} onChange={e=>setUsername(e.target.value)}/></label>
        <label>Пароль<input type="password" autoComplete={mode==='register'?'new-password':'current-password'} minLength={mode==='register'?8:1} maxLength={128} required value={password} onChange={e=>setPassword(e.target.value)}/></label>
        {mode==='register'&&<small className="muted">Не менее 8 символов. Восстановление по почте не предусмотрено.</small>}
        {error&&<p role="alert" className="error-text">{error}</p>}
        <button className="wide secondary" disabled={busy}>
          {busy?'Подождите…':mode==='register'?'Создать профиль':'Войти'}
          <ArrowRight size={16}/>
        </button>
        <button type="button" className="wide text-button" onClick={()=>{setMode(mode==='login'?'register':'login');setError('');}}>
          {mode==='register'?'Уже есть профиль? Войти':'Создать именованный профиль'}
        </button>
        <div className="auth-private"><UserRound size={16}/>Все проекты и файлы сохраняются локально.</div>
      </form>
    </div>
  );

  return <AuthContext.Provider value={{account,logout,isIde}}><div key={account.id}>{children}</div></AuthContext.Provider>;
}
