"""Read-only, fixed-query multi-source demo. No arbitrary SQL or NL model."""
import json
import sqlite3
import threading
from pathlib import Path
from generators import jde_inventory as inv, jde_purchasing as po, jde_manufacturing as wo, fusion_erp_financial as fin

QUESTIONS = {
 'stock': 'Quais itens estão abaixo do ponto de reposição?',
 'overdue': 'Qual o saldo de faturas vencidas por fornecedor?',
 'integrated': 'Quais fornecedores têm faturas vencidas e pedidos em aberto?',
 'manufacturing': 'Quais ordens de produção ainda estão em processo?'
}
QUERIES = {
 'stock': ('JDE inventory', '''SELECT i.IMLITM AS item, i.IMDSC1 AS description, b.IBMCU AS branch, b.IBPQOH AS on_hand, b.IBREORDER AS reorder_point FROM JDE_ITEMS i JOIN JDE_ITEM_BALANCE b ON b.IBITM=i.IMITM WHERE b.IBPQOH < b.IBREORDER ORDER BY b.IBPQOH, item, branch LIMIT 20'''),
 'overdue': ('Fusion AP', '''SELECT SUPPLIER_NUMBER AS supplier_id, SUPPLIER_NAME AS supplier, ROUND(SUM(AMOUNT_REMAINING),2) AS overdue_brl FROM FUSION_AP_INVOICES WHERE STATUS='OVERDUE' AND AMOUNT_REMAINING>0 GROUP BY SUPPLIER_NUMBER,SUPPLIER_NAME ORDER BY overdue_brl DESC LIMIT 20'''),
 'integrated': ('JDE purchasing + Fusion AP', '''WITH ap AS (SELECT SUPPLIER_NUMBER AS supplier_id, SUPPLIER_NAME AS supplier, SUM(AMOUNT_REMAINING) AS overdue FROM FUSION_AP_INVOICES WHERE STATUS='OVERDUE' AND AMOUNT_REMAINING>0 GROUP BY SUPPLIER_NUMBER,SUPPLIER_NAME), po AS (SELECT CAST(h.PHVEND AS TEXT) AS supplier_id, SUM(d.PDAOPN) AS open_amount FROM JDE_PO_HEADER h JOIN JDE_PO_DETAIL d ON h.PHDOCO=d.PDDOCO AND h.PHDCTO=d.PDDCTO WHERE h.PHST='20' AND d.PDUOPN>0 GROUP BY h.PHVEND) SELECT ap.supplier_id,ap.supplier,ROUND(ap.overdue,2) AS overdue_brl,ROUND(po.open_amount,2) AS open_po_brl FROM ap JOIN po ON ap.supplier_id=po.supplier_id ORDER BY overdue_brl DESC LIMIT 20'''),
 'manufacturing': ('JDE manufacturing', '''SELECT WADOCO AS work_order, WAMCU AS branch, WAUORG AS ordered, WACMPL AS completed, ROUND(WAWQTY,2) AS remaining FROM JDE_WO_HEADER WHERE WAST IN ('30','40') ORDER BY remaining DESC LIMIT 20''')
}


class Workspace:
 def __init__(self, seed=42):
  self.lock=threading.RLock()
  self.db=sqlite3.connect(':memory:',check_same_thread=False)
  self.db.row_factory=sqlite3.Row
  for module in [inv,po,wo,fin]:module.rng.seed(seed)
  headers=po.generate_po_header()
  tables={'JDE_ITEMS':inv.generate_f4101(),'JDE_ITEM_BALANCE':inv.generate_f41021(),
   'JDE_PO_HEADER':headers,'JDE_PO_DETAIL':po.generate_po_detail(headers),
   'JDE_WO_HEADER':wo.generate_work_orders(),'FUSION_GL_JOURNAL':fin.generate_gl_journals(),
   'FUSION_AP_INVOICES':fin.generate_ap_invoices()}
  self.counts={name:len(df) for name,df in tables.items()}
  for name,df in tables.items():df.to_sql(name,self.db,index=False)
  self.db.execute('PRAGMA query_only=ON')
  self.policies=json.loads((Path(__file__).parents[1]/'demo/policies.json').read_text())

 def ask(self, question_id):
  if question_id not in QUESTIONS:raise ValueError('Unsupported demo question. Choose one of the four fixed questions.')
  source,sql=QUERIES[question_id]
  with self.lock:rows=[dict(row) for row in self.db.execute(sql).fetchall()]
  policy_ids={'stock':['SYN-PROC-001'],'overdue':['SYN-FIN-001'],'integrated':['SYN-PROC-001','SYN-FIN-001'],'manufacturing':[]}[question_id]
  policies=[p for p in self.policies if p['id'] in policy_ids]
  return {'question':QUESTIONS[question_id],'source':source,'sql':sql,'rows':rows,'policies':policies,
    'answer':f'{len(rows)} synthetic result rows. Review the table and cited invented policy; no ERP changes are made.',
    'mode':'fixed-query synthetic demo','as_of':'2026-04-26','row_limit':20}

 def close(self):self.db.close()
