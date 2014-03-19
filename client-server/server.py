import json
import settings
import solr
from flask import Flask
from flask import request
from flask import render_template
from flask.ext.paginate import Pagination
from flask_bootstrap import Bootstrap

# app setup
app = Flask(__name__)
app.debug = True
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
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
    page = int(request.args.get('page', 1))
    rows = settings.RESULTS_PER_PAGE
    start = (page-1) * rows
    response = []
    total = 0
    if query:
        facet_fields = settings.FACET_FIELDS
        response = solr_handler.__call__(query, start=start, rows=rows, facet='true', facet_field=facet_fields)
        total = response.numFound

        #for facetfield in response.facet_counts['facet_fields']:
        # for facetfield in response.facet_counts['facet_fields']:
        #     for element in response.facet_counts['facet_fields'][facetfield]:
        #         if response.facet_counts['facet_fields'][facetfield][element] > 0:
        #             print(response.facet_counts['facet_fields'][facetfield][element])
     
    pagination = Pagination(page=page, per_page=rows, total=total, search=False, bs_version=3)
    return render_template('search.html', response=response, pagination=pagination)

@app.route('/searchFacet', methods=['GET'])
def searchFacet():
    # query = request.args.get('query', '')
    # if query:

    #     response = solr_handler.__call__(query, facet='true', facet_field=['creator_facet', 'publisher_facet', 'contributor_facet', 'date_facet', 'language_facet', 'source_facet', 'type_facet', 'signature_facet'])

    #     #for facetfield in response.facet_counts['facet_fields']:
    #     # for facetfield in response.facet_counts['facet_fields']:
    #     #     for element in response.facet_counts['facet_fields'][facetfield]:
    #     #         if response.facet_counts['facet_fields'][facetfield][element] > 0:
    #     #             print(response.facet_counts['facet_fields'][facetfield][element])
        

    #     return render_template('search.html', query=query, response=response)
    return render_template('search.html')


@app.route('/refined', methods=['GET'])
def refined_search():
    query = []
    for k,v in request.args.items():
        if v and k != "page":
            query.append('{}:{}'.format(k,v))
    query = " AND ".join(query)
    page = int(request.args.get('page', 1))
    rows = settings.RESULTS_PER_PAGE
    start = (page-1) * rows
    response = []
    total = 0
    if query:
        response = solr_handler.__call__(query, start=start, rows=rows, facet='true', facet_field=settings.FACET_FIELDS)
        total = response.numFound
    pagination = Pagination(page=page, per_page=rows, total=total, search=False, bs_version=3)
    return render_template('refined_search.html', response=response, pagination=pagination)    


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
