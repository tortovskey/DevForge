function extractClassFields(classBody) {
  let depth = 0;
  let stmt = '';
  const fields = [];
  for (let i = 0; i < classBody.length; i++) {
    const ch = classBody[i];
    if (ch === '{') {
      depth++;
      stmt = '';
    } else if (ch === '}') {
      depth--;
      stmt = '';
    } else if (ch === ';') {
      if (depth === 0) {
        // We have a field statement at class depth!
        // Split before '=' if any
        const beforeAssign = stmt.split('=')[0].trim();
        const m = beforeAssign.match(/\b([A-Za-z_]\w*)$/);
        if (m && m[1] !== 'return') {
          fields.push(m[1]);
        }
      }
      stmt = '';
    } else {
      stmt += ch;
    }
  }
  return fields;
}

const testClass = `
    long id;
    String title;
    int count = 0;
    Map db = new HashMap();
    TaskItem(long id, String title, int priority) {
        this.id = id; this.title = title; this.priority = priority;
    }
    void doWork() {
        int temp = 42;
        String name = "test";
    }
`;

console.log('Extracted fields:', extractClassFields(testClass));
