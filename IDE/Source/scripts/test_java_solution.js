const fs = require('fs');

let workerContent = fs.readFileSync('frontend/public/workers/java.js', 'utf8');

// Replace field collection logic in Step 10
workerContent = workerContent.replace(
  "// Collect field names in this class\n      const fields = [];",
  `// Collect field names in this class: only look outside method bodies!
      const fields = [];
      const classBodyWithoutMethods = classBody.replace(/\\{[^{}]*\\}/g, '{}').replace(/\\{[^{}]*\\}/g, '{}');`
);
workerContent = workerContent.replace(
  "while ((fm = fieldRegex.exec(classBody)) !== null) {",
  "while ((fm = fieldRegex.exec(classBodyWithoutMethods)) !== null) {"
);

const transpileMatch = workerContent.match(/function transpileJava\([\s\S]*?\n\}/);
eval(transpileMatch[0]);

const code = `
class TaskItem {
    long id;
    String title;
    int priority;
    TaskItem(long id, String title, int priority) {
        this.id = id; this.title = title; this.priority = priority;
    }
}

class ApiResponse {
    int status;
    Object data;
    String error;
    ApiResponse(int s, Object d, String e) {
        this.status = s; this.data = d; this.error = e;
    }
}

class TaskService {
    TaskItem create(String title, int priority) {
        return new TaskItem(1, title, priority);
    }
    TaskItem findById(long id) {
        return null;
    }
}

class TaskApiController {
    TaskService srv;
    TaskApiController(TaskService s) { this.srv = s; }
    ApiResponse handleCreate(String title, int priority) {
        if (title == null || title.isEmpty() || priority < 1) {
            return new ApiResponse(400, null, "Validation failed");
        }
        TaskItem item = this.srv.create(title, priority);
        return new ApiResponse(201, item, null);
    }
    ApiResponse handleGetById(long id) {
        TaskItem found = this.srv.findById(id);
        if (found == null) return new ApiResponse(404, null, "Task not found");
        return new ApiResponse(200, found, null);
    }
}

public class Main {
    public static void main(String[] args) {
        TaskService s = new TaskService();
        TaskApiController c = new TaskApiController(s);
        ApiResponse r1 = c.handleCreate("Init DB", 5);
        ApiResponse r2 = c.handleGetById(999);
        TaskItem t = r1.data;
        System.out.println(r1.status + " " + t.title);
        System.out.println(r2.status + " " + r2.error);
    }
}
`;

const res = transpileJava(code);
console.log(res);

let out = '';
const scope = {
  __println__: (...args) => out += args.join(' ') + '\n',
  __print__: (...args) => out += args.join(' '),
  Math, String, Array, Boolean, Number, parseInt, parseFloat, JSON
};

try {
  new Function('__scope__', `with (__scope__) { ${res}\n__main__(); }`)(scope);
  console.log('SUCCESS! Output:\n' + out);
} catch (e) {
  console.error('Runtime error:', e);
}
