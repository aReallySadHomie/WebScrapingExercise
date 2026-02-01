from psycopg2 import pool
import os

class DatabaseConnector:
    def __init__(self):
        self.parameters = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("db_USER"),
            "password": os.getenv("db_PASSWORD")
            }

        if not all(self.parameters.values()):
            raise EnvironmentError("Please set environment variables in .env file")

        self.connection_pool = pool.ThreadedConnectionPool(1, 10, **self.parameters)