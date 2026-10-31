from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from .accounts import Account, Assessment, Completion, current_account
from .content import LESSONS, read
from .database import session
from .schemas import StrictModel

QUESTIONS=read('assessment.json')
router=APIRouter(prefix='/api')

class Answers(StrictModel):
    answers:dict[str,int]=Field(max_length=30)

@router.get('/assessment/{language}')
def questions(language:str):
    entries=[q for q in QUESTIONS if q['language']==language]
    if not entries:raise HTTPException(404,'Тест для этого языка не найден')
    return [{k:v for k,v in q.items() if k not in {'correct','explanation'}} for q in entries]

@router.post('/assessment/{language}')
def assess(language:str,body:Answers,db:Session=Depends(session),account:Account=Depends(current_account)):
    entries=[q for q in QUESTIONS if q['language']==language]
    if not entries:raise HTTPException(404,'Тест не найден')
    if set(body.answers)!={q['id'] for q in entries}:raise HTTPException(422,'Ответьте на все вопросы или выберите «Не знаю»')
    if any(not -1<=body.answers[q['id']]<len(q['options']) for q in entries):raise HTTPException(422,'Некорректный вариант ответа')
    value=assessment_value(language,body.answers)
    db.merge(Assessment(owner_id=account.id,language=language,value=value));db.commit()
    return value

def assessment_value(language:str,answers:dict[str,int],created_at:str|None=None):
    entries=[q for q in QUESTIONS if q['language']==language]
    results=[{'id':q['id'],'tag':q['tag'],'correct':answers[q['id']]==q['correct'],'answer':answers[q['id']],'expected':q['correct'],'explanation':q['explanation']} for q in entries]
    score=sum(r['correct'] for r in results)
    ratio=score/len(entries)
    level='С нуля' if ratio<.25 else 'Beginner' if ratio<.6 else 'Elementary' if ratio<.85 else 'Intermediate'
    return {'language':language,'score':score,'total':len(entries),'level':level,'results':results,'createdAt':created_at or datetime.now(timezone.utc).isoformat(),'preliminary':True}

@router.get('/learning-plan')
def plan(db:Session=Depends(session),account:Account=Depends(current_account)):
    completed=set(db.scalars(select(Completion.lesson_id).where(Completion.owner_id==account.id)))
    assessments={a.language:a.value for a in db.scalars(select(Assessment).where(Assessment.owner_id==account.id))}
    courses=[]
    for language in dict.fromkeys(l['language'] for l in LESSONS):
        assessment=assessments.get(language)
        strong={r['tag'] for r in assessment['results'] if all(x['correct'] for x in assessment['results'] if x['tag']==r['tag'])} if assessment else set()
        ordered=sorted([l for l in LESSONS if l['language']==language],key=lambda l:l['order'])
        recommended=[l['id'] for l in ordered if l['id'] not in completed and (not strong or not set(l.get('concepts',[])).issubset(strong))]
        review=[l['id'] for l in ordered if l['id'] not in completed and l['id'] not in recommended]
        courses.append({'language':language,'assessment':assessment,'recommended':recommended,'review':review,'nextLesson':next(iter(recommended or review),None),'completed':len([l for l in ordered if l['id'] in completed]),'total':len(ordered)})
    return {'courses':courses,'notice':'Диагностика предварительная. Она меняет порядок рекомендаций, но не засчитывает уроки и не начисляет XP.'}
