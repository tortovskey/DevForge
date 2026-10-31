import {test, expect} from '@playwright/test';
import solutions from './solutions.json' with {type: 'json'};

test.describe('DevForge New Languages: JS, TS, Java', () => {
  test('JavaScript in-browser worker runs code and passes tests', async ({page}) => {
    await page.goto('/');
    const result = await page.evaluate(async () => {
      const {BrowserRunner} = await import(/* @vite-ignore */ '/src/runners/runner.ts');
      const runner = new BrowserRunner('javascript');
      const r1 = await runner.run({code: 'console.log("Hello from JS " + (2 + 3));'});
      const r2 = await runner.run({
        code: 'function add(a, b) { return a + b; } console.log(add(10, 20));',
        check: true,
        tests: [{id: 't1', expected: '30'}]
      });
      runner.reset();
      return {r1, r2};
    });

    expect(result.r1.stdout.trim()).toBe('Hello from JS 5');
    expect(result.r2.stdout.trim()).toBe('30');
    expect(result.r2.results[0].actual).toBe('30');
  });

  test('TypeScript in-browser worker transpiles and runs typed code', async ({page}) => {
    await page.goto('/');
    const result = await page.evaluate(async () => {
      const {BrowserRunner} = await import(/* @vite-ignore */ '/src/runners/runner.ts');
      const runner = new BrowserRunner('typescript');
      const tsCode = `
        interface User { name: string; age: number; }
        const u: User = { name: "Alice", age: 30 };
        function greet(user: User): string { return user.name + ":" + user.age; }
        console.log(greet(u));
      `;
      const r = await runner.run({
        code: tsCode,
        check: true,
        tests: [{id: 't1', expected: 'Alice:30'}]
      });
      runner.reset();
      return r;
    });

    expect(result.stdout.trim()).toBe('Alice:30');
    expect(result.results[0].actual).toBe('Alice:30');
  });

  test('Java in-browser worker / hybrid runner runs and evaluates tests', async ({page}) => {
    await page.goto('/');
    const result = await page.evaluate(async () => {
      const {BrowserRunner} = await import(/* @vite-ignore */ '/src/runners/runner.ts');
      const runner = new BrowserRunner('java');
      const javaCode = `
        public class Main {
            public static void main(String[] args) {
                int a = 15;
                int b = 27;
                System.out.println(a + b);
            }
        }
      `;
      const r = await runner.run({
        code: javaCode,
        check: true,
        tests: [{id: 't1', expected: '42'}]
      });
      runner.reset();
      return r;
    });

    expect(result.stdout.trim()).toBe('42');
    expect(result.results[0].actual).toBe('42');
  });

  test('All 56 new lessons (JS: 20, TS: 18, Java: 18) solutions pass their test suites', async ({page}) => {
    test.setTimeout(180000);
    await page.goto('/');
    const result = await page.evaluate(async (sols) => {
      const {BrowserRunner} = await import(/* @vite-ignore */ '/src/runners/runner.ts');
      const courses = await (await fetch('/api/courses')).json();
      const newCourses = courses.filter((c: any) => ['javascript', 'typescript', 'java'].includes(c.id));
      const errors: string[] = [];
      let checked = 0;

      for (const course of newCourses) {
        const runner = new BrowserRunner(course.id);
        for (const lesson of course.lessons) {
          const solution = sols[lesson.id];
          if (!solution) {
            errors.push(`Missing solution for ${lesson.id}`);
            continue;
          }
          const runRes = await runner.run({
            code: solution,
            stdin: lesson.stdin || '',
            check: true,
            tests: lesson.tests
          });

          if (runRes.error) {
            errors.push(`${lesson.id} runtime error: ${runRes.error}`);
          }
          for (const t of lesson.tests) {
            const actual = runRes.results?.find((r: any) => r.id === t.id);
            if (!actual) {
              errors.push(`${lesson.id}: test ${t.id} not evaluated`);
            } else if (actual.error) {
              errors.push(`${lesson.id}: test ${t.id} failed with error: ${actual.error}`);
            } else if (JSON.stringify(actual.actual) !== JSON.stringify(t.expected)) {
              errors.push(`${lesson.id}: test ${t.id} got ${JSON.stringify(actual.actual)}, expected ${JSON.stringify(t.expected)}`);
            }
          }
          checked++;
        }
        runner.reset();
      }
      return {checked, errors};
    }, solutions);

    expect(result.errors).toEqual([]);
    expect(result.checked).toBe(56);
  });
});
