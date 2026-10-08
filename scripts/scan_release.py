"""Conservative release-content check, not a security audit."""
from pathlib import Path
import re
import subprocess
ROOT=Path(__file__).parents[1]
patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{30,}',r'AKIA[A-Z0-9]{16}',r'ocid1\.[a-z]+\.[a-z0-9.]+',r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',r'verify\s*=\s*False']
try:
 names=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).splitlines()
except subprocess.CalledProcessError:
 names=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','.venv','__pycache__','.pytest_cache'])]
errors=[]
for name in names:
 p=ROOT/name
 if not p.exists():continue
 if p.name=='.env' or p.suffix in ['.pem','.key','.tfstate','.parquet','.db','.sqlite']:errors.append(name+': forbidden file type')
 if p.suffix=='.png':continue
 try:text=p.read_text()
 except UnicodeDecodeError:errors.append(name+': unexpected binary');continue
 for pattern in patterns:
  if re.search(pattern,text):errors.append(name+': sensitive or unsafe pattern')
 if p.suffix=='.ipynb':
  import json
  nb=json.loads(text)
  if any(c.get('outputs') or c.get('execution_count') is not None for c in nb['cells']):errors.append(name+': notebook contains outputs')
if errors:raise SystemExit('\n'.join(errors))
print(f'Release check passed for {len(names)} candidate files (heuristic only).')
