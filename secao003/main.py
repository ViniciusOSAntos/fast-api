from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import HTTPException
from fastapi import status
from fastapi import Path, Query, Header, Depends

from  models import Curso
from typing import Any, Dict, List
from time import sleep

def fake_db():
    try:
        print('Abrindo conxão com banco de dados...')
        sleep(1)
    finally:
        print('Fechando conexão com o banco de dados...')
        sleep(1)

app = FastAPI(
    title='Studies FastAPI',
    version='0.01',
    description='API for FastAPI studies'
    )

cursos = {
   1: {
    "titulo": "Programação para Leigos",
    "aulas": 112,
    "horas": 58
   },
   2: {
       "título": "Algoritmos e Lógica de Programação",
       "aulas": 87,
       "horas": 67
   }
}


@app.get('/cursos',
         description='Retorna todos os cursos ou uma lista vazia',
         summary='Retorna todos os cursos',
         response_model=List[Curso],
         response_description="Cursos Retornados com Sucesso "
         )
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path( 
    title='ID do Curso', 
    description='Deve ser entre 1 e 2', 
    gt=0, 
    lt=3)
    ): # Tem que ser maior que 0 e menor que 3

    try:     
        curso = cursos[curso_id]
        curso.update({"id": curso_id})
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')
    
    return curso

@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    if curso.id not in cursos:
        cursos[curso.id] = curso
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Já existe um curso com {curso.id}.")


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso

        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com id {curso_id}')

@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT) Esse é o método ideal porém há um big na lib
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Não existe um curso com id {curso_id}")


@app.get('/calculadora')
async def calcular(x_geek: str = Header(default=None),a: int = Query(gt=5), b: int = Query(gt=10),  c: int = Query(gt=15)):
    resultado = a + b + c

    print(f"X-GEEK: {x_geek}")
    return {"resultado": resultado}

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)