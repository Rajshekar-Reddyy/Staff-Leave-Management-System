from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from accounts.models import profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
#to connect html page in django 
def home(request):
    return render(request,'home.html')

## 2. for register.html connection we write this
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        role=request.POST['role']
        user=User.objects.create_user(username=username,password=password) #
        profile.objects.create(user=user,role=role)
        return redirect('login')
    return render(request,'register.html')

## 3. for login.html page connection we write this
def login_view(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            if user.profile.role=='admin':
                return redirect('admin_dashboard')
            else:
                return redirect('staff_dashboard')
    return render(request,'login.html')

@login_required
def admin_dashboard(request):
    if request.user.profile.role!='admin':
        return redirect('staff_dashboard')
    return render(request,'admin_dashboard.html')

# for staff_dashboard
@login_required
def staff_dashboard(request):
    return render(request,'staff_dashboard.html')

#for logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

#manage staff
@login_required
def manage_staff(request):
    if request.user.profile.role !='admin':
        return redirect('staff_dashboard')
    staff_list=User.objects.filter(profile__role='staff')
    return render(request,'manage_staff.html',{'staff_list':staff_list})

# to add staff
@login_required
def add_staff(request):
 if request.user.profile.role != 'admin':
     return redirect('staff_dashboard')
 if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=User.objects.create_user(username=username,password=password) #
        profile.objects.create(user=user,role='staff')
        return redirect('manage_staff')
 return render(request,'add_staff.html')

@login_required
def edit_staff(request,id):
    if request.user.profile.role !='admin':
        return redirect('staff_dashboard')
    user=get_object_or_404(User,id=id)
    if request.method=='POST':
        user.username=request.POST['username']
        user.save()
        return redirect('manage_staff')
    return render(request,'edit_staff.html',{'user':user})

@login_required
def delete_staff(request,id):
    if request.user.profile.role !='admin':
        return redirect('staff_dashboard')
    user=get_object_or_404(User,id=id)
    user.delete()
    return redirect('manage_staff')