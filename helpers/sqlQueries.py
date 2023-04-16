class SqlQueries:
    @staticmethod
    def createTableWriter():
        return """
        create table if not exists writers
        (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """

    @staticmethod
    def createTableBook():
        return """
            CREATE TABLE IF NOT EXISTS books
            (
                id SERIAL PRIMARY KEY,
                author_id INTEGER,
                name VARCHAR(255) NOT NULL,
                FOREIGN KEY (author_id) REFERENCES writers (id)
            );
            """

    @staticmethod
    def dropTableWriters():
        return """DROP TABLE IF EXISTS writers CASCADE"""

    @staticmethod
    def dropTableBooks():
        return """DROP TABLE IF EXISTS books CASCADE"""

    @staticmethod
    def insertWriter(name):
        return """
        INSERT INTO writers
            (name)
        SELECT
            %(name)s
        WHERE
            NOT EXISTS (
                SELECT name FROM writers WHERE name = %(name)s
            )
        """

    @staticmethod
    def insertBook(author_id, name):
        return """
        INSERT INTO books
            (author_id, name)
        SELECT
            %(author_id)s, %(name)s
        WHERE
            NOT EXISTS (
                SELECT author_id, name FROM books WHERE name = %(name)s AND author_id = %(author_id)s
            )
        """

    @staticmethod
    def selectFullDataAboutWriter(writerID):
        return """
        SELECT 
        json_build_object(
            'id', writers.id,
            'name', writers.name,
            'books', json_agg(
                json_build_object(
                    'id', books.id,
                    'name', books.name
                )
            )  
        )
        FROM books, writers
        WHERE writers.id = %(writerID)s AND books.author_id = writers.id
        GROUP BY writers.id
        """

    @staticmethod
    def selectAllWriters():
        return """SELECT * FROM writers"""

    @staticmethod
    def selectAllBooks():
        return """SELECT * FROM books"""
