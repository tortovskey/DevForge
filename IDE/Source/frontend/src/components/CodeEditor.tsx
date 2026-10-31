import Editor,{loader} from '@monaco-editor/react';
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api';
import 'monaco-editor/esm/vs/editor/editor.all';
// Load syntax support only for the languages offered by DevForge.
import 'monaco-editor/esm/vs/basic-languages/python/python.contribution';
import 'monaco-editor/esm/vs/basic-languages/sql/sql.contribution';
import 'monaco-editor/esm/vs/basic-languages/pgsql/pgsql.contribution';
import 'monaco-editor/esm/vs/basic-languages/html/html.contribution';
import 'monaco-editor/esm/vs/basic-languages/css/css.contribution';
import 'monaco-editor/esm/vs/basic-languages/cpp/cpp.contribution';
import 'monaco-editor/esm/vs/basic-languages/csharp/csharp.contribution';
import 'monaco-editor/esm/vs/basic-languages/java/java.contribution';
import 'monaco-editor/esm/vs/basic-languages/javascript/javascript.contribution';
import 'monaco-editor/esm/vs/basic-languages/typescript/typescript.contribution';
import 'monaco-editor/esm/vs/basic-languages/objective-c/objective-c.contribution';
import 'monaco-editor/esm/vs/basic-languages/rust/rust.contribution';
import 'monaco-editor/esm/vs/basic-languages/lua/lua.contribution';
import EditorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';
import {useStore} from '../services/store';
import {useEffect,useRef} from 'react';
import {registerInline} from '../features/completions';
import {registerIntelligence} from '../features/intelligence';
import {FONTS,resolveTheme} from '../ide/config';
import type {Settings} from '../types';

// Explicit local Monaco loader: @monaco-editor/react's default CDN is never used.
self.MonacoEnvironment={getWorker:()=>new EditorWorker()};
loader.config({monaco});

let intelligenceRegistered = false;
function initMonacoThemes() {
  if (intelligenceRegistered) return;
  intelligenceRegistered = true;

  monaco.editor.defineTheme('devforge-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'comment', foreground: '717b8f', fontStyle: 'italic' },
      { token: 'keyword', foreground: '799eff', fontStyle: 'bold' },
      { token: 'identifier', foreground: 'e6edf3' },
      { token: 'string', foreground: '69cfac' },
      { token: 'number', foreground: 'f0883e' },
      { token: 'type', foreground: 'd2a8ff' }
    ],
    colors: {
      'editor.background': '#13161c',
      'editor.foreground': '#e6edf3',
      'editor.lineHighlightBackground': '#181c24',
      'editorCursor.foreground': '#799eff',
      'editorWhitespace.foreground': '#252a35',
      'editorIndentGuide.background1': '#202530',
      'editorIndentGuide.activeBackground1': '#3a4459'
    }
  });

  monaco.editor.defineTheme('devforge-light', {
    base: 'vs',
    inherit: true,
    rules: [
      { token: 'comment', foreground: '6e7781', fontStyle: 'italic' },
      { token: 'keyword', foreground: '0969da', fontStyle: 'bold' },
      { token: 'string', foreground: '1a7f37' },
      { token: 'number', foreground: '953800' }
    ],
    colors: {
      'editor.background': '#ffffff',
      'editor.foreground': '#1f2328',
      'editor.lineHighlightBackground': '#f6f8fa',
      'editorCursor.foreground': '#0969da'
    }
  });

  monaco.editor.defineTheme('jetbrains-darcula', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'comment', foreground: '808080', fontStyle: 'italic' },
      { token: 'keyword', foreground: 'cc7832', fontStyle: 'bold' },
      { token: 'identifier', foreground: 'a9b7c6' },
      { token: 'string', foreground: '6a8759' },
      { token: 'number', foreground: '6897bb' },
      { token: 'type', foreground: 'ffc66d' }
    ],
    colors: {
      'editor.background': '#2b2b2b',
      'editor.foreground': '#a9b7c6',
      'editor.lineHighlightBackground': '#323232',
      'editorCursor.foreground': '#bbbbbb',
      'editorWhitespace.foreground': '#3b3b3b',
      'editorIndentGuide.background1': '#3b3b3b',
      'editorIndentGuide.activeBackground1': '#555555'
    }
  });

  monaco.editor.defineTheme('github-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'comment', foreground: '8b949e', fontStyle: 'italic' },
      { token: 'keyword', foreground: 'ff7b72', fontStyle: 'bold' },
      { token: 'identifier', foreground: 'c9d1d9' },
      { token: 'string', foreground: 'a5d6ff' },
      { token: 'number', foreground: '79c0ff' },
      { token: 'type', foreground: 'd2a8ff' }
    ],
    colors: {
      'editor.background': '#0d1117',
      'editor.foreground': '#c9d1d9',
      'editor.lineHighlightBackground': '#161b22',
      'editorCursor.foreground': '#58a6ff'
    }
  });

  registerIntelligence(monaco);
}

export interface CodeEditorProps {
  code: string;
  onChange: (value: string) => void;
  language: string;
  path: string;
  customTheme?: string;
  onMount?: (editor: monaco.editor.IStandaloneCodeEditor, monacoInstance: typeof monaco) => void;
  onCursorChange?: (line: number, column: number) => void;
}

