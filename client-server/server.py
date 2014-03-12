from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True
Bootstrap(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = "RESULT"
    if request.method == 'POST':
        if request.form['query'] == "dragon":
            return "Here be dragons"
        else:
            return "No dragons be here"
    return render_template('home.html', result=results)

@app.route("/dragon")
def merada():
    return "<button>scales</button>"

@app.route("/test")
def test_bootstrap():
    return render_template('test.html')

@app.route("/layout")
def test_layout():
    return render_template('layout.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()
