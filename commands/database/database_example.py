import logging
import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# sqlite with memory
# engine = create_engine("sqlite:///:memory:", future=True)

# sqlite with file, https://docs.sqlalchemy.org/en/14/dialects/sqlite.html
engine = create_engine("sqlite:///example.sqlite3", future=True)

# pgsql, https://docs.sqlalchemy.org/en/14/dialects/postgresql.html
# engine = create_engine(
#     "postgresql+psycopg2://postgres:admin@127.0.0.1:5432/data",
#     pool_recycle=1800,
#     future=True,
#     echo=False,
#     pool_pre_ping=True
# )

# mysql, https://docs.sqlalchemy.org/en/14/dialects/mysql.html
# engine = create_engine(
#     "mysql+mysqldb://scott:tiger@192.168.0.134/test?charset=utf8mb4&binary_prefix=true",
#     connect_args={
#         "ssl": {
#             "ca": "/home/gord/client-ssl/ca.pem",
#             "cert": "/home/gord/client-ssl/client-cert.pem",
#             "key": "/home/gord/client-ssl/client-key.pem"
#         }
#     }
# )

# oracle, http://docs.sqlalchemy.org/en/latest/dialects/oracle.html
# mssql, http://docs.sqlalchemy.org/en/latest/dialects/mssql.html

Session = scoped_session(sessionmaker(bind=engine, future=True))


def commit_session():
    try:
        Session.commit()
    except Exception as exc:
        logging.error(traceback.format_exc())
        logging.error(f'Commit failed, session will be rollback: {exc}')
        Session.rollback()
        raise
    finally:
        Session.close()


def flush_session():
    Session.flush()
