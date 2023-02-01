from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control, never_cache

from LibraryApp.models import Student, Course, Book, Issue_Book


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def log_fun(request):
    return render(request,'login.html',{'data':''})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def readlog_fun(request):
    user_name=request.POST['txtname']
    user_password=request.POST['txtpwd']
    user = authenticate(username=user_name,password=user_password)
    if user is not None:
        if user.is_superuser:
            suser = authenticate(username=user_name, password=user_password)
            login(request, suser)
            return render(request,'AdminHome.html')
        else:
            user = authenticate(username=user_name, password=user_password)
            request.session['name'] = user_name
            login(request, user)
            return render(request, 'StudentHome.html', {'data': user_name})

    # elif Student.objects.filter(Q(Student_Name=user_name) & Q(Student_Password=user_password)).exists():
    #     request.session['name']=user_name
    #     login(request, user_name)
    #     return render(request,'StudentHome.html',{'data':user_name})
    else:
            return render(request, 'login.html', {'data': 'Invalid Username or Password '})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def studentReg_fun(request):
    c = Course.objects.all()
    return render(request,'StudentReg.html',{'data':'','course':c})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def adminReg_fun(request):
    return render(request,'AdminReg.html',{'data':""})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def readstdreg_fun(request):
    user = Student.objects.filter(Q(Student_Name=request.POST['txtname']) & Q(Student_Password=request.POST['txtpwd'])).exists()
    if user:
        c = Course.objects.all()
        return render(request,'StudentReg.html',{'data':'UserName And Password Already Exist','course':c})
    else:
        s = Student()
        s.Student_Name=request.POST['txtname']
        s.Student_PhoneNo=request.POST['txtmobile']
        s.Student_Sem=request.POST['txtsem']
        s.Student_Password=request.POST['txtpwd']
        s.Course=Course.objects.get(Course_Name=request.POST['ddlcourse'])
        s.save()
        user = User.objects.create_user(username=request.POST['txtname'],password=request.POST['txtpwd'])
        user.save()
        login(request, user)
        return redirect('log')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def readadminreg_fun(request):
    u = authenticate(username=request.POST['txtname'], password=request.POST['txtpwd'])
    if u is not None:
        if u.is_superuser:
            return render(request, 'AdminReg.html',{'data':'Username and Password Already Exist'})
        else:
            u = User.objects.create_superuser(username=request.POST['txtname'], password=request.POST['txtpwd'])
            u.save()
            return redirect('log')
    else:
        u = User.objects.create_superuser(username=request.POST['txtname'], password=request.POST['txtpwd'])
        u.save()
        return redirect('log')

@login_required()
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def addbook_fun(request):
    c = Course.objects.all()
    return render(request,'AddBook.html',{'courses':c,'msg':''})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def readaddbook_fun(request):
    b = Book()
    b.Book_Name = request.POST['txtname']
    b.Author_Name = request.POST['txtAname']
    b.Course = Course.objects.get(Course_Name=request.POST['ddlcourse'])
    b.save()
    c = Course.objects.all()
    return render(request,'AddBook.html',{'courses':c,'msg':'One Book Added Successfully'})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def displaybooks_fun(request):
    b = Book.objects.all()


    return render(request,'Display.html',{'books':b})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def update_fun(request,bid):
    b = Book.objects.get(id=bid)
    c = Course.objects.all()
    if request.method=='POST':
        b.Book_Name = request.POST['txtname']
        b.Author_Name = request.POST['txtAname']
        b.Course = Course.objects.get(Course_Name=request.POST['ddlcourse'])
        b.save()
        c = Course.objects.all()
        return render(request, 'UpdateBook.html', {'book': b, 'courses': c, 'msg': 'One Book Updated'})

    return render(request,'UpdateBook.html',{'book':b,'courses':c, 'msg':''})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def delete_fun(request,bid):
    b = Book.objects.get(id=bid)
    b.delete()
    return redirect('dis')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def assignbook(request):
    c = Course.objects.all()
    return render(request,'AssignBook.html',{'Courses':c})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def readsemcourse(request):
    stdsem = request.POST['txtsem']
    course = request.POST['ddlcourse']
    students = Student.objects.filter(Q(Student_Sem=stdsem) & Q(Course=Course.objects.get(Course_Name=course)))
    print(students)
    books = Book.objects.filter(Course=Course.objects.get(Course_Name=course))
    print(books)
    return render(request,'AssignBook.html',{'students':students,'books':books})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def readstdbook(request):
    ib = Issue_Book()
    ib.Student_Name = Student.objects.get(Student_Name=request.POST['ddlstdname'])
    ib.Book_Name = Book.objects.get(Book_Name=request.POST['ddlbookname'])
    ib.Start_Date = request.POST['startdate']
    ib.End_Date = request.POST['enddate']
    ib.save()
    c = Course.objects.all()
    return render(request,'AssignBook.html',{'Courses':c,'msg':'Book Assigned Successfully'})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def disIssuedBk(request):
    Ibooks = Issue_Book.objects.all()
    return render(request,'DisplayIssuedBooks.html',{'Ibooks':Ibooks})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def updateIbook(request,id):
    ib=Issue_Book.objects.get(id=id)
    bk = Book.objects.all()
    # s = Student.objects.get(id=ib.Student_Name_id)
    # c = Course.objects.get(Q(Course_Name=s.Course) &
    if request.method == 'POST':
        ib.Student_Name = Student.objects.get(Student_Name=request.POST['txtstdname'])
        ib.Book_Name= Book.objects.get(Book_Name=request.POST['ddlbkname'])
        ib.Start_Date= request.POST['startdate']
        ib.End_Date= request.POST['enddate']
        ib.save()
        return redirect('IssuedBooks')

    return render(request,'UpdateIssuedBook.html',{'ib':ib,'books':bk})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def delIbook(request,id):
    ib = Issue_Book.objects.get(id=id)
    ib.delete()
    return redirect('IssuedBooks')
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def stdbooks(request):
    ib = Issue_Book.objects.filter(Student_Name=Student.objects.get(Student_Name=request.session['name']))
    print(ib)
    return render(request, 'StdIssuedBooks.html', {'books': ib})
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def stdhome(request):
    return render(request,'StudentHome.html',{'data':request.session['name']})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def stdprofile(request):
    print(request.session['name'])
    s = Student.objects.get(Student_Name=request.session['name'])
    print(s)
    return render(request,'stdprofile.html',{'s':s})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def stdedit(request):
    s = Student.objects.get(Student_Name=request.session['name'])
    if request.method=='POST':
        s.Student_Name = request.POST['txtname']
        s.Student_PhoneNo = request.POST['txtmobile']
        s.Student_Password = request.POST['txtpwd']
        s.save()
        user = User.objects.get(username=request.session['name'])
        user.delete()
        user = User.objects.create_user(username=request.POST['txtname'],password=request.POST['txtpwd'])
        user.save()
        login(request, user)
        request.session['name'] = request.POST['txtname']
        return redirect('stdprofile')
    return render(request,'stdedit.html',{'std': s})

def adminlogout(request):
    logout(request)
    return redirect('log')


def stdlogout(request):
    logout(request)
    return redirect('log')
