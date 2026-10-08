import subprocess,sys,time
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parents[1]
server=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8003'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 for _ in range(100):
  try:
   if urlopen('http://127.0.0.1:8003/health').status==200:break
  except OSError:time.sleep(.1)
 else:raise RuntimeError('Server did not start')
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':1100});page.goto('http://127.0.0.1:8003');page.locator('#run').click();page.get_by_text('SYN-FIN-001 · Synthetic supplier review',exact=True).wait_for();assert page.locator('#table tr').count()>1;assert 'WITH ap AS' in page.locator('#sql').inner_text();page.screenshot(path=str(ROOT/'docs/demo-running.png'))
  for scenario in ['stock','overdue','manufacturing']:
   page.locator('#question').select_option(scenario);page.locator('#run').click();page.locator('#run').wait_for(state='visible');page.wait_for_function('!document.getElementById("run").disabled');assert page.locator('#table tr').count()>1;assert page.locator('#error').inner_text()==''
  print('4 UI scenarios passed. Actual integrated query screenshot captured.');b.close()
finally:server.terminate();server.wait(timeout=10)
