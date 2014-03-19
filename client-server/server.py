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
    if query:
        response = solr_handler.__call__(query, facet='true', facet_field=['creator_facet', 'publisher_facet', 'contributor_facet', 'year_facet'])
        return render_template('search.html', query=query, response=response)
    return render_template('search.html')


@app.route('/refined', methods=['GET'])
def refined_search():
    query = []
    for k,v in request.args.items():
        if v:
            query.append('{}:{}'.format(k,v))
    query = " AND ".join(query)
    if query:
        print query
        response = solr_handler.__call__(query)#, facet='true', facet_field=['creator', 'publisher', 'contributor'])
        return render_template('refined_search.html', response=response)


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
