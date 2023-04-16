import random

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

from settingsConfig import PrettyJSONResponse
from helpers.database import databaseSession
from helpers.sqlQueries import SqlQueries
from helpers.logger import logger


app = FastAPI()
log = logger.getLogger(__name__)


class _Server:
    def __init__(self):
        self.__initOnStart = False
        self.__dropOnFinish = False
        self.router = APIRouter()
        self.router.add_api_route("/writers/{writerID}", self.getWriterFullData, methods=["GET"], response_class=PrettyJSONResponse)

    def setInitOnStart(self, state):
        self.__initOnStart = state

    def setDropOnFinish(self, state):
        self.__dropOnFinish = state

    @staticmethod
    @app.on_event("shutdown")
    def __shutdown():
        if server.__dropOnFinish:
            server.__dropTables()

    @staticmethod
    def getWriterFullData(writerID):
        with databaseSession as db:
            writerData = db.getRows(
                SqlQueries.selectFullDataAboutWriter(writerID),
                data=dict(
                    writerID=writerID
                )
            )
        if writerData is None:
            return JSONResponse(status_code=404, content={"ErrorMessage": "Writer not found"})
        return writerData[0]

    def start(self):
        if self.__initOnStart:
            self.__initDatabase()
        uvicorn.run(app, host="127.0.0.1", port=8000)

    @staticmethod
    def __dataExists():
        flags = []
        commands = [
            SqlQueries.selectAllWriters(),
            SqlQueries.selectAllBooks()
        ]
        log.debug("Проверка наличия данных...")
        with databaseSession as db:
            for command in commands:
                data = db.getRows(command)
                if data:
                    flags.append(True)
                else:
                    flags.append(False)
        return False if not all(flags) else True

    @staticmethod
    def __initTables():
        commands = [
            SqlQueries.createTableWriter(),
            SqlQueries.createTableBook()
        ]
        log.debug("Инициализация таблиц в базе данных...")
        with databaseSession as db:
            for command in commands:
                db.execute(command)

    @staticmethod
    def __dropTables():
        commands = [
            SqlQueries.dropTableWriters(),
            SqlQueries.dropTableBooks()
        ]
        log.debug("Удаление таблиц из базы данных...")
        with databaseSession as db:
            for command in commands:
                db.execute(command)

    @staticmethod
    def __generateWriterData():
        for writerID in range(1, 4):
            name = f"writer_{writerID}"
            log.debug(f"Сгенерирован писатель с ID<{writerID}> и именем<{name}>")
            yield {
                "id": writerID,
                "name": name
            }

    @staticmethod
    def __generateBookData(writerID):
        numberAuthorBooks = random.randint(1, 4)
        for authorBookID in range(1, numberAuthorBooks + 1):
            name = f"book {authorBookID} from author {writerID}"
            log.debug(f"Сгенерирована книга с названием<{name}> для автора с ID<{writerID}>")
            yield {
                "author_id": writerID,
                "name": name
            }

    def __initData(self):
        log.debug("Запущен процесс генерации данных...")
        with databaseSession as db:
            for writer in self.__generateWriterData():
                db.execute(
                    SqlQueries.insertWriter(writer["name"]),
                    dict(name=writer["name"])
                )
                for book in self.__generateBookData(writer["id"]):
                    db.execute(
                        SqlQueries.insertBook(book["author_id"], book["name"]),
                        book
                    )
        log.debug("Процесс генерации данных завершен")

    def __initDatabase(self):
        self.__initTables()
        if not self.__dataExists():
            log.warning("Данные отсутствуют")
            self.__initData()


server = _Server()
