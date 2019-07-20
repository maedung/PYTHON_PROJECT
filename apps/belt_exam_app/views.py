from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import re
import bcrypt

############# REGEX ############

NAME_REGEX = re.compile(r'^[a-zA-z]')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,15})')

############# Main Page ########

def index(request):
    if "user" in request.session:
        del request.session['user']
    return render(request, "belt_exam_app/index.html")


######## Register Validation #######

def register(request):
    if request.method == 'POST':
        if request.POST["register"] == "register":
            is_valid = True
            if len(request.POST['fname']) < 2 or not NAME_REGEX.match(request.POST['fname']):
                messages.error(request, "First Name must contain at least two letters and contain only letters")
                is_valid = False
            if len(request.POST['lname']) < 2 or not NAME_REGEX.match(request.POST['lname']):
                messages.error(request, "Last Name must contain at least two letters and contain only letters")
                is_valid = False
            if not EMAIL_REGEX.match(request.POST['email']):
                messages.error(request, "Invalid email address")
                is_valid = False
            if User.objects.filter(email=request.POST['email']).exists()==True:
                messages.error(request, "Email address is already Taken")
                is_valid = False
            if not PASSWORD_REGEX.match(request.POST['pw']):
                messages.error(request, "Password must contain a number, a capital letter, and at least 8-15 characters")
                is_valid = False
            if request.POST['pw'] != request.POST['pwc']:
                messages.error(request, "Passwords need to match")
                is_valid = False

            if is_valid:
                new_fname = request.POST['fname']
                new_lname = request.POST['lname']
                new_email = request.POST['email']
                new_pw = request.POST['pw']
                hash1 = bcrypt.hashpw(new_pw.encode(), bcrypt.gensalt())
                new_user = User.objects.create(first_name = new_fname, last_name = new_lname, email = new_email, password = hash1.decode())
                messages.success(request, "Successfully created your account!")
                
                return redirect('/')

            else:
                return redirect('/')

######### Login Validation ###########

def login(request):
    if request.method == 'POST':
        if request.POST['login'] == 'login':
            if User.objects.filter(email=request.POST['login_email']).exists()==False:
                messages.error(request, "Email doesn't exist")
                return redirect('/')
            else:
                user = User.objects.get(email = request.POST['login_email'])
                if bcrypt.checkpw(request.POST['login_pw'].encode(), user.password.encode()) == False:
                    messages.error(request, "Wrong Password")
                    return redirect('/')
                else:
                    request.session['user'] = user.id
                    return redirect('/dashboard')
####### DashBoard Page ##############
def dashboard(request):
    if not 'user' in request.session:
        messages.error(request, "Log In First")
        return redirect('/') 
    else:
        this_user = User.objects.get(id = request.session['user'])
        context = {
            "user": this_user,
            "jobs": Job.objects.all(),
        }
        return render(request, "belt_exam_app/dashboard.html", context)

########## New Job Page ################
def new_job(request):
    if not 'user' in request.session:
        messages.error(request, "Log In First")
        return redirect('/') 
    else:
        this_user = User.objects.get(id = request.session['user'])
        all_categories = Category.objects.all()
        context = {
            'user': this_user,
            'categories': all_categories,
        }

        return render(request,'belt_exam_app/new_job.html',context)


########## Create Processing / Validate ############
def create_job(request):
    if request.method == 'POST':
        is_valid = True
        if len(request.POST['new_title']) < 3:
            messages.error(request, "job title should be at least 3 characters!")
            is_valid = False
        if len(request.POST['new_desc']) < 3:
            messages.error(request, "job desc should be at least 3 characters!")
            is_valid = False
        if len(request.POST['new_location']) < 3:
            messages.error(request, "A location must consist of at least 3 characters!")
            is_valid = False
        if Job.objects.filter(title=request.POST['new_title']).exists()==True:
            messages.error(request, "This Job Name is already exist!")
            is_valid = False

        if not is_valid:
            return redirect('/jobs/new')
        else:
            new_title = request.POST['new_title']
            new_desc = request.POST['new_desc']
            new_location = request.POST['new_location']
            new_job = Job.objects.create(title = new_title, desc = new_desc, location = new_location)

            if len(request.POST['other']) > 0:
                if Category.objects.create(title = request.POST['other']).exists() == True:
                    new_category = Category.objects.get(title = request.POST['other'])
                    new_job.categories.add(new_category)
                else:
                    new_category = Category.objects.create(title = request.POST['other'])
                    new_job.categories.add(new_category)
                    
            # cat = Category.objects.last()
            # for i in range(cat.id):        
            #     if checkbox (i) is checked:
            #         new_category = Category.objects.get(id = i)
            #         new_job.categories.add(new_category)



            return redirect('/dashboard')

def job_delete(request, id):
    this_job = Job.objects.get(id = id)
    this_job.delete()
    return redirect('/dashboard')

def job_info(request, id):
    if not 'user' in request.session:
        messages.error(request, "Log In First")
        return redirect('/') 
    else:
        job_info = Job.objects.get(id = id)
        user = User.objects.get(id = request.session['user'])
        this_job = job_info.categories.all().values()
        context = {
            'job': job_info,
            'user': user,
            "this_job": this_job
        }
        return render(request, 'belt_exam_app/job_info.html', context)

def edit_job(request, id):
    if not 'user' in request.session:
        messages.error(request, "Log In First")
        return redirect('/') 
    else:
        job_info = Job.objects.get(id = id)
        request.session['job'] = id
        user = User.objects.get(id = request.session['user'])
        context = {
            'job': job_info,
            'user': user,
        }
        return render(request, 'belt_exam_app/edit.html', context)

def edit_process(request):
    if request.method == 'POST':
        is_valid = True
        this_job = request.session['job']
        if len(request.POST['edit_title']) < 3:
            messages.error(request, "job title should be at least 3 characters!")
            is_valid = False
        if len(request.POST['edit_desc']) < 3:
            messages.error(request, "job desc should be at least 3 characters!")
            is_valid = False
        if len(request.POST['edit_location']) < 3:
            messages.error(request, "A location must consist of at least 3 characters!")
            is_valid = False
        if Job.objects.filter(title = request.POST['edit_title']).exists() == True:
            messages.error(request, "This Job Name is already exist!")
            
        if not is_valid:    
            return redirect(f'/edit/{this_job}')

        else:
            this_job = request.session['job']
            edit_title = request.POST['edit_title']
            edit_desc = request.POST['edit_desc']
            edit_location = request.POST['edit_location']
            this_job = Job.objects.get(id = request.session['job'])
            this_job.title = edit_title
            this_job.desc = edit_desc
            this_job.location = edit_location
            this_job.save()
            return redirect('/dashboard')