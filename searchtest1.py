#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import libraries to help read and create PDF
import PyPDF2
from fpdf import FPDF
import base64
import json
from flask import Flask, jsonify, request
from datetime import datetime

# import the Elasticsearch low-level client library
from elasticsearch import Elasticsearch
# create a new client instance of Elasticsearch
elastic_client = Elasticsearch(hosts=["localhost"])
es = Elasticsearch("http://localhost:9200/")
app = Flask(__name__)

result = elastic_client.get(index="pdf", doc_type='_doc', id=42)

# print the data to terminal
result_data = result["_source"]["data"]
#print ("\nresult_data:", result_data, '-- type:', type(result_data))

# decode the base64 data (use to [:] to slice off
# the 'b and ' in the string)
decoded_pdf = base64.b64decode(result_data[2:-1]).decode("utf-8")

json_dict = json.loads(decoded_pdf)


@app.route('/search/<value>', methods=['GET'])
def search(value):
    keyword = value

    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["pdf", "title"]
            }
        }
    }

    res = es.search(index="pdf", doc_type="_doc", body=body)

    return jsonify(res['hits']['hits'])

app.run(port=5001, debug=True)