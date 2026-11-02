/** Public workbench registries. Add themes, commands and preferences here. */
import type {CSSProperties} from 'react';

export interface IDEPreferences {
  theme:'inherit'|'forge'|'code'|'graphite'|'nord'|'midnight'|'paper';
  accent:string; density:'compact'|'comfortable'; sidebarSide:'left'|'right'; sidebarWidth:number;
  panelPosition:'bottom'|'right'; panelHeight:number; panelWidth:number;
  activityBar:boolean; statusBar:boolean; breadcrumbs:boolean; centered:boolean;
  fontFamily:'cascadia'|'consolas'|'jetbrains'|'fira'|'monospace'; ligatures:boolean; lineHeight:number;
  tabSize:2|4|8; insertSpaces:boolean; wordWrap:'on'|'off'|'bounded'; lineNumbers:'on'|'off'|'relative';
  whitespace:'none'|'selection'|'all'; smoothScrolling:boolean; cursorStyle:'line'|'block'|'underline';
  cursorBlinking:'blink'|'smooth'|'solid'; bracketColors:boolean; indentGuides:boolean; stickyScroll:boolean;
  keymap:'code'|'jetbrains'; shortcuts:Partial<Record<CommandId,string>>; colors:Partial<Record<ColorToken,string>>;
}
export interface ProfilePreferences {theme:'dark'|'light';fontSize:number;minimap:boolean;inlineCompletion:boolean;ide:IDEPreferences}
export interface IDEProfile {id:string;name:string;preferences:ProfilePreferences}
export interface ProfileDocument {format:'devforge.ide-profile';version:1;profile:IDEProfile}
export const DEFAULT_IDE:IDEPreferences = {
  theme:'inherit',accent:'#68c6ff',density:'compact',sidebarSide:'left',sidebarWidth:248,
  panelPosition:'bottom',panelHeight:230,panelWidth:400,activityBar:true,statusBar:true,breadcrumbs:true,centered:false,
  fontFamily:'cascadia',ligatures:true,lineHeight:1.6,tabSize:4,insertSpaces:true,wordWrap:'off',lineNumbers:'on',
  whitespace:'selection',smoothScrolling:true,cursorStyle:'line',cursorBlinking:'smooth',bracketColors:true,
  indentGuides:true,stickyScroll:false,keymap:'code',shortcuts:{},colors:{}
};
export const FONTS = {
  cascadia: '"Cascadia Code", "Cascadia Mono", Consolas, monospace',
  consolas: 'Consolas, "Liberation Mono", monospace',
  jetbrains: '"JetBrains Mono", Consolas, monospace',
  fira: '"Fira Code", Consolas, monospace',
  monospace: 'monospace'
};
export type ColorToken = 'background'|'panel'|'editor'|'text'|'muted'|'border';
export interface WorkbenchTheme {id:Exclude<IDEPreferences['theme'],'inherit'>;name:string;description:string;light:boolean;colors:Record<ColorToken,string>;keyword:string;string:string;number:string}
export const THEMES:WorkbenchTheme[] = [
  {id:'forge',name:'Forge Blue',description:'Графит с голубым акцентом',light:false,colors:{background:'#16191f',panel:'#1b1e25',editor:'#20232b',text:'#dce1eb',muted:'#969eaf',border:'#303540'},keyword:'#a7baff',string:'#a6c99b',number:'#dfb481'},
  {id:'code',name:'Code Dark',description:'Нейтральный рабочий стол',light:false,colors:{background:'#181818',panel:'#1f1f1f',editor:'#1f1f1f',text:'#d4d4d4',muted:'#a1a1a1',border:'#363636'},keyword:'#82b9e8',string:'#ce9178',number:'#b5cea8'},
  {id:'graphite',name:'Graphite',description:'Тёплый графит',light:false,colors:{background:'#202124',panel:'#2b2d30',editor:'#24262a',text:'#d6d8dd',muted:'#a0a5b1',border:'#40434b'},keyword:'#d5a4f7',string:'#a8c58f',number:'#7bb7cf'},
  {id:'nord',name:'Nord',description:'Мягкие северные оттенки',light:false,colors:{background:'#242a36',panel:'#2e3440',editor:'#2e3440',text:'#eceff4',muted:'#b0bbcc',border:'#4c566a'},keyword:'#81a1c1',string:'#a3be8c',number:'#b48ead'},
  {id:'midnight',name:'Midnight',description:'Глубокая тёмная тема',light:false,colors:{background:'#090c14',panel:'#111624',editor:'#0c101b',text:'#e0e6f5',muted:'#99a6c1',border:'#2b3450'},keyword:'#b7a2ff',string:'#81d6c3',number:'#f2bf8e'},
  {id:'paper',name:'Paper Light',description:'Светлая, с чёткими границами',light:true,colors:{background:'#e9eef5',panel:'#f4f7fb',editor:'#ffffff',text:'#23344c',muted:'#586c85',border:'#c8d3e1'},keyword:'#6046b5',string:'#207644',number:'#a64c15'}
];
export const ACCENTS = ['#68c6ff','#739dff','#ad99ff','#ed9ac7','#efb778','#8bd4af','#66cfd1','#b9cf71'];
export function resolveTheme(ide:IDEPreferences,base:'dark'|'light') {
  return THEMES.find(t=>t.id===(ide.theme==='inherit'?(base==='light'?'paper':'forge'):ide.theme)) || THEMES[0];
}
export function workbenchStyle(ide:IDEPreferences,base:'dark'|'light'):CSSProperties {
  const theme=resolveTheme(ide,base),colors={...theme.colors,...ide.colors};
  return Object.fromEntries([
    ...Object.entries(colors).map(([k,v])=>[`--ide-${k}`,v]),['--ide-accent',ide.accent],
    ['--ide-sidebar-width',`${ide.sidebarWidth}px`],['--ide-panel-height',`${ide.panelHeight}px`],
    ['--ide-panel-width',`${ide.panelWidth}px`]
  ]) as CSSProperties;
}
export const COMMANDS = [
  {id:'run',label:'Запустить файл',code:'Ctrl+Enter',jetbrains:'Shift+F10'},
  {id:'save',label:'Сохранить все файлы',code:'Ctrl+S'},
  {id:'format',label:'Форматировать документ',code:'Alt+Shift+F',jetbrains:'Ctrl+Alt+L'},
  {id:'split',label:'Разделить редактор',code:'Ctrl+Backslash'},
  {id:'palette',label:'Палитра команд',code:'Ctrl+Shift+P'},
  {id:'files',label:'Быстрый переход к файлу',code:'Ctrl+P',jetbrains:'Ctrl+Shift+N'},
  {id:'search',label:'Поиск по проекту',code:'Ctrl+Shift+F'},
  {id:'terminal',label:'Открыть терминал',code:'Ctrl+Backquote',jetbrains:'Alt+F12'},
  {id:'sidebar',label:'Переключить боковую панель',code:'Ctrl+B',jetbrains:'Alt+1'},
  {id:'panel',label:'Переключить панель инструментов',code:'Ctrl+J'},
  {id:'settings',label:'Настроить IDE',code:'Ctrl+Comma',jetbrains:'Ctrl+Alt+S'},
  {id:'zen',label:'Режим фокуса',code:'Ctrl+Shift+F12'},
  {id:'previousTab',label:'Предыдущий файл',code:'Alt+ArrowLeft'},
  {id:'nextTab',label:'Следующий файл',code:'Alt+ArrowRight'}
] as const;
export type CommandId = typeof COMMANDS[number]['id'];
export function bindings(ide:IDEPreferences):Record<CommandId,string> {
  return Object.fromEntries(COMMANDS.map(c=>[c.id,ide.shortcuts[c.id]??(ide.keymap==='jetbrains'&&'jetbrains' in c?c.jetbrains:c.code)])) as Record<CommandId,string>;
}
export function keyString(e:Pick<KeyboardEvent,'code'|'ctrlKey'|'metaKey'|'altKey'|'shiftKey'>) {
  const key=e.code.replace(/^Key/,'').replace(/^Digit/,'');
  if(/^(Control|Shift|Alt|Meta)/.test(key))return '';
  return `${e.ctrlKey||e.metaKey?'Ctrl+':''}${e.altKey?'Alt+':''}${e.shiftKey?'Shift+':''}${key}`;
}
export function displayKey(key:string) {
  return key.replace('Backquote','`').replace('Backslash','\\').replace('Comma',',').replace('Period','.').replace('ArrowLeft','←').replace('ArrowRight','→') || 'Не назначено';
}
export function shortcutErrors(ide:IDEPreferences):string[] {
  const used=new Map<string,string>(),errors:string[]=[];
  const pattern=/^(?:Ctrl\+)?(?:Alt\+)?(?:Shift\+)?(?:[A-Z0-9]|F(?:[1-9]|1[0-2])|Enter|Backslash|Backquote|Comma|Period|ArrowLeft|ArrowRight)$/;
  const reserved=new Set(['Ctrl+W','Ctrl+T','Ctrl+N','Ctrl+R','Ctrl+L','Ctrl+Tab','Ctrl+Shift+W','Ctrl+Shift+T','Alt+F4','Ctrl+Alt+Delete','F1']);
  for(const c of COMMANDS){const key=bindings(ide)[c.id];if(!key)continue;
    if(!pattern.test(key)||(!key.includes('Ctrl+')&&!key.includes('Alt+')&&!/F\d+$/.test(key))||reserved.has(key))errors.push(`${c.label}: недопустимое или системное сочетание.`);
    if(used.has(key))errors.push(`${displayKey(key)}: «${used.get(key)}» и «${c.label}».`);
    used.set(key,c.label);
  }
  return errors;
}
export const LAYOUT_PRESETS: {id:string;name:string;description:string;patch:Partial<IDEPreferences>}[] = [
  {id:'code',name:'Code',description:'Компактные вкладки, проводник слева, вывод снизу.',patch:{density:'compact',sidebarSide:'left',sidebarWidth:248,panelPosition:'bottom',panelHeight:230,activityBar:true,statusBar:true,breadcrumbs:true,centered:false,keymap:'code',shortcuts:{}}},
  {id:'studio',name:'Studio',description:'Свободные отступы, инструменты справа, схема JetBrains.',patch:{density:'comfortable',sidebarSide:'left',sidebarWidth:270,panelPosition:'right',panelWidth:400,activityBar:true,statusBar:true,breadcrumbs:true,centered:false,keymap:'jetbrains',shortcuts:{}}},
  {id:'writer',name:'Focus',description:'Центрированный код и минимум визуального шума.',patch:{density:'comfortable',sidebarSide:'left',panelPosition:'bottom',activityBar:false,statusBar:true,breadcrumbs:false,centered:true}}
];
