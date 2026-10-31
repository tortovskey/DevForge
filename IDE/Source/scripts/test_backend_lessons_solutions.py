"""Verify that all 19 backend lessons' solutionCode pass all their defined tests."""
import json
import sys
from pathlib import Path

# Add backend pack to sys.modules
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "frontend" / "public" / "workers"))
import backend_pack  # registers fastapi, pydantic, sqlalchemy, pytest

def main():
    lessons = json.load(open(root / "content" / "lessons.json", encoding="utf-8"))
    backend_lessons = [l for l in lessons if l["id"].startswith("backend-")]
    print(f"Testing {len(backend_lessons)} backend lessons...")

    failed = 0
    for l in backend_lessons:
        lid = l["id"]
        code = l["solutionCode"]
        tests = l["tests"]

        namespace = {"__name__": "__main__"}
        try:
            exec(code, namespace)
            for t in tests:
                expr = t["expression"]
                expected = t["expected"]
                actual = eval(expr, namespace)
                assert actual == expected, f"Lesson {lid} test {t['id']} failed: expected {expected}, got {actual}"
            print(f"  [PASS] {lid} ({len(tests)} tests)")
        except Exception as e:
            print(f"  [FAIL] {lid}: {e}")
            failed += 1

    if failed == 0:
        print(f"\nALL {len(backend_lessons)} BACKEND LESSONS PASSED 100%!")
    else:
        print(f"\n{failed} LESSONS FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
