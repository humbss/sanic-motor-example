from sanic import Sanic
from sanic.response import json
from db.motor_connection import connect
from api.routes import add_routes
import uvloop
import asyncio
import aiotask_context as context
from sanic.log import logger

"""
Application Initialization:

The middleware request will set important variables like db info into the context,
this is important in order to reconnect to database.
"""
app = Sanic()
@app.listener('before_server_start')
def init(sanic, loop):
    connect(app.config.get('dbhost'), app.config.get('dbport'))


@app.middleware('request')
async def add_key(request):
    context.set('db_host', app.config.get('dbhost'))
    context.set('db_port', app.config.get('dbport'))
    context.set('request', request)

"""
Routes Initialization
"""
add_routes(app)

if __name__ == '__main__':
    asyncio.set_event_loop(uvloop.new_event_loop())
    server = app.create_server(
        host="0.0.0.0", port=8000, return_asyncio_server=True)
    loop = asyncio.get_event_loop()
    loop.set_task_factory(context.task_factory)
    task = asyncio.ensure_future(server)
    try:
        loop.run_forever()
    except:
        loop.stop()
