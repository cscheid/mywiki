#!/usr/bin/env python

from flask import Flask, request, jsonify, safe_join, escape, redirect
from jinja2 import Environment, FileSystemLoader

import json
import sys
import os
import codecs

app = Flask(__name__)
env = Environment(loader=FileSystemLoader('templates'))

from conf import Conf

##############################################################################

def save_file(filename, content):
    path = safe_join("data", filename)
    f = codecs.open(path, 'w', 'utf-8')
    f.write(content)
    f.close()
    os.system('cd data; git add %s; git commit -m"checkin"' % filename)

##############################################################################

@app.route('/')
def hello_world():
    return redirect('%s/view/Main' % Conf["prefix"])

@app.route('/view/')
def main_view():
    return redirect('%s/view/Main' % Conf["prefix"])

view_template = env.get_template('view.html')
edit_template = env.get_template('edit.html')

@app.route('/view/<path:filename>')
def view(filename):
    try:
        f = codecs.open(safe_join('data', filename), 'r', 'utf-8')
        content = f.read()
    except IOError:
        return redirect('%s/edit/%s' % (Conf["prefix"], filename))
    return view_template.render(title=filename, content=content, **Conf)

@app.route('/edit/<path:filename>')
def edit(filename):
    path = safe_join('data', filename)
    try:
        f = codecs.open(path, 'r', 'utf-8')
    except IOError:
        save_file(filename, '')
        f = codecs.open(path, 'r', 'utf-8')
    return edit_template.render(title=filename, content=f.read(), **Conf)

@app.route('/save/<path:filename>', methods=['POST'])
def save(filename):
    content = request.form.get('data')
    save_file(filename, content)
    return "OK"

if __name__ == '__main__':
    app.run(port=8300)
