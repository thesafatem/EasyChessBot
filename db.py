import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from contextlib import closing


def get_conn(dbname=None):
    kw = {
        'user': 'postgres',
        'password': '****************',
        'host': 'localhost',
        'port': '5432'
    }
    if dbname:
        kw['dbname'] = dbname
    return psycopg2.connect(**kw)


def create_database():
    with closing(get_conn()) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE easychess")


def delete_database():
    with closing(get_conn('easychess')) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute("DROP DATABASE easychess")


def create_table():
    with closing(get_conn('easychess')) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            sql = """CREATE type game_state as enum(
                        'find',
                        'in progress',
                        'white wins',
                        'black wins',
                        'draw'
                    );
                    CREATE type move_state as enum(
                        'white',
                        'black'
                    );
                    CREATE TABLE games(
                        id SERIAL PRIMARY KEY,
                        game bytea,
                        start_time timestamp NOT NULL DEFAULT NOW(),
                        white int,
                        black int,
                        status game_state NOT NULL DEFAULT 'find',
                        current_move move_state NOT NULL DEFAULT 'white'
                    );"""
            cursor.execute(sql)


def insert_row(game, white):
    with closing(get_conn('easychess')) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            sql = f"""INSERT INTO games (game, white) VALUES (decode('{game}', 'base64'), {white})"""
            cursor.execute(sql)
            conn.commit()


def update_row(**kw):
    with closing(get_conn('easychess')) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            val = []
            _set = []
            where_str = " WHERE id=%s"
            for key in kw.keys():
                if key != 'id':
                    _set.append(f"{key}=%s")
                    val.append(kw[key])
            val.append(kw['id'])
            val = tuple(val)
            set_str = ','.join(_set)
            sql = f"""UPDATE games SET """ + set_str + where_str
            cursor.execute(sql, val)
            conn.commit()


def delete_row(id):
    with closing(get_conn('easychess')) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            sql = f"""DELETE FROM games WHERE id={id}"""
            cursor.execute(sql)
            conn.commit()


def select_all():
    with closing(get_conn('easychess')) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            sql = f"""SELECT * FROM games"""
            cursor.execute(sql)
            return cursor.fetchall()


def select(sql):
    with closing(get_conn('easychess')) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
