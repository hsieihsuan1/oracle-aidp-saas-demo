from pathlib import Path
from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,ConfigDict,Field
from app.workspace import Workspace,QUESTIONS

ROOT=Path(__file__).parents[1]
class Query(BaseModel):
 model_config=ConfigDict(extra='forbid')
 question_id:str=Field(min_length=1,max_length=30)

def create_app():
 app=FastAPI(title='Enterprise Data Workspace - synthetic local demo')
 workspace=Workspace()
 @app.get('/health')
 def health():return {'status':'ok','remote_calls':False,'mode':'synthetic'}
 @app.get('/api/catalog')
 def catalog():return {'questions':QUESTIONS,'tables':workspace.counts,'as_of':'2026-04-26'}
 @app.post('/api/query')
 def query(request:Query):
  try:return workspace.ask(request.question_id)
  except ValueError as e:raise HTTPException(422,str(e))
 @app.get('/')
 def home():return FileResponse(ROOT/'demo/index.html')
 app.mount('/assets',StaticFiles(directory=ROOT/'demo'),name='assets')
 return app
app=create_app()
