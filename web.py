import cherrypy
import os.path
import redis
from jinja2 import Environment, FileSystemLoader

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

        list_of_hash = []
        for i in range(3000):
            if conn.hget(i, 'SC_NAME') == None:
                continue
            if search.lower().strip() in conn.hget(i, 'SC_NAME').decode('utf-8').strip().lower():
                data_dict = {k.decode('utf-8'): v.decode('utf-8') for (k, v) in conn.hgetall(i).items()}
                list_of_hash.append(data_dict)

        return template.render(top_10=list_of_hash)


conn = redis.Redis('localhost')
configfile = os.path.join(os.path.dirname(__file__),'server.conf')
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
env = Environment(loader=FileSystemLoader(CUR_DIR), trim_blocks=True)
cherrypy.quickstart(index(),config= configfile)