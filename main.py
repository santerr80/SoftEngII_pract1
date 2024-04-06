from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import asyncio
import uvicorn
import TapexTokenizer
import pandas as pd


class Request(BaseModel):
    my_request: str


app = FastAPI()


"""
    Функция, которая обрабатывает корневую конечную точку ("/") приложения.
    Возвращает:
        HTMLResponse: Объект ответа, содержащий отображаемый HTML-контент.
"""


@app.get("/")
async def root():
    return {"message": "TapexTokenizer"}

"""
    Создание нового запроса.
    Параметры:
        my_request (str): Запрос, который необходимо создать.
    Возвращает:
        dict: Словарь, содержащий созданный запрос.
    """


@app.post("/request_create/")
async def request_create(request: Request):
    my_request = request.my_request
    app.state.my_request = my_request
    return {"Request": "my_request"}


"""
    Создание загружаемого файла.
    Параметры:
    - file (UploadFile): Файл для загрузки.
    Возвращает:
    - dict: Словарь, содержащий имя файла и dataframe, преобразованный в
    словарь.
    """


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    df = pd.read_csv(file.file, encoding='utf-8', sep=';')
    df = df.to_json()  # Преобразование dataframe в JSON-строку
    app.state.df = df  # Сохранение dataframe в state приложения
    return {"filename": file.filename, "dataframe": df}


"""
    Эта функция является асинхронным обработчиком маршрута для конечной точки
    API "/tokenize/". Она отвечает за токенизацию данных в `df` DataFrame с
    помощью класса TapexTokenizer.
    Параметры:
        None
    Возвращает:
        dict: Словарь, содержащий ответ от метода TapexTokenizer.
        tapex_tokenizer. Ответ хранится под ключом "response".
    """


@app.get("/tokenize/")
async def tokenize():
    df = app.state.df
    my_request = app.state.my_request
    df = pd.read_json(df)
    df = df.astype(str)
    response = TapexTokenizer.tapex_tokenizer(df, my_request)
    return {"response": response}


"""
    Асинхронная функция, обслуживающая основное приложение.
    :return: None
    """


async def main():
    config = uvicorn.Config("main:app", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
