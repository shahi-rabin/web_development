from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.core.validators import validate_email

from dashboard.models import LogisticsData

from main.models import Book


# Create your views here.


def mainLogin(request):
    templatePath = 'main/login.html'
    context = {}

    if request.method == 'POST':          
        username = request.POST['username']        
        password = request.POST['password'] 

        # try:
        validate_email(username)
        print("email validated")
        print(username)
        existinguser = User.objects.filter(email=str(username)).first()
        print(existinguser)

        if not existinguser:
            print("Not Existing user")
        else:
            print("checking super user")
            if existinguser.is_superuser:
                print(1)
                user = authenticate(request, username=existinguser, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    print("redirecting to dashboard")
                    return redirect('admin_dashboard')
            else:
                context['error'] = "Admin Account Does Not Exist"
                return render(request, templatePath, context)
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            print("logged in")
            return redirect('admin_dashboard')
        else:
            print("not super user")
    else:
        print("not logged in first time")
        return render(request, templatePath)
        

def admin_dashboard(request):
    templatePath = "main/main_dashboard.html"
    context = {}

    if request.method == 'POST':
        if "book" in request.POST:
            
            bookName = request.POST['bookName']        
            bookAuthor = request.POST['authorName'] 

            newbook = Book.objects.create(bookName = bookName, authorName = bookAuthor)
            newbook.save()

            return redirect('admin_dashboard')

        elif "entry_record" in request.POST:
            user = request.POST['user']
            returnDate = request.POST['return_date']
            currentBookId = request.POST['currentBook']

            username = User.objects.get(pk=user)
            currentBook = Book.objects.get(pk=currentBookId)

            print (currentBook)            
            bookAlreadyAdded = LogisticsData.objects.filter(bookName=currentBook).filter(studentId=username).exists()
            
            if not bookAlreadyAdded:
                currentLogisticEntry = LogisticsData.objects.create(studentId = username, bookName= currentBook, ReturnDate = returnDate)
                currentLogisticEntry.save()
                context['success'] = "Record Successfully Added"
            else:
                print("book already added")
                context['error'] = "This book record already exist for this student."
        elif 'delete' in request.POST:
            data = request.POST['trigger']
            currentItem =LogisticsData.objects.get(pk=data)
            currentItem.delete()
            context['success'] = "Record Successfully Deleted"

        elif 'delete_book' in request.POST:
            data = request.POST['trigger']
            currentItem = Book.objects.get(pk=data)
            currentItem.delete()
            context['success'] ="Record Successfully Deleted"

    # reports data
    reports = LogisticsData.objects.all()
    context['reports'] = reports

    # book data
    bookData = Book.objects.all()
    context['books'] = bookData

    # user data
    allUsers = User.objects.all()
    print(allUsers)
    context['users'] = allUsers
    

    return render(request, templatePath, context)