from django.db import models

# Create your models here.
from django.db import models

class Doc(models.Model): 
    #name = models.CharField(max_length=50) 
    doc_main_img = models.ImageField(upload_to='images/') 