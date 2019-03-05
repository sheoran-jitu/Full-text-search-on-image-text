from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch

def home(request):
    return render(request,'home.html')

def search(request):
    if request.method == 'POST':

        query = request.POST['query']
        es=Elasticsearch()
        doc = {
 	    "query":
 	    {
 		    "match":
 		    {
 		 	    "st":
 			    {
 			 	    "query":query,
  			    }
 		    }
     	    }
         }
        res = es.search(index="testingnode", body=doc)
        res=res['hits']['hits']
        titles=list()
        
        for entry in res:
           source=entry['_source']
           titles.append(source['name'])

        return render(request, 'search_result.html', {'titles': titles})
    
    return render(request, 'search.html')

def upload(request):
    return render(request,'upload.html')