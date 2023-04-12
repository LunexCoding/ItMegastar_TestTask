class SqlQueries:
    @staticmethod
    def createTableWriter():
        return """
        create table if not exists Writer
        (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """

    @staticmethod
    def createTableBook():
        return """
            CREATE TABLE IF NOT EXISTS Book
            (
                id SERIAL PRIMARY KEY,
                author_id INTEGER,
                name VARCHAR(255) NOT NULL,
                FOREIGN KEY (author_id) REFERENCES Writer (id) ON DELETE CASCADE
            );
            """

    @staticmethod
    def selectAllRowsFromTableWriter():
        return """
        SELECT * FROM Writer
        """

    @staticmethod
    def selectAllRowsFromTableBook():
        return """
        SELECT * FROM Book
        """

    @staticmethod
    def insertWriter(name):
        return """
        INSERT INTO Writer
            (name)
        SELECT
            %(name)s
        WHERE
            NOT EXISTS (
                SELECT name FROM Writer WHERE name = %(name)s
            )
        """

    @staticmethod
    def insertBook(author_id, name):
        return """
        INSERT INTO Book 
            (author_id, name)
        SELECT
            %(author_id)s, %(name)s
        WHERE
            NOT EXISTS (
                SELECT author_id, name FROM Book WHERE name = %(name)s AND author_id = %(author_id)s
            )
        """