from flask import Flask, jsonify, request,render_template
from elasticsearch import Elasticsearch
from datetime import datetime
es = Elasticsearch("http://localhost:9200/")

app = Flask(__name__)

@app.route('/pdf', methods=['GET'])
def index():
    results = es.get(index='pdfclearn', doc_type='_doc', id='44')
    return jsonify(results['_source'])
    

@app.route('/pdf/<id>', methods=['GET'])
def index_by_id(id):
    results = es.get(index='pdfclearn', doc_type='_doc', id=id)
    return jsonify(results['_source'])



@app.route('/search/<keyword>', methods=['POST','GET'])
def search(keyword):
    keyword = keyword

    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["data"]
            }
        }
    }

    res = es.search(index="pdfclearn", doc_type="_doc", body=body)

    return jsonify(res['hits']['hits'])

@app.route("/searhbar")
def searhbar():
    return render_template("index.html")

@app.route("/searhbar/<string:box>")
def process(box):
    query = request.args.get('query')
    if box == 'names':
         keyword = box

    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["data"]
            }
        }
    }

    res = es.search(index="pdfclearn", doc_type="_doc", body=body)

    return jsonify(res['hits']['hits'])

app.run(port=5003, debug=True)
