import type {LanguageId} from '../types';

// Every supported language must have an explicit template. A new language can
// never silently inherit SQL's filename or source code.
export const PROJECT_TEMPLATES: Record<LanguageId, {name:string;content:string}> = {
  python: {name:'main.py',content:'# Ваш следующий проект начинается здесь\nprint("Hello, DevForge!")'},
  c: {name:'main.c',content:'#include <stdio.h>\n\nint main(void) {\n    puts("Hello, DevForge!");\n    return 0;\n}'},
  cpp: {name:'main.cpp',content:'#include <iostream>\n\nint main() {\n    std::cout << "Hello, DevForge C++!" << std::endl;\n    return 0;\n}'},
  csharp: {name:'Program.cs',content:'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, DevForge C#!");\n    }\n}'},
  objc: {name:'main.m',content:'#import <Foundation/Foundation.h>\n\nint main() {\n    @autoreleasepool {\n        NSLog(@"Hello, DevForge Objective-C!");\n    }\n    return 0;\n}'},
  rust: {name:'main.rs',content:'fn main() {\n    println!("Hello, DevForge Rust!");\n}'},
  '1c': {name:'Module.bsl',content:'Сообщить("Привет, DevForge 1С!");'},
  javascript: {name:'index.js',content:'// Ваш скрипт JavaScript\nconsole.log("Hello, DevForge!");'},
  typescript: {name:'index.ts',content:'// Типизированный код TypeScript\nconst greet = (name: string): string => `Привет, ${name}!`;\nconsole.log(greet("DevForge"));'},
  java: {name:'Main.java',content:'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, DevForge!");\n    }\n}'},
  lua: {name:'main.lua',content:'-- Ваш скрипт Lua\nprint("Hello, DevForge!")'},
  assembly: {name:'main.asm',content:`; x86-64 NASM — вывод строки через Linux syscall
section .data
    message db "Hello, DevForge!", 10
    length equ $ - message

section .text
    global _start

_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, message
    mov rdx, length
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall
`},
  sql: {name:'query.sql',content:"-- Ваша независимая база SQLite\nSELECT 'Hello, DevForge!' AS message;"},
  postgresql: {name:'query.sql',content:"-- Ваша независимая база PostgreSQL\nSELECT 'Hello, DevForge!' AS message;"},
  'html-css': {name:'index.html',content:'<h1>Моя первая страница</h1>\n<p>Здесь начинается идея.</p>'}
};
