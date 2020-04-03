from flask import Flask, jsonify, request, render_template

from sys import argv

app = Flask(__name__)

@app.route('/google-charts/line-chart')
def google_line_chart():
    data = {
        '2006' : 1000,
        '2007' : 1050,
        '2008' : 900,
        '2009' : 1170
        }
    return render_template('line-chart.html', data=data)

@app.route('/')
def index():
    return "<h1>Test page</h1>"

if __name__ == "__main__":
    
    if len(argv) == 2:
        app.run(host='0.0.0.0', port=int(argv[1]))
    else:
        app.run(port=8080)