from django.shortcuts import render

# Create your views here.
def sign_in(request):
    return render(request, 'frontend/signin.html')

def sign_up(request):
    return render(request, 'frontend/signup.html')