function defineWorkbenchTheme(settings:Settings){
  const theme=resolveTheme(settings.ide,settings.theme),c={...theme.colors,...settings.ide.colors};
  monaco.editor.defineTheme('devforge-workbench',{
    base:theme.light?'vs':'vs-dark',inherit:true,
    rules:[{token:'comment',foreground:c.muted.slice(1),fontStyle:'italic'},
      {token:'keyword',foreground:theme.keyword.slice(1)},{token:'string',foreground:theme.string.slice(1)},
      {token:'number',foreground:theme.number.slice(1)}],
    colors:{'editor.background':c.editor,'editor.foreground':c.text,
      'editorLineNumber.foreground':c.muted,'editorLineNumber.activeForeground':c.text,
      'editor.lineHighlightBackground':c.panel,'editorCursor.foreground':settings.ide.accent,
      'editor.selectionBackground':settings.ide.accent+'40','editor.inactiveSelectionBackground':settings.ide.accent+'22',
      'editorIndentGuide.background1':c.border,'editorIndentGuide.activeBackground1':c.muted,
      'editorWhitespace.foreground':c.border,'editorWidget.background':c.panel,
      'editorWidget.border':c.border,'editorSuggestWidget.background':c.panel,
      'editorSuggestWidget.foreground':c.text,'editorSuggestWidget.border':c.border,
      'editorSuggestWidget.selectedBackground':settings.ide.accent+'30',
      'editorHoverWidget.background':c.panel,'editorHoverWidget.foreground':c.text,
      'editorHoverWidget.border':c.border,'editorStickyScroll.background':c.editor}
  });
}

export default function CodeEditor({code,onChange,language,path,customTheme,onMount,onCursorChange}:CodeEditorProps) {
  const {settings}=useStore();
  const current=useRef(settings);current.current=settings;

  useEffect(()=>{
    initMonacoThemes();
    const provider=registerInline(monaco,()=>current.current);
    return()=>provider.dispose();
  },[]);

  const prefs=settings.ide;
  const themeName=customTheme||'devforge-workbench';
  useEffect(()=>{
    defineWorkbenchTheme(settings);
    if(!customTheme)monaco.editor.setTheme('devforge-workbench');
    monaco.editor.getModels().forEach(model=>model.updateOptions({tabSize:prefs.tabSize,insertSpaces:prefs.insertSpaces}));
  },[prefs,settings.theme,customTheme]);

  return <Editor
    height="100%"
    language={language}
    path={path}
    value={code}
    beforeMount={()=>{initMonacoThemes();defineWorkbenchTheme(current.current);}}
    onChange={value=>onChange(value??'')}
    onMount={(editor, m) => {
      editor.addCommand(monaco.KeyMod.Alt|monaco.KeyCode.Backslash,()=>{
        editor.trigger('devforge','hideSuggestWidget',{});
        void editor.getAction('editor.action.inlineSuggest.trigger')?.run();
      });
      if (onCursorChange) {
        editor.onDidChangeCursorPosition(e => {
          onCursorChange(e.position.lineNumber, e.position.column);
        });
      }
      if (onMount) {
        onMount(editor, m);
      }
    }}
    theme={themeName}
    loading={<div className="muted">Загрузка редактора…</div>}
    options={{
      fontSize: settings.fontSize,
      inlineSuggest: {
        enabled: settings.inlineCompletion,
        suppressSuggestions: false
      },
      quickSuggestions: {
        other: true,
        comments: false,
        strings: true
      },
      suggestOnTriggerCharacters: true,
      suggest: {
        preview: true,
        showWords: true,
        showSnippets: true,
        showKeywords: true,
        showFunctions: true,
        showClasses: true,
        showVariables: true,
        showProperties: true,
        showMethods: true,
        shareSuggestSelections: true
      },
      hover: {
        enabled: true,
        delay: 100
      },
      parameterHints: {
        enabled: true,
        cycle: true
      },
      wordBasedSuggestions: 'allDocuments',
      tabCompletion: 'on',
      acceptSuggestionOnEnter: 'on',
      snippetSuggestions: 'top',
      fontFamily: FONTS[prefs.fontFamily],
      fontLigatures:prefs.ligatures,
      lineHeight:Math.round(settings.fontSize*prefs.lineHeight),
      minimap: { enabled: !!settings.minimap },
      padding: { top: 16, bottom: 16 },
      scrollBeyondLastLine: false,
      automaticLayout: true,
      tabSize: prefs.tabSize,
      insertSpaces:prefs.insertSpaces,
      detectIndentation:false,
      wordWrap:prefs.wordWrap,
      wordWrapColumn:100,
      lineNumbers:prefs.lineNumbers,
      renderWhitespace:prefs.whitespace,
      smoothScrolling:prefs.smoothScrolling,
      cursorSmoothCaretAnimation:prefs.smoothScrolling?'on':'off',
      cursorStyle:prefs.cursorStyle,
      cursorBlinking:prefs.cursorBlinking,
      bracketPairColorization:{enabled:prefs.bracketColors},
      guides:{indentation:prefs.indentGuides,bracketPairs:prefs.bracketColors},
      stickyScroll:{enabled:prefs.stickyScroll},
      renderLineHighlight: 'all',
      overviewRulerBorder: false
    }}
  />;
}
