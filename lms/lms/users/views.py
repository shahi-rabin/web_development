from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse


from django.contrib.auth import logout

# from users.models import Profile

from django.core.validators import validate_email

from users.models import UserDetails

# Create your views here.


def home(request):
    templatePath = 'index.html'
    context = {}

    if request.method == 'POST':          
        username = request.POST['username']        
        password = request.POST['password'] 

        try:
            validate_email(username)
            print(username)
            existinguser = User.objects.filter(email=str(username)).first()

            print(existinguser)

            if not existinguser:
                print("Not Existing user")
            else:
                user = authenticate(request, username=existinguser, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')

        except:
            context['error'] = "Invalid Username or Password"
            return render(request, templatePath, context)
    
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            print("logged in")
            return redirect('dashboard')
    else:
        print("not logged in")
        return render(request, templatePath)
            

def register(request):
    context = {}
    templatePath = 'register.html'

    if request.method == 'POST':
        username = request.POST['user']
        stdId = request.POST['stdId']
        batch = request.POST['batch']
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['pwd1']
        password2 = request.POST['pwd2']


        if User.objects.filter(email=email).exists():
            context['email_taken'] = "This email is already registered."
        print ("1")

        print ("1")
            
        if User.objects.filter(username = username).exists():
            context["username_taken"] = "This username is already taken"

        print ("1")

        if password1 != password2:
            context['password_err'] = "Password Not Matched"
            print ("21")
        else:
            password = password1
            print ("22")

        

        if len(context) == 0:
            try:      
                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName)
                user.save()
                UserDetails.objects.create(user=user, studentId=stdId, batchNo=batch)

                return redirect('/')
            except:
                context['error'] = "Error Occured"
                return render(request,templatePath,context)                
        else:
            return render(request,templatePath,context)

    return render(request, templatePath)


def logout_view(request):
    logout(request)
    return redirect('home')