import cherrypy
import os.path
import redis
from jinja2 import Environment, FileSystemLoader
import urllib
import sys
import signal

def signal_handler(signal, frame):
	print('Exiting...')
	cherrypy.engine.exit()

signal.signal(signal.SIGINT, signal_handler)


class index:

    @cherrypy.expose()
    def index(self):

        template = env.get_template('index.html')

        top_10_index_list = conn.zrange('top_10', 0, -1, desc=True)

        list_of_hash = []

        for index in [int(i.decode('utf-8')) for i in top_10_index_list]:
            conn.hgetall(index)

            data_dict = {k.decode('utf-8'): v.decode('utf-8') for (k, v) in conn.hgetall(index).items()}
            list_of_hash.append(data_dict)

        return template.render(top_10=list_of_hash)

    @cherrypy.expose()
    def search(self, search=None):

        template = env.get_template('index.html')

        maxm = 0
        for i in conn.keys('*'):
            try:
                i = int(i.decode('utf-8'))
                if i > maxm: maxm = i
            except:
                continue

        list_of_hash = []
        for i in range(maxm+1):
            if conn.hget(i, 'SC_NAME') == None:
                continue
            if search.lower().strip() in conn.hget(i, 'SC_NAME').decode('utf-8').strip().lower():
                data_dict = {k.decode('utf-8'): v.decode('utf-8') for (k, v) in conn.hgetall(i).items()}
                list_of_hash.append(data_dict)


        return template.render(top_10=list_of_hash, search=search, search_flag = True)

# if __name__ == '__main__':

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
env = Environment(loader=FileSystemLoader(CUR_DIR), trim_blocks=True)
try:
    url = urllib.parse.urlparse(os.environ['REDIS_URL'])
    conn = redis.Redis(host=url.hostname, port=url.port, db=0, password=url.password)
except:
    conn = redis.Redis('127.0.0.1')

cherrypy.server.socket_host = '127.0.0.1'
cherrypy.server.socket_port = 8000
cherrypy.server.thread_pool = 10
cherrypy.config.update({'engine.autoreload.on': False})
cherrypy.config.update({'environment': 'embedded'})
cherrypy.server.unsubscribe()
cherrypy.engine.signals.subscribe()
cherrypy.engine.start()

# cherrypy.quickstart(index())

cherrypy.tree.mount(index(), '/', {})
application = cherrypy.tree