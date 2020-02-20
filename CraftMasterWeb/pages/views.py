from django.shortcuts import render
# from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'index.html')
def team(request):
    return render(request, 'team.html')
def downloads(request):
    return render(request, 'downloads.html')
