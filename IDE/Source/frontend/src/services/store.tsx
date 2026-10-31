import {createContext,useContext,useEffect,useRef,useState,type ReactNode} from 'react';
import {api} from './api';
import type {Course,Doc,Language,Progress,Project,Settings,LearningPlan,Account,Track} from '../types';
import {prewarm,clearRunners} from '../runners/runner';
import {useAuth} from './auth';
import type {IDEPreferences} from '../ide/config';
interface State {courses:Course[];languages:Language[];docs:Doc[];projects:Project[];progress:Progress;settings:Settings;plan:LearningPlan;tracks:Track[]}
interface Store extends State {account:Account;refresh:()=>Promise<void>;updateSettings:(patch:Partial<Settings>)=>Promise<void>;updateIDE:(patch:Partial<IDEPreferences>)=>Promise<void>;notify:(message:string)=>void}
const Context=createContext<Store|null>(null);
export const useStore=()=>{const store=useContext(Context);if(!store)throw new Error('Missing store');return store;};
export function StoreProvider({children}:{children:ReactNode}) {
  const {account}=useAuth();
  const [data,setData]=useState<State|null>(null),[error,setError]=useState(''),[toast,setToast]=useState('');
  const settingsRef=useRef<Settings|null>(null),settingsQueue=useRef(Promise.resolve());
  async function refresh() {
    const [courses,languages,docs,projects,progress,settings,plan,tracks]=await Promise.all([api<Course[]>('/courses'),api<Language[]>('/languages'),api<Doc[]>('/documentation'),api<Project[]>('/projects'),api<Progress>('/progress'),api<Settings>('/settings'),api<LearningPlan>('/learning-plan'),api<Track[]>('/tracks').catch(()=>[])]);
    settingsRef.current=settings;setData({courses,languages,docs,projects,progress,settings,plan,tracks});setError('');
  }
  useEffect(()=>{refresh().catch(e=>setError(String(e)));prewarm();return()=>clearRunners();},[]);
  useEffect(()=>{if(data)document.documentElement.dataset.theme=data.settings.theme;},[data?.settings.theme]);
  useEffect(()=>{if(!toast)return;const id=setTimeout(()=>setToast(''),6000);return()=>clearTimeout(id);},[toast]);
  function saveSettings(patch:Partial<Settings>,idePatch?:Partial<IDEPreferences>):Promise<void>{
    const task=settingsQueue.current.then(async()=>{
      if(!settingsRef.current)return;
      const merged={...settingsRef.current,...patch};
      if(idePatch)merged.ide={...merged.ide,...idePatch};
      const settings=await api<Settings>('/settings','PUT',merged);
      settingsRef.current=settings;
      setData(current=>current?{...current,settings}:current);
    });
    settingsQueue.current=task.catch(()=>{});
    return task;
  }
  const updateSettings=(patch:Partial<Settings>)=>saveSettings(patch);
  const updateIDE=(patch:Partial<IDEPreferences>)=>saveSettings({},patch);
  if(error&&!data)return <div className="boot"><h1>DevForge</h1><p>Не удалось подключиться к локальному серверу.</p><pre>{error}</pre><p>Запустите start.bat в папке проекта.</p><button onClick={()=>refresh().catch(e=>setError(String(e)))}>Повторить</button></div>;
  if(!data)return <div className="boot"><span className="brand-mark">⌘</span><h1>DevForge</h1><p>Открываем вашу мастерскую…</p></div>;
  return <Context.Provider value={{...data,account,refresh,updateSettings,updateIDE,notify:setToast}}>{children}{toast&&<div role="status" className="toast" onClick={()=>setToast('')}>{toast}</div>}</Context.Provider>;
}
