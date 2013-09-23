# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import *
from bottle import __version__ as bottleVer
from bottle import jinja2_template as template
from config import JINJA2TPL_PATH
TEMPLATE_PATH.insert(0, JINJA2TPL_PATH)



APP = Bottle()
#APP.mount('/up', __import__('mana4up').APP)
APP.mount('/api', __import__('mana4api').APP)
#APP.mount('/mana', __import__('mana4sys').APP)

@APP.route('/')
#@view('404.html')
def index():
    return template('index.html')

#@view('404.html')
@APP.error(404)
def error404(error):
    return template('404.html')

@APP.route('/favicon.ico')
def favicon():
    abort(204)
    
@APP.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')
    

if __name__ == '__main__':
    debug(True)
    #0.0.0.0
    run(app, host="0.0.0.0",reloader=True)
