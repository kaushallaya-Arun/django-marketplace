from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import error
from .forms import LoginForm,SignupForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, User

# Create your views here.

#Home page view(index.html file)
def home_page_view(request):
     # Your logic for the homepage, e.g., fetching data from the database
    context = {'message': 'Welcome to market place'}
    return render(request,'index.html',context)

#login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  

            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Use User model here
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error(request, 'Invalid username or password') 

                print("error in the credentials") # Use error message
                # return JsonResponse({'error': 'Invalid credentials'})
                return render(request, 'login.html',{'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()
        print("Bad thig happend")
    return render(request, 'login.html')

#Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set password after saving to avoid hashing issues
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

#Dashboard view
@login_required
def dashboard(request):  

    # Access user information
    user = request.user
    context = {'user': user}
    return render(request, 'dashboard.html', context)
