from django.shortcuts import render, HttpResponse, redirect
from .models import *
import FileShare.settings as settings
import os
from django.templatetags.static import static
from django.http import FileResponse

#############################################################
# FILE SHARING
#############################################################
def FileInput(request):
    if (request.method == "POST"):
        files = request.FILES.getlist('file_input')

        Link = []
        file_count = 0
        for file in files:
            file_name = file.name
            file_path = os.path.join(settings.BASE_DIR, 'Files\\', file_name)

            # Checking if the file with the same name already exists
            count = 1
            while os.path.exists(file_path):
                # file.name[0] == ABC   || file.name[1] == .txt  ==> For file ABC.txt
                name, extension = os.path.splitext(file_name)
                new_name = f"{name}_{count}{extension}"
                file_path = os.path.join(settings.BASE_DIR, 'Files\\', new_name)
                count += 1
            
            print(f"File path: {file_path}")
            # Create directories if they don't exist
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            link = generate_link()
            FileLink.objects.create(link = link, path = file_path, name = file.name)

            Link.append(link)
            file_count += 1
            context = {"Link" : Link}
        return render(request,'Base_Share/link_generation.html',context=context)
      
    return render(request,"Base_Share/home.html")

def LinkGeneration(request):
    if (request.method == "POST"):
        link = request.POST["Link"]
        identifier = request.POST["identifier"]

        # Check for the identifier name being Primary key.
        for entity in LinkIdentifier.objects.all():
            if (entity.identifier == identifier):
                return HttpResponse("<h1> The identifier name already exists. </h1>")
            
        link = FileLink.objects.filter(link = link)[0] # Get the FileLink Object.
        LinkIdentifier.objects.create(link = link, identifier = identifier).save()
        return redirect("Base_Share:Public Links")
    
    return render(request,"Base_Share/link_generation.html")

def PublicLinks(request):
    Links = []

    for entity in LinkIdentifier.objects.all():
        Links.append({"Link" : entity.file_link(), "Identifier": entity.identifier})   

    exists = False
    if (Links != []):   exists = True 
    content = {
        "Links" : Links,
        "Exists" : exists,
        "url" : "http://127.0.0.1:8000/files/"
    }
    return render(request,"Base_Share/public_links.html",context=content)

def LinkToFile(request, links = ""):
    obj = FileLink.objects.filter(link = links)[0]

    return FileResponse(open(obj.path,'rb'))

def RecieveFile(request):
    if (request.method == "POST"):
        code = request.POST["link-code"]

        link = FileLink.objects.filter(link = code)[0].link
        
        if (link == ""):
            return HttpResponse("There is no link with this code")
        else:
            context = {"Link" : [link]}
            return render(request,"Base_Share/link_generation.html",context = context)

    return render(request,'Base_Share/file_recieve.html')

#############################################################
# TEXT EDITING
#############################################################
def TextEditor(request):
    return render(request,"Base_Share/Text_editor.html")