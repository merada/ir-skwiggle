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
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return search_query(request.form)
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        query = request.form['query']
        results = s.query('title:marmoset')
        for r in results:
            print r['title']
        print "noooooo..."
    else:
        query = "Local JSON file"
        results = get_results() # test file
    return render_template('search.html', query=query, results=results)

@app.route('/search', methods=['GET', 'POST'])
def search_query(query):
    #results = get_results()
    results = s.query('title:marmoset')
    for r in results:
        print r['title']
    print "noooooo..."
    return render_template('search.html', query=query, results=results)

@app.route('/refined', methods=['GET', 'POST'])
def refined_search():
    return render_template('refined_search.html')    

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#----- HELPERS ------------------------------------
def get_results():
    with open("./results.json") as f:
        return json.load(f)['response']['docs']

if __name__ == "__main__":
    app.run(port = settings.SERVER_PORT)
