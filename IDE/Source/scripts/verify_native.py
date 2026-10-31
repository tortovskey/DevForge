"""Exercise self-contained builds from an unrelated working directory and fresh data."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time
from uuid import uuid4


def wait_file(path, process, timeout=60):
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        if path.is_file():return json.loads(path.read_text(encoding='utf-8-sig'))
        if process.poll() is not None:raise RuntimeError(f'Process exited with {process.returncode}: {path.name}')
        time.sleep(.2)
    raise TimeoutError(path.name)


def main():
    root=Path(__file__).resolve().parents[1]
    parser=argparse.ArgumentParser()
    parser.add_argument('--distribution',type=Path,default=root/'build'/'distribution')
    parser.add_argument('--edition',choices=['IDE','Desktop'],action='append')
    args=parser.parse_args()
    report=root/'build'/'native-verification';report.mkdir(parents=True,exist_ok=True)
    for edition in args.edition or ['IDE','Desktop']:
        state=report/f'{edition}.json';state.unlink(missing_ok=True)
        env={**os.environ,'DEVFORGE_TEST_HIDDEN':'1','DEVFORGE_DATA_DIR':str(report/f'{edition}-{uuid4().hex[:8]}-data'),
             'DEVFORGE_SMOKE_REPORT':str(state),'DEVFORGE_MODE':'full'}
        for key in ('DEVFORGE_ROOT','DEVFORGE_DB'):env.pop(key,None)
        name={'IDE':'DevForgeIDE','Desktop':'DevForge'}[edition]
        command=[str(args.distribution.resolve()/edition/(name+'.exe'))]
        process=subprocess.Popen(command,cwd=report,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            result=wait_file(state,process)
            if edition=='IDE':
                assert result['ready'] and result['icon'] and result['isolated'],result
            elif edition=='Desktop':
                assert result['isolated'] and result['python']['stdout'].strip()=='42',result
            print(edition+': passed',flush=True)
        finally:
            if process.poll() is None:process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)


if __name__=='__main__':main()
