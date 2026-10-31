import type {LanguageId,RunRequest,RunResult} from '../types';
export interface CodeRunner {run(request:RunRequest):Promise<RunResult>;stop():void;reset():void;warm():Promise<void>}
export class BrowserRunner implements CodeRunner {
  private worker:Worker|null=null;
  private ready:Promise<void>|null=null;
  private bootReject:((error:Error)=>void)|null=null;
  private bootTimer:ReturnType<typeof setTimeout>|null=null;
  private pending:((result:RunResult)=>void)|null=null;
  private cancel:(()=>void)|null=null;
  private context:string|null=null;
  private phase:((phase:string)=>void)|null=null;
  private inputBuffer:SharedArrayBuffer|null=null;
  onInputRequest:(prompt:string)=>Promise<string|null>=async()=>null;
  onInputCancel:()=>void=()=>{};
  onStatus:(status:string)=>void;
  constructor(private language:LanguageId,onStatus:(status:string)=>void=()=>{},private timeout=5000){this.onStatus=onStatus;}
  warm():Promise<void>{
    if(this.ready)return this.ready;
    this.onStatus('Подготовка среды…');
    this.ready=new Promise((resolve,reject)=>{
      this.bootReject=reject;
      this.worker=new Worker(`/workers/${this.language}.js`,this.language==='postgresql'?{type:'module'}:undefined);
      this.bootTimer=setTimeout(()=>this.failBoot('Загрузка Worker превысила 45 секунд'),45000);
      this.worker.onmessage=(event:MessageEvent)=>{
        if(event.data.type==='ready'){if(this.bootTimer)clearTimeout(this.bootTimer);this.bootTimer=null;this.bootReject=null;this.onStatus('Среда готова');resolve();}
        else if(event.data.type==='boot-error')this.failBoot(String(event.data.error));
        else if(event.data.type==='phase')this.phase?.(event.data.phase);
        else if(event.data.type==='input-request'){
          const shared=this.inputBuffer;
          if(!shared)return;
          this.phase?.('input');
          const view=new Int32Array(shared,0,2),bytes=new Uint8Array(shared,8);
          void this.onInputRequest(String(event.data.prompt||'')).then(value=>{
            if(!this.worker||this.inputBuffer!==shared)return;
            if(value===null)Atomics.store(view,0,2);
            else{
              const encoded=new TextEncoder().encode(value);
              bytes.set(encoded.subarray(0,bytes.length));
              Atomics.store(view,1,Math.min(encoded.length,bytes.length));
              Atomics.store(view,0,1);
            }
            Atomics.notify(view,0);
            this.phase?.('run');
          }).catch(()=>{if(this.inputBuffer===shared){Atomics.store(view,0,2);Atomics.notify(view,0);this.phase?.('run');}});
        }
        else if(event.data.type==='result')this.pending?.(event.data.result);
      };
      this.worker.onerror=event=>{if(this.bootReject)this.failBoot(event.message);else{this.pending?.({stdout:'',stderr:'',tables:[],results:[],error:event.message});this.reset();}};
    });
    return this.ready;
  }
  private failBoot(message:string){const reject=this.bootReject;this.bootReject=null;this.destroy();reject?.(new Error(`Не удалось загрузить локальную среду: ${message}`));}
  private destroy(){if(this.bootTimer)clearTimeout(this.bootTimer);this.bootTimer=null;this.worker?.terminate();this.worker=null;this.ready=null;this.context=null;}
  run(request:RunRequest):Promise<RunResult>{
    if(this.cancel)return Promise.reject(new Error('Дождитесь текущего запуска'));
    return new Promise(resolve=>{
      let finished=false,timer:ReturnType<typeof setTimeout>|undefined,executionStart=0,inputStart=0,inputDuration=0;
      const finish=(result:RunResult)=>{if(finished)return;finished=true;if(timer)clearTimeout(timer);this.pending=null;this.cancel=null;this.phase=null;this.inputBuffer=null;this.onStatus('Готово');resolve({...result,duration:executionStart?performance.now()-executionStart-inputDuration-(inputStart?performance.now()-inputStart:0):0});};
      const interrupt=(message:string)=>{this.onInputCancel();finish({stdout:'',stderr:'',tables:[],results:[],error:message});const reject=this.bootReject;this.bootReject=null;this.destroy();reject?.(new Error(message));};
      this.cancel=()=>interrupt('Выполнение остановлено. Среда перезапустится при следующем запуске.');

      this.warm().then(()=>{
        // Stop/reset may finish the run while the runtime is still loading.
        if(finished)return;
        this.pending=finish;
        executionStart=performance.now();this.onStatus('Выполнение…');
        const arm=(ms:number)=>{if(timer)clearTimeout(timer);timer=setTimeout(()=>interrupt(`Timeout: превышен лимит ${ms/1000} с. Worker завершён.`),ms);};
        this.phase=phase=>{
          this.onStatus(phase==='compile'?'Компиляция…':phase==='input'?'Ожидание ввода…':'Выполнение…');
          if(phase==='input'){if(!inputStart)inputStart=performance.now();if(timer)clearTimeout(timer);}
          else {if(inputStart){inputDuration+=performance.now()-inputStart;inputStart=0;}arm(phase==='compile'?30000:this.timeout);}
        };
        arm(['c','cpp','csharp','objc','rust','java'].includes(this.language)?30000:this.timeout);
        const context=request.context||'';
        const reset=request.reset||context!==this.context;this.context=context;
        this.inputBuffer=this.language==='python'&&typeof SharedArrayBuffer!=='undefined'?new SharedArrayBuffer(4104):null;
        this.worker!.postMessage({...request,reset,inputBuffer:this.inputBuffer});
      }).catch(error=>{if(!finished){interrupt(String(error));}});
    });
  }
  stop(){this.cancel?.();}
  reset(){this.stop();const reject=this.bootReject;this.bootReject=null;this.destroy();reject?.(new Error('Среда сброшена'));}
}
const pool=new Map<LanguageId,BrowserRunner>();
export function getRunner(language:LanguageId,onStatus:(status:string)=>void=()=>{}){
  if(!pool.has(language))pool.set(language,new BrowserRunner(language));
  const runner=pool.get(language)!;runner.onStatus=onStatus;return runner;
}
export function clearRunners(){for(const runner of pool.values())runner.reset();pool.clear();}
export function prewarm(){for(const language of ['python','sql'] as const)void getRunner(language).warm().catch(()=>{});}
