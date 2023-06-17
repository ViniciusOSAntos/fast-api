from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from  models import Curso

app = FastAPI()

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


@app.get('/cursos')
async def get_cursos():
    return cursos

@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int):
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

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)