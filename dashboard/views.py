from django.shortcuts import render

# Create your views here.
def dashboardView(request):
    return render(request, "dashboard/index.html")