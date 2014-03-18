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
solr_handler = solr.SearchHandler(s, settings.HANDLER_STRING)

#----- PAGES -------------------------------------
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    print query
    if query:
        results = solr_handler.__call__(query)
        return render_template('search.html', query=query, results=results)
    #if request.method == 'POST':
    #    query = request.form['query']
    #    results = s.query('title:marmoset')
    #    return render_template('search.html', query=query, results=results)
    # set query to 'search for something'
    return render_template('search.html')


@app.route('/refined', methods=['GET', 'POST'])
def refined_search():
    return render_template('refined_search.html')    


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#----- HELPERS ------------------------------------
def get_results():
    with open("./results.json") as f:
        return json.load(f)['response']['docs']

if __name__ == "__main__":
    app.run(port = settings.SERVER_PORT)
