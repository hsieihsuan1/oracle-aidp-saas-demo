import sqlite3
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.workspace import Workspace,QUESTIONS
from generators.jde_purchasing import jde_date
from datetime import date

@pytest.fixture
def workspace():
 w=Workspace();yield w;w.close()

@pytest.mark.parametrize('question_id',QUESTIONS)
def test_scenarios(workspace,question_id):
 r=workspace.ask(question_id)
 assert r['rows'] and len(r['rows'])<=20
 assert r['mode']=='fixed-query synthetic demo'
 assert r['as_of']=='2026-04-26'

@pytest.mark.parametrize('question_id',QUESTIONS)
def test_repeatable_seed(workspace,question_id):
 other=Workspace();assert workspace.ask(question_id)==other.ask(question_id);other.close()

def test_integrated_totals_no_join_fanout(workspace):
 r=workspace.ask('integrated')
 for row in r['rows']:
  ap=workspace.db.execute("SELECT ROUND(SUM(AMOUNT_REMAINING),2) FROM FUSION_AP_INVOICES WHERE STATUS='OVERDUE' AND SUPPLIER_NUMBER=?",(row['supplier_id'],)).fetchone()[0]
  po=workspace.db.execute("SELECT ROUND(SUM(d.PDAOPN),2) FROM JDE_PO_HEADER h JOIN JDE_PO_DETAIL d ON h.PHDOCO=d.PDDOCO AND h.PHDCTO=d.PDDCTO WHERE h.PHST='20' AND CAST(h.PHVEND AS TEXT)=?",(row['supplier_id'],)).fetchone()[0]
  assert row['overdue_brl']==ap and row['open_po_brl']==po

def test_stock_predicate(workspace):
 assert all(row['on_hand']<row['reorder_point'] for row in workspace.ask('stock')['rows'])

def test_policy_provenance(workspace):
 assert {p['id'] for p in workspace.ask('integrated')['policies']}=={'SYN-PROC-001','SYN-FIN-001'}
 assert workspace.ask('manufacturing')['policies']==[]

def test_financial_invariant(workspace):
 n=workspace.db.execute('SELECT COUNT(*) FROM FUSION_AP_INVOICES WHERE ABS(AMOUNT-AMOUNT_PAID-AMOUNT_REMAINING)>0.011').fetchone()[0]
 assert n==0

def test_read_only_database(workspace):
 with pytest.raises(sqlite3.OperationalError):workspace.db.execute('DELETE FROM JDE_ITEMS')

@pytest.mark.parametrize('question',['DROP TABLE JDE_ITEMS','invented','../.env',''])
def test_unknown_not_executed(workspace,question):
 with pytest.raises(ValueError):workspace.ask(question)
 assert workspace.db.execute('SELECT COUNT(*) FROM JDE_ITEMS').fetchone()[0]==50

def test_jde_dates():
 assert jde_date(date(2026,1,1))==126001
 assert jde_date(date(2024,12,31))==124366

def test_api_contract():
 client=TestClient(create_app())
 assert client.get('/health').json()['remote_calls'] is False
 assert client.get('/api/catalog').status_code==200
 assert client.post('/api/query',json={'question_id':'integrated'}).status_code==200
 assert client.post('/api/query',json={'question_id':'stock','sql':'SELECT 1'}).status_code==422
 assert client.post('/api/query',json={'question_id':'arbitrary'}).status_code==422
 assert client.get('/').status_code==200

def test_notebook_code_executes():
 import json
 from pathlib import Path
 notebook=json.loads((Path(__file__).parents[1]/'notebooks/01_local_workspace.ipynb').read_text())
 namespace={}
 for cell in notebook['cells']:
  if cell['cell_type']=='code':
   assert cell['outputs']==[] and cell['execution_count'] is None
   exec(compile(''.join(cell['source']),'demo-notebook','exec'),namespace)
