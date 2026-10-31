import json

# 1. Update frontend/public/workers/java.js
with open('frontend/public/workers/java.js', 'r', encoding='utf-8') as f:
    jw = f.read()

# Add String.join helper or replace String.join in transpileJava
if 'String.join =' not in jw:
    jw = jw.replace(
        "/* DevForge Java Worker: transpiles educational Java code to JavaScript and runs in Web Worker */",
        """/* DevForge Java Worker: transpiles educational Java code to JavaScript and runs in Web Worker */
if (typeof String.join !== 'function') {
  String.join = (sep, arr) => (Array.isArray(arr) ? arr.join(sep) : String(arr));
}
class Exception extends Error {
  constructor(msg) { super(msg); this.message = msg; }
  getMessage() { return this.message; }
}
"""
    )

# Fix cast stripping: ((Type)expr) -> expr
if 'Casts stripping' not in jw:
    jw = jw.replace(
        "// 1. Remove imports and package",
        """// 0. Casts and catch clauses
  js = js.replace(/\\(\\s*\\([A-Za-z_]\\w*\\)\\s*([A-Za-z_][\\w\\.]*)\\s*\\)/g, '$1');
  js = js.replace(/catch\\s*\\(\\s*[A-Za-z_]\\w*\\s+(\\w+)\\s*\\)/g, 'catch ($1)');
  // 1. Remove imports and package"""
    )

with open('frontend/public/workers/java.js', 'w', encoding='utf-8') as f:
    f.write(jw)

# 2. Update content/lessons.json solutions for the 6 Java lessons so they are crystal-clean
lessons = json.load(open('content/lessons.json', 'r', encoding='utf-8'))

for l in lessons:
    if l['id'] == 'java-stream-api':
        code = '''import java.util.*;

class Task {
    String title;
    int priority;
    Task(String title, int priority) {
        this.title = title;
        this.priority = priority;
    }
}

public class Main {
    public static void main(String[] args) {
        Task[] tasks = new Task[] {
            new Task("deploy", 10),
            new Task("refactor", 3),
            new Task("backup", 8)
        };
        ArrayList res = new ArrayList();
        for (Task t : tasks) {
            if (t.priority >= 5) {
                res.add(t.title.toUpperCase());
            }
        }
        Collections.sort(res);
        System.out.println(String.join(", ", res));
    }
}
'''
        l['starterCode'] = code
        l['guide']['solution'] = code
        l['guide']['example']['code'] = code

    elif l['id'] == 'java-spring-boot-controller':
        code = '''import java.util.*;

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
        TaskItem item = this.srv.findById(id);
        if (item == null) return new ApiResponse(404, null, "Task not found");
        return new ApiResponse(200, item, null);
    }
}

public class Main {
    public static void main(String[] args) {
        TaskService s = new TaskService();
        TaskApiController c = new TaskApiController(s);
        ApiResponse r1 = c.handleCreate("Init DB", 5);
        ApiResponse r2 = c.handleGetById(999);
        TaskItem t = (TaskItem)r1.data;
        System.out.println(r1.status + " " + t.title);
        System.out.println(r2.status + " " + r2.error);
    }
}
'''
        l['starterCode'] = code
        l['guide']['solution'] = code
        l['guide']['example']['code'] = code

    elif l['id'] == 'java-project-enterprise-api':
        code = '''import java.util.*;

class EntTask {
    long id;
    String title;
    String status;
    int priority;
    EntTask(long id, String title, int priority) {
        this.id = id; this.title = title; this.priority = priority; this.status = "NEW";
    }
}

class EnterpriseTaskManager {
    Map db = new HashMap();
    long nextId = 1;
    EntTask createTask(String title, int priority) {
        EntTask t = new EntTask(this.nextId++, title, priority);
        this.db.put(t.id, t);
        return t;
    }
    EntTask updateStatus(long id, String newStatus) {
        EntTask t = (EntTask)this.db.get(id);
        t.status = newStatus;
        return t;
    }
    ArrayList searchTasks(String status, int page, int pageSize) {
        ArrayList res = new ArrayList();
        for (Object obj : this.db.values()) {
            EntTask t = (EntTask)obj;
            if (t.status.equals(status)) res.add(t);
        }
        return res;
    }
}

public class Main {
    public static void main(String[] args) {
        EnterpriseTaskManager m = new EnterpriseTaskManager();
        EntTask t1 = m.createTask("Setup CI/CD", 5);
        EntTask t2 = m.createTask("Security Audit", 10);
        m.updateStatus(t1.id, "IN_PROGRESS");
        ArrayList list = m.searchTasks("IN_PROGRESS", 1, 10);
        EntTask first = (EntTask)list.get(0);
        System.out.println(list.size() + " " + first.title + " " + first.status);
    }
}
'''
        l['starterCode'] = code
        l['guide']['solution'] = code
        l['guide']['example']['code'] = code

    elif l['id'] == 'java-exceptions-try-resources':
        code = '''class OverdraftException extends Exception {
    OverdraftException(String msg) { super(msg); }
}

class SafeBankVault {
    int balanceCents;
    SafeBankVault(int initial) { this.balanceCents = initial; }
    void withdraw(int amount) throws OverdraftException {
        if (this.balanceCents < amount) throw new OverdraftException("Not enough balance");
        this.balanceCents -= amount;
    }
    int getBalance() { return this.balanceCents; }
}

public class Main {
    public static void main(String[] args) {
        SafeBankVault vault = new SafeBankVault(500);
        try {
            vault.withdraw(300);
            vault.withdraw(400);
        } catch (OverdraftException e) {
            System.out.println(e.getMessage());
        }
        System.out.println(vault.getBalance());
    }
}
'''
        l['starterCode'] = code
        l['guide']['solution'] = code
        l['guide']['example']['code'] = code

    elif l['id'] == 'java-spring-data-jpa':
        code = '''import java.util.*;

class JpaTask {
    Long id;
    String name;
    String category;
    int priority;
    JpaTask(Long id, String name, String category, int priority) {
        this.id = id; this.name = name; this.category = category; this.priority = priority;
    }
}

class TaskRepositoryModel {
    ArrayList store = new ArrayList();
    long nextId = 1;
    JpaTask save(JpaTask item) {
        item.id = this.nextId++;
        this.store.add(item);
        return item;
    }
    ArrayList findByCategory(String cat) {
        ArrayList res = new ArrayList();
        for (Object obj : this.store) {
            JpaTask item = (JpaTask)obj;
            if (item.category.equals(cat)) res.add(item);
        }
        return res;
    }
    long count() { return this.store.size(); }
}

public class Main {
    public static void main(String[] args) {
        TaskRepositoryModel repo = new TaskRepositoryModel();
        JpaTask t1 = repo.save(new JpaTask(null, "Setup PostgreSQL", "database", 10));
        JpaTask t2 = repo.save(new JpaTask(null, "Write Liquibase", "database", 8));
        ArrayList dbTasks = repo.findByCategory("database");
        System.out.println(repo.count() + " " + dbTasks.size() + " " + t1.id);
    }
}
'''
        l['starterCode'] = code
        l['guide']['solution'] = code
        l['guide']['example']['code'] = code

with open('content/lessons.json', 'w', encoding='utf-8') as f:
    json.dump(lessons, f, indent=2, ensure_ascii=False)

print("Updated Java lessons and worker successfully!")
