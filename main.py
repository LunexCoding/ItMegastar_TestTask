from helpers.database import databaseSession
from helpers.sqlQueries import SqlQueries


with databaseSession as db:
    commands = (
        SqlQueries.createTableWriter(),
        SqlQueries.createTableBook()
    )
    for command in commands:
        db.execute(
            command
        )

    name = "Oleg"
    db.execute(
        SqlQueries.insertWriter(name),
        dict(
            name=name
        )
    )
    data = db.getRows(SqlQueries.selectAllRowsFromTableWriter())
    print(data)

    author_id = 3
    name = "сказка"
    db.execute(
        SqlQueries.insertBook(author_id, name),
        dict(
            author_id=author_id,
            name=name
        )
    )

    data = db.getRows(SqlQueries.selectAllRowsFromTableBook())
    print(data)
