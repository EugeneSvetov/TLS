from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os

def home(request):
    return render(request, 'AnalysisTrafic/index.html')


def download_file(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['myfile1']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)

    return render(request, 'AnalysisTrafic/download_file.html')


def dashboard(request):
    name_file = os.listdir("media")[0]


    return render(request, 'AnalysisTrafic/dashboard.html')