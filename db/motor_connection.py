
import motor.motor_asyncio
import aiotask_context as context
from sanic.log import logger

db = None

'''
    Connects to Mongo DB, store client+collection into var.
    this is using a test collection called test_database, is higly 
    recommended to change by a function argument.
'''
def connect(db_host, db_port):
    logger.info("[DB] Establishing connection DB connection in: %s:%s ", db_host, db_port)

    if db_host is None:
        db_host = context.get('db_host')

    if db_port is None:
        db_port = context.get('db_port')

    db = (motor.motor_asyncio.AsyncIOMotorClient(
        db_host,
        db_port
    )).test_database
   
    return db

'''
    Retrieve mongo database connection if it exists, else create one.
    DB connection has been stored into db variable, host and port came
    from context.
'''
def get_connection():
    try:
        if db is not None:
            return db
        raise Exception('DB connection not found.')
    except Exception as e:
        logger.info("Trying reconnect to DB: %s:%s ",
                    context.get('db_host'), context.get('db_port'))
        return connect(context.get('db_host'), context.get('db_port'))
