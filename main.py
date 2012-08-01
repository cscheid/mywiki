#!/usr/bin/env python

from flask import Flask, request, jsonify, safe_join, escape, redirect
import json
import sys
import os

app = Flask(__name__)

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

@app.route('/view/<path:filename>')
def view(filename):
    try:
        f = file(safe_join('data', filename))
    except IOError:
        return redirect('/edit/%s' % filename)
    return """<html>
    <head><title>%s</title>
    <script type='text/javascript' src='/static/js/jquery.js'></script>
    <script type='text/javascript' src='/static/js/showdown.js'></script>
    </head>
    <body><div style='display:none' id='content'>%s</div><div id='output'></div><hr><button id='edit'>edit</button>
    <script>
    $('#edit').click(function() {
        window.location = '/edit/' + '%s'
    })
    var new_html = (new Showdown.converter()).makeHtml($('#content').text());
    $(output).html(new_html);
    </script>
</body></html>""" % (filename, escape(f.read()), filename)

@app.route('/edit/<path:filename>')
def edit(filename):
    path = safe_join('data', filename)
    try:
        f = file(path)
    except IOError:
        save_file(filename, '')
        f = file(path)
    return """<html><head><title>Editing %s...</title>
    <script type='text/javascript' src='/static/js/jquery.js'></script>
    </head>
    <body>
    <textarea id='text-content'>%s</textarea>
    <button id='save'>save</button>
    <button id='cancel'>cancel</button>
    <script>
    $('#save').click(function() {
        $.post('/save/%s',
               { data: $('#text-content').val() },
               function(data) {
                   window.location = '/view/%s';
               });
    })
    </script>
</body></html>""" % (filename, escape(f.read()), filename, filename)

@app.route('/save/<path:filename>', methods=['POST'])
def save(filename):
    content = request.form.get('data')
    save_file(filename, content)
    return "OK"

if __name__ == '__main__':
    app.debug = True
    app.run()
