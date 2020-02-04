#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import libraries to help read and create PDF
import PyPDF2
from fpdf import FPDF
import base64

from flask import Flask, jsonify, request, render_template,  json
from datetime import datetime
import pandas as pd

# import the Elasticsearch low-level client library
from elasticsearch import Elasticsearch
# create a new client instance of Elasticsearch
elastic_client = Elasticsearch(hosts=["localhost"])
es = Elasticsearch("http://localhost:9200/")
app = Flask(__name__)

""" # create a new PDF object with FPDF
pdf = FPDF()

# use an iterator to create 10 pages
for page in range(10):
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(150, 12, txt="Object Rocket ROCKS!!", ln=1, align="C")

# output all of the data to a new PDF file
pdf.output("object_rocket.pdf")
 """
'''
read_pdf = PyPDF2.PdfFileReader("object_rocket.pdf")
page = read_pdf.getPage(0)
page_mode = read_pdf.getPageMode()
page_text = page.extractText()
print (type(page_text))
'''
#with open(path, 'rb') as file:

# get the PDF path and read the file
file = "Sheet3.pdf"
read_pdf = PyPDF2.PdfFileReader(file, strict=False)
#print (read_pdf)

# get the read object's meta info
pdf_meta = read_pdf.getDocumentInfo()

# get the page numbers
num = read_pdf.getNumPages()
print ("PDF pages:", num)

# create a dictionary object for page data
all_pages = {}

# put meta data into a dict key
all_pages["meta"] = {}

# Use 'iteritems()` instead of 'items()' for Python 2
for meta, value in pdf_meta.items():
    print (meta, value)
    all_pages["meta"][meta] = value

x = 44
# iterate the page numbers
for page in range(num):
    data = read_pdf.getPage(page)
    #page_mode = read_pdf.getPageMode()

    # extract the page's text
    page_text = data.extractText()
    
    # put the text data into the dict
    all_pages[page] = page_text

    body_doc2 = {"data": page_text}
    result3 = elastic_client.index(index="pdfclearn", doc_type="_doc", id=x, body=body_doc2)
    x += 1

@app.route('/', methods=['GET'])
def index():
    results = es.get(index='pdfclearn', doc_type='_doc', id='44')
    return jsonify(results['_source'])
    

@app.route('/<id>', methods=['GET'])
def index_by_id(id):
 
    return jsonify(json_dict[id])

app.run(port=5003, debug=True)





