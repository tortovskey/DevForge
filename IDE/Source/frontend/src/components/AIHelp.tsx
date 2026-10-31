import {useState} from 'react';
import {Link} from 'react-router-dom';
import {Send,Sparkles,Copy,Plus} from 'lucide-react';
import {useStore} from '../services/store';
import {api} from '../services/api';
export default function AIHelp({code,language,onInsert}:{code:string;language:string;onInsert:(value:string)=>void}){
  const {settings,notify}=useStore();const [question,setQuestion]=useState(''),[answer,setAnswer]=useState(''),[busy,setBusy]=useState(false);
  async function ask(e:React.FormEvent){e.preventDefault();setBusy(true);try{const result=await api<{text:string}>('/ai/generate','POST',{prompt:question,code:code.slice(0,14000),language,mode:'chat'});setAnswer(result.text);}catch(e){setAnswer(String(e));}finally{setBusy(false);}}
  const snippet=answer.match(/```[^\n]*\n([\s\S]*?)```/)?.[1];
  return <section className="ai-help"><div className="section-heading"><h3><Sparkles size={16}/>Локальный помощник</h3><span className="pill">{settings.aiModel||'Модель не выбрана'}</span></div>{settings.aiProvider==='disabled'||!settings.aiModel?<div className="note">Выберите установленную модель в <Link to="/settings">настройках локального ИИ</Link>. Код отправляется только провайдеру на этом компьютере.</div>:<><form onSubmit={ask}><textarea aria-label="Вопрос локальному помощнику" value={question} onChange={e=>setQuestion(e.target.value)} maxLength={6000} placeholder="Объясни ошибку или помоги написать функцию…" required/><button className="primary" disabled={busy}>{busy?'Модель думает…':'Спросить'}<Send size={15}/></button></form>{answer&&<><pre className="ai-answer">{answer}</pre><div className="toolbar-actions"><button onClick={()=>navigator.clipboard.writeText(answer).then(()=>notify('Ответ скопирован')).catch(()=>notify('Буфер обмена недоступен'))}><Copy size={14}/>Копировать</button>{snippet&&<button onClick={()=>onInsert(code+'\n'+snippet)}><Plus size={14}/>Добавить код в конец файла</button>}</div><small className="muted">Модель может ошибаться. Проверьте предложенный код перед запуском.</small></>}</>}</section>;
}
