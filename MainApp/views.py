from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from MainApp.models import Doc
from MainApp.forms import DocUploadForm

from multiprocessing.pool import ThreadPool
import os
import requests
import base64
import json

def adddoc(title):

    title2=title
    title="http://18.191.180.251:8099/"+title
    
    sending_request={
      "requests":[
        {
          "image":{
            "source":{
              "imageUri":title
            }
          },
          "features": [
            {
              "type": "TEXT_DETECTION"
            }
          ]
        }
      ]
    }



    data=json.dumps(sending_request)
    #data=sending_request
    headers=  {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    url="https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDpzf-Awq52jLEK7iy_9-xIQicjNXwaZfY"   
    
    r=requests.post(url,data=data,headers=headers)
    result=r.json()
    #print(result)
    result_text=result['responses'][0]['textAnnotations'][0]['description']
    result_text_arr=result_text.split('\n')
    result_text=' '.join(result_text_arr)
    print(result_text)
    es=Elasticsearch()

    doc={
         'des':result_text,
         'link':title2,
          }
    es.index(index='docnode',doc_type='1',id=title2,body=doc)

def home(request):
    return render(request,'home.html')

def search(request):
    if request.method == 'POST':
        doc={}
        if "find_all" in request.POST:
            doc = {
 	        "query":
 	        {
 		        "match_all":{}
 		    
     	        }
             }
        else:
            query = request.POST['query']
            doc = {
 	        "query":
 	        {
 		        "match":
 		        {
 		 	        "des":
 			        {
 			 	        "query":query,
  			        }
 		        }
     	        }
             }
        es=Elasticsearch()
        res = es.search(index="docnode", body=doc)
        res=res['hits']['hits']
        titles=list()
        
        for entry in res:
           source=entry['_source']
           titles.append(source['link'])
        return render(request, 'search_result.html', {'titles': titles})
    
    return render(request, 'search.html')

def upload(request):
    if request.method =="POST":
        #form = DocUploadForm(request.POST, request.FILES)
        #if form.is_valid():
        #   newdoc = Profile()
        #    newdoc = Profile(img = request.FILES['img'])
        #    newdoc.save()
        #else:        
        #    return render(request,'uploaded.html')
        #newdoc=Doc()
        newdoc=Doc(doc_main_img=request.FILES['img'])
        newdoc.save()
        
        title=newdoc.doc_main_img.path
        title=os.path.basename(title)
        adddoc(title)
        return render(request,'uploaded.html',{'title':title})
    return render(request,'upload.html')