from django.db import models
import random
import string

# Generate random link.
def generate_link():
    links = FileLink.objects.all()

    res = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    # Checking whether generated string is unique or not.
    for i in links:
        if (i.link == res):
            res = generate_link()
            break
    return res

# Create your models here.
class FileLink(models.Model):
    link = models.CharField(max_length = 255, primary_key= True)
    path = models.TextField()
    name = models.CharField(max_length = 255, null = False)

    def __str__(self):
        return self.name




class LinkIdentifier(models.Model):
    identifier = models.CharField(max_length=255, primary_key= True)
    link = models.ForeignKey(FileLink, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.identifier

    def file_link(self):
        return self.link.link
# While Uploading the file :-
# 1. Check the format type.
# 2. Use try except to check the file existance.
# 3. If not exists then save this file there.
# 4. Else in the name field keep the name same and do <name>_<count> until the file path gets unique.

# For link identifier :-
# 1. Same link can have mulitple Identifiers.
# 2. Identifiers should be unique For identification.