export type LanguageId = 'python' | 'sql' | 'postgresql' | 'html-css' | 'c' | 'javascript' | 'typescript' | 'java' | 'cpp' | 'csharp' | 'objc' | 'rust' | '1c' | 'lua' | 'assembly';
export interface Language {id:string; name:string; extension:string; editorLanguage:string; runnerType:string; status:'available'|'planned'; description:string; supportedFeatures:string[]}
export interface Test {id:string; label:string; expression?:string; query?:string; expected:unknown;stdin?:string;viewport?:number;focus?:boolean;dom?:{selector:string;property:string;attribute?:string;css?:string}}
export interface TeachingGuide {version:number;idea:string;steps:string[];experiment:string;terms:{term:string;meaning:string}[];solution:string;taskSteps:string[];checklist:string[];taskTables:{name:string;columns:string[];values:unknown[][]}[];example:{code:string;expected:unknown;setupSql:string;kind:string;dom?:Test["dom"];tables:{name:string;columns:string[];values:unknown[][]}[]}}
export interface Lesson {guide?:TeachingGuide;stdin?:string;resources?:{title:string;url:string;language:string}[];lifeExample?:string;challenge?:string;id:string;language:LanguageId;title:string;topic:string;section:string;order:number;level:string;minutes:number;theory:string;syntax:string;examples:string[];task:string;starterCode:string;tests:Test[];hints:string[];commonMistakes:string;solutionExplanation:string;xp:number;setupSql:string;concepts:string[];walkthrough:string[];prerequisites:string[]}
export interface Course {id:LanguageId;name:string;lessons:Lesson[]}
export interface Doc {id:string;title:string;language:LanguageId;category:string;explanation:string;syntax:string;example:string;mistakes:string;relatedLessons:string[]}
export interface ProjectFile {name:string;content:string}
export interface Project {id:string;name:string;language:LanguageId;files:ProjectFile[];revision:number;updated_at:string}
export interface Progress {completed:string[];xp:number;attemptCount:number;attempts:{id:string;lesson_id:string;passed:number;total:number;created_at:string}[];streak?:number;lastActiveDate?:string;badges?:string[]}
export interface Settings {theme:'dark'|'light';fontSize:number;mode:'learning'|'developer';lastLesson:string|null;aiProvider:'disabled'|'ollama'|'lmstudio'|'openai-local';aiPort:number;aiModel:string;inlineCompletion:boolean;aiCompletion:boolean;minimap?:boolean;ide:import('../ide/config').IDEPreferences;ideProfiles:import('../ide/config').IDEProfile[]}
export interface TestResult {id:string;actual:unknown;error?:string|null}
export interface Table {columns:string[];values:(string|number|null)[][]}
export interface RunResult {stdout:string;stderr:string;tables:Table[];results:TestResult[];error?:string;duration?:number;registers?:Record<string,string|number>}
export interface RunRequest {stdin?:string;code:string;tests?:Test[];setupSql?:string;check?:boolean;reset?:boolean;files?:ProjectFile[];filename?:string;context?:string}
export interface Account {id:string;username:string;displayName:string}
export interface AssessmentResult {language:LanguageId;score:number;total:number;level:string;preliminary:boolean;results:{id:string;tag:string;correct:boolean;expected:number;explanation:string}[]}
export interface LearningPlan {courses:{language:LanguageId;assessment:AssessmentResult|null;recommended:string[];review:string[];nextLesson:string|null;completed:number;total:number}[];notice:string}
export const LANGUAGE_NAMES:Record<LanguageId,string>={
  c:'C',
  cpp:'C++',
  csharp:'C#',
  objc:'Objective-C',
  rust:'Rust',
  '1c':'1С:Предприятие',
  python:'Python',
  sql:'SQL / SQLite',
  postgresql:'PostgreSQL',
  'html-css':'HTML / CSS',
  javascript:'JavaScript',
  typescript:'TypeScript',
  java:'Java',
  lua:'Lua',
  assembly:'Assembly (x86-64 NASM)'
};
export const EXTENSIONS:Record<LanguageId,string>={
  c:'.c',
  cpp:'.cpp',
  csharp:'.cs',
  objc:'.m',
  rust:'.rs',
  '1c':'.bsl',
  python:'.py',
  sql:'.sql',
  postgresql:'.sql',
  'html-css':'.html',
  javascript:'.js',
  typescript:'.ts',
  java:'.java',
  lua:'.lua',
  assembly:'.asm'
};

export interface TrackModule {
  id: string;
  title: string;
  skills: string[];
  lessonIds: string[];
}

export interface TrackCapstone {
  id: string;
  title: string;
  description: string;
  deliverables: string[];
}

export interface Track {
  id: string;
  title: string;
  kicker: string;
  description: string;
  targetRole: string;
  level: string;
  icon: string;
  badge: string;
  stack: string[];
  modules: TrackModule[];
  capstone: TrackCapstone;
}
