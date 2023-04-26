from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

app_name = "Base_Share"

urlpatterns = [
    path('', PublicLinks, name = "Public Links"),
    path('file-input',FileInput,name = "File Input"),
    path('link-generate', LinkGeneration, name = "Link Generation"),
    path('file-recieve', RecieveFile, name = "RecieveFile"),

    path('files/<str:links>', LinkToFile, name="Link to File")
]
urlpatterns += staticfiles_urlpatterns()