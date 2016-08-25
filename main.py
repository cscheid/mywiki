#!/usr/bin/env python

from flask import Flask, request, jsonify, safe_join, escape, redirect, Response
from jinja2 import Environment, FileSystemLoader

import git
import json
import sys
import codecs

app = Flask(__name__)
env = Environment(loader=FileSystemLoader('templates'))

from conf import Conf

repo = git.Repo('data')

##############################################################################

def save_file(filename, content):
    path = safe_join("data", filename)
    f = codecs.open(path, 'w', 'utf-8')
    f.write(content)
    f.close()
    repo.index.add([filename])
    repo.index.commit("checkin")

##############################################################################

@app.route('/')
def hello_world():
    return redirect('%s/view/Main' % Conf["prefix"])

@app.route('/view/')
def main_view():
    return redirect('%s/view/Main' % Conf["prefix"])

view_template = env.get_template('view.html')
edit_template = env.get_template('edit.html')
version_template = env.get_template('versions.html')


@app.route('/view/<path:filename>')
def view(filename):
    try:
        f = codecs.open(safe_join('data', filename), 'r', 'utf-8')
        content = f.read()
    except IOError:
        return redirect('%s/edit/%s' % (Conf["prefix"], filename))
    return view_template.render(title=filename, content=repr(content)[1:], **Conf)

@app.route('/edit/<path:filename>')
def edit(filename):
    path = safe_join('data', filename)
    try:
        f = codecs.open(path, 'r', 'utf-8')
    except IOError:
        save_file(filename, '')
        f = codecs.open(path, 'r', 'utf-8')
    return edit_template.render(title=filename, content=f.read(), **Conf)

@app.route('/versions/<path:filename>')
def show_versions(filename):
    result = repo.git.log(filename).split('\n')
    hashes = list(l[7:] for l in result if l.startswith('commit '))
    dates = list(l[6:] for l in result if l.startswith('Date: '))
    commits = []
    
    for (hash, date) in zip(hashes, dates):
        commits.append({
            "hash": hash,
            "date": date
            })
    return version_template.render(title=filename, commits=commits, **Conf)
    # return str(repo.refs.log.RefLog(filename))

@app.route('/get/<path:filename>')
def get(filename):
    try:
        f = codecs.open(safe_join('data', filename), 'r', 'utf-8')
        content = f.read()
    except IOError:
        return Response("Not found", status=404, mimetype="text/plain")
    return Response(content, status=200, mimetype="text/plain")

@app.route('/get_version/<path:filename>/<path:commit>')
def get_file(filename, commit):
    result = repo.git.show(commit + ":" + filename)
    return Response(result, mimetype='text/plain')

@app.route('/save/<path:filename>', methods=['POST'])
def save(filename):
    content = request.form.get('data')
    save_file(filename, content)
    return "OK"

app.debug = True
if __name__ == '__main__':
    app.run(port=8300)
