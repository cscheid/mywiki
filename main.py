#!/usr/bin/env python

from flask import Flask, request, jsonify, safe_join, escape, redirect
from jinja2 import Environment, FileSystemLoader

import json
import sys
import os

app = Flask(__name__)
env = Environment(loader=FileSystemLoader('templates'))

##############################################################################

def save_file(filename, content):
    path = safe_join("data", filename)
    f = file(path, 'w')
    f.write(content)
    f.close()
    os.system('cd data; git add %s; git commit -m"checkin"' % filename)

##############################################################################

@app.route('/')
def hello_world():
    return '<a href="/static/test.html">Go here instead</a>.'

@app.route('/view/')
def main_view():
    return redirect('/view/Main')

view_template = env.get_template('view.html')
edit_template = env.get_template('edit.html')

@app.route('/view/<path:filename>')
def view(filename):
    try:
        f = file(safe_join('data', filename))
    except IOError:
        return redirect('/edit/%s' % filename)
    return view_template.render(title=filename, content=f.read())

@app.route('/edit/<path:filename>')
def edit(filename):
    path = safe_join('data', filename)
    try:
        f = file(path)
    except IOError:
        save_file(filename, '')
        f = file(path)
    return edit_template.render(title=filename, content=f.read())

@app.route('/save/<path:filename>', methods=['POST'])
def save(filename):
    content = request.form.get('data')
    save_file(filename, content)
    return "OK"

if __name__ == '__main__':
    app.debug = True
    app.run()
