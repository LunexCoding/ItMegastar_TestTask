import sys
import random
import json

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from helpers.database import databaseSession
from helpers.sqlQueries import SqlQueries
from settingsConfig import PrettyJSONResponse


def __initTables():
    with databaseSession as db:
        commands = [
            SqlQueries.createTableWriter(),
            SqlQueries.createTableBook()
        ]
        for command in commands:
            db.execute(command)

def __initData():
    with databaseSession as db:
        for writerID in range(1, 4):
            name = f"writer_{writerID}"
            db.execute(
                SqlQueries.insertWriter(name),
                dict(
                    name=name
                )
            )
            numberAuthorBooks = random.randint(1, 4)
            print(numberAuthorBooks)
            for authorBookID in range(1, numberAuthorBooks + 1):
                bookName = f"book {authorBookID} from author {writerID}"
                print(authorBookID, bookName)
                db.execute(
                    SqlQueries.insertBook(writerID, bookName),
                    dict(
                        author_id=writerID,
                        name=bookName
                    )
                )

def initDatabase():
    print("init")
    __initTables(),
    __initData()


app = FastAPI()

@app.get("/writers/{id}", response_class=PrettyJSONResponse)
def get_account(id):
    writerData = None
    with databaseSession as db:
        writerData = db.getRows(
            SqlQueries.selectFullDataAboutWriter(id),
            data=dict(
                writerID=id
            )
        )
    if writerData is None:
        return JSONResponse(status_code=404, content={"ErrorMessage": "Writer not found"})
    return writerData[0]


if __name__ == "__main__":
    args = sys.argv
    if "init" in args:
        initDatabase()
    uvicorn.run(app, host="127.0.0.1", port=8000)

