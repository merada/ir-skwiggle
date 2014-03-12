import json
import settings
import solr
from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap

# app setup
app = Flask(__name__)
app.debug = True
Bootstrap(app)

# solr setup
s = solr.SolrConnection(settings.SOLR_URL)

#----- PAGES -------------------------------------
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        results = s.query(request.form['query']) # basic query
    else:
        results = get_results() # test file
    return render_template('search.html', results=results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#----- HELPERS ------------------------------------
def get_results():
    with open("./results.json") as f:
        return json.load(f)['response']['docs']

if __name__ == "__main__":
    app.run(port = settings.SERVER_PORT)
