import sys

from server import server, app


if __name__ == "__main__":
    args = sys.argv
    app.include_router(server.router)
    server.setInitOnStart("init" in args)
    server.setDropOnFinish("drop" in args)
    server.start()
