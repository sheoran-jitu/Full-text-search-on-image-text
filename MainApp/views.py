from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
#es=ElasticSearch()

def home(request):
    es=Elasticsearch()
    doc = {
 	    "query":
 	    {
 		    "match":
 		    {
 		 	    "st":
 			    {
 			 	    "query":"yaar",
  			    }
 		    }
     	    }
         }

    res = es.search(index="testingnode", body=doc)
    res=res['hits']['hits']
    doc_names=list()
    for x in res:
        y=x['_source']
        for z in y:
            doc_names.append(z)
            
    response_html = '<br>'.join(doc_names)

    return HttpResponse(response_html)