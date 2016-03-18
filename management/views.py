from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import MyUser, Book, Img, UserType,aUser,Computer,Server,SparePart,IdcInfo
from django.core.urlresolvers import reverse
from management.utils import permission_check
from datetime import datetime

def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)


@user_passes_test(permission_check)
def add_book(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Book(
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                category=request.POST.get('category', ''),
                price=request.POST.get('price', 0),
                publish_date=request.POST.get('publish_date', '')
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_book',
        'state': state,
    }
    return render(request, 'management/add_book.html', content)


def view_book_list(request):
    user = request.user if request.user.is_authenticated() else None
    category_list = Book.objects.values_list('category', flat=True).distinct()
    query_category = request.GET.get('category', 'all')
    if (not query_category) or Book.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        book_list = Book.objects.all()
    else:
        book_list = Book.objects.filter(category=query_category)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        book_list = Book.objects.filter(name__contains=keyword)
        query_category = 'all'

    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_book',
        'category_list': category_list,
        'query_category': query_category,
        'book_list': book_list,
    }
    
    return render(request, 'management/view_book_list.html', content)


def cpudetail(request):
    user = request.user if request.user.is_authenticated() else None
    computer_id = request.GET.get('Did', '')
    if computer_id == '':
        return HttpResponseRedirect(reverse('view_computer_list'))
    try:
        computer = Computer.objects.get(Did=computer_id)
    except computer.DoesNotExist:
        return HttpResponseRedirect(reverse('view_computer_list'))
    content = {
        'user': user,
        'active_menu': 'view_book',
        'computer': computer,
    }

    return render(request,'management/detail.html',content)


@user_passes_test(permission_check)
def add_img(request):
    user = request.user
    state = None
    if request.method == 'POST':
        try:
            new_img = Img(
                    name=request.POST.get('name', ''),
                    description=request.POST.get('description', ''),
                    img=request.FILES.get('img', ''),
                    book=Book.objects.get(pk=request.POST.get('book', ''))
            )
            new_img.save()
        except Book.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'state': state,
        'book_list': Book.objects.all(),
        'active_menu': 'add_img',
    }
    return render(request, 'management/add_img.html', content)

def add_computer(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_computer = Computer(
                Did=request.POST.get('Did', ''),
                Dname=request.POST.get('Dname', ''),
                Dstatus=request.POST.get('Dstatus', ''),
                Dbrand=request.POST.get('Dbrand', ''),
                Duser=request.POST.get('Duser', ''),
                Dposition=request.POST.get('Dposition', ''),
                Dmac=request.POST.get('Dmac', ''),
                Dallot=request.POST.get('Dallot', '1970-01-01'),
                Dbuy_time=request.POST.get('Dbuy_time', '1970-01-01'),
                Dprice=request.POST.get('Dprice', 1000),
                Dexpire=request.POST.get('Dexpire', '1970-01-01'),
                Ddetail=request.POST.get('Ddetail', ''),
                Dservices=request.POST.get('Dservices',''),
        )
        print request.POST.get('Dallot')
        new_computer.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_computer',
        'state': state,
    }
    return render(request, 'management/add_computer.html',content)

def view_computer_list(request):
    user = request.user if request.user.is_authenticated() else None
    Did_list = Computer.objects.values_list('Did', flat=True).distinct()
    query_Did = request.GET.get('Did', 'all')
    if (not query_Did) or Computer.objects.filter(Did=query_Did).count() is 0:
        query_Did = 'all'
        computer_list = Computer.objects.all()
    else:
        computer_list = Computer.objects.filter(category=query_category)
#    computer_list = Computer.objects.all().values()
    if request.method == 'POST':
         keyword = request.POST.get('keyword', '')
         computer_list = Computer.objects.filter(Did__contains=keyword)
         query_Did = 'all'
    paginator = Paginator(computer_list, 20)
    page = request.GET.get('page')
    try:
        computer_list = paginator.page(page)
    except PageNotAnInteger:
        computer_list = paginator.page(1)
    except EmptyPage:
        computer_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_computer',
        'category_list': Did_list,
        'query_category': query_Did,
        'computer_list': computer_list,
    }
#     return render_to_response('management/view_computer_list.html', {'computer_list':computer_list})
    return render(request, 'management/view_computer_list.html', content)

def modify_computer(request):
    user = request.user if request.user.is_authenticated() else None
    computer_id = request.GET.get('Did', '')
    if computer_id == '':
        return HttpResponseRedirect(reverse('view_computer_list'))
    try:
        computer = Computer.objects.get(Did=computer_id)
    except computer.DoesNotExist:
        return HttpResponseRedirect(reverse('view_computer_list'))
    computer.Dallot= computer.Dallot.strftime('%Y-%m-%d')
    computer.Dbuy_time= computer.Dbuy_time.strftime('%Y-%m-%d')
    computer.Dexpire= computer.Dexpire.strftime('%Y-%m-%d')
    content = {
        'user': user,
        'active_menu': 'view_book',
        'computer': computer,
    }

    return render(request,'management/modify_computer.html',content)

def up_computer(request):
    user = request.user if request.user.is_authenticated() else None
    computer_id = request.POST.get('Did', '')
    if computer_id == '':
        return HttpResponseRedirect(reverse('view_computer_list'))
    try:
        computer = Computer.objects.get(Did=computer_id)
    except computer.DoesNotExist:
        return HttpResponseRedirect(reverse('view_computer_list'))
    
    p = Computer.objects.get(Did=computer_id)
    p.Dname = request.POST.get('Dname')
    p.Dstatus = request.POST.get('Dstatus')
    p.Dbrand = request.POST.get('Dbrand')
    p.Duser = request.POST.get('Duser')
    p.Dposition = request.POST.get('Dposition')
    p.Dmac = request.POST.get('Dmac')
    p.Dallot = request.POST.get('Dallot')
    p.Dbuy_time = request.POST.get('Dbuy_time')
    p.Dprice = request.POST.get('Dprice')
    p.Dexpire = request.POST.get('Dexpire')
    p.Ddetail = request.POST.get('Ddetail')
    p.Dservices = request.POST.get('Dservices')
    p.save()
    computer = Computer.objects.get(Did=computer_id)
    content = {
        'user': user,
        'active_menu': 'detail',
        'computer': computer,
    }

    return render(request,'management/detail.html',content)

def del_computer(request):
    user = request.user if request.user.is_authenticated() else None
    computer_id = request.GET.get('Did', '')
    if computer_id == '':
        return HttpResponseRedirect(reverse('view_computer_list'))    
    Computer.objects.get(Did=computer_id).delete()
    return HttpResponseRedirect(reverse('view_computer_list'))

def add_server(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_server = Server(
                Sid=request.POST.get('Sid'),
                Sname=request.POST.get('Sname'),
                Sstatus=request.POST.get('Sstatus'),
                Sbrand=request.POST.get('Sbrand'),
                Escode=request.POST.get('Escode'),
                Sposition=request.POST.get('Sposition'),
                Sip2=request.POST.get('Sip2'),
                Sip1=request.POST.get('Sip1'),
                Sbuy_time=request.POST.get('Sbuy_time'),
                Sprice=request.POST.get('Sprice'),
                Sexpire=request.POST.get('Sexpire'),
                Sidc=request.POST.get('Sidc'),
                Spod=request.POST.get('Spod'),
                Sues=request.POST.get('Su'),
                Sdetail=request.POST.get('Sdetail'),
                Sservices=request.POST.get('Sservices'),
        )
        new_server.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_computer',
        'state': state,
    }
    return render(request, 'management/add_server.html',content)

def view_server_list(request):
    user = request.user if request.user.is_authenticated() else None
    Sid_list = Server.objects.values_list('Sid', flat=True).distinct()
    query_Sid = request.GET.get('Sid', 'all')
    if (not query_Sid) or Server.objects.filter(Sid=query_Sid).count() is 0:
        query_Sid = 'all'
        server_list = Server.objects.all()
    else:
        server_list = Server.objects.filter(category=query_category)
#    computer_list = Computer.objects.all().values()
    if request.method == 'POST':
         keyword = request.POST.get('keyword', '')
         server_list = Server.objects.filter(Sid__contains=keyword)
         query_Sid = 'all'
    paginator = Paginator(server_list, 20)
    page = request.GET.get('page')
    try:
        server_list = paginator.page(page)
    except PageNotAnInteger:
        server_list = paginator.page(1)
    except EmptyPage:
        server_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_server',
        'category_list': Sid_list,
        'query_category': query_Sid,
        'server_list': server_list,
    }
#     return render_to_response('management/view_computer_list.html', {'computer_list':computer_list})
    return render(request, 'management/view_server_list.html', content)

def serverdetail(request):
    user = request.user if request.user.is_authenticated() else None
    server_id = request.GET.get('Sid', '')
    if server_id == '':
        return HttpResponseRedirect(reverse('view_server_list'))
    try:
        server = Server.objects.get(Sid=server_id)
    except server.DoesNotExist:
        return HttpResponseRedirect(reverse('view_server_list'))
    content = {
        'user': user,
        'active_menu': 'view_book',
        'server': server,
    }
    print server.Sdetail

    return render(request,'management/serverdetail.html',content)

def modify_server(request):
    user = request.user if request.user.is_authenticated() else None
    server_id = request.GET.get('Sid', '')
    if server_id == '':
        return HttpResponseRedirect(reverse('view_server_list'))
    try:
        server = Server.objects.get(Sid=server_id)
    except server.DoesNotExist:
        return HttpResponseRedirect(reverse('view_server_list'))
    
    server.Sbuy_time= server.Sbuy_time.strftime('%Y-%m-%d')
    server.Sexpire= server.Sexpire.strftime('%Y-%m-%d')
    content = {
        'user': user,
        'active_menu': 'view_book',
        'server': server,
    }

    return render(request,'management/modify_server.html',content)

def up_server(request):
    user = request.user if request.user.is_authenticated() else None
    server_id = request.POST.get('Sid', '')
    if server_id == '':
        return HttpResponseRedirect(reverse('view_server_list'))
    try:
        server = Server.objects.get(Sid=server_id)
    except server.DoesNotExist:
        return HttpResponseRedirect(reverse('view_server_list'))
    
    p = Server.objects.get(Sid=server_id)
    p.Sname = request.POST.get('Sname')
    p.Sstatus = request.POST.get('Sstatus')
    p.Sbrand = request.POST.get('Sbrand')
    p.Sip1 = request.POST.get('Sip1')
    p.Sidc = request.POST.get('Sidc')
    p.Spod = request.POST.get('Spod')
    p.Sues = request.POST.get('Su')
    p.Sip2 = request.POST.get('Sip2')
    p.Sposition = request.POST.get('Sposition')
    p.Escode = request.POST.get('Escode')
    p.Sbuy_time = request.POST.get('Sbuy_time')
    p.Sprice = request.POST.get('Sprice')
    p.Sexpire = request.POST.get('Sexpire')
    p.Sdetail = request.POST.get('Sdetail')
    p.Sservices = request.POST.get('Sservices')
    p.save()
    server = Server.objects.get(Sid=server_id)
    content = {
        'user': user,
        'active_menu': 'serverdetail',
        'server': server,
    }
    return render(request,'management/serverdetail.html',content)

def del_server(request):
    user = request.user if request.user.is_authenticated() else None
    server_id = request.GET.get('Sid', '')
    if server_id == '':
        return HttpResponseRedirect(reverse('view_server_list'))    
    Server.objects.get(Sid=server_id).delete()
    return HttpResponseRedirect(reverse('view_server_list'))

def add_spart(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_sparepart = SparePart(
                Sid=request.POST.get('Sid', ''),
                Sname=request.POST.get('Sname', ''),
                Sbrand=request.POST.get('Sbrand', ''),
                Sdetail=request.POST.get('Sdetail', ''),
                Sbuy_time=request.POST.get('Sbuy_time', ''),
                Sprice=request.POST.get('Sprice', ''),
                Sexpire=request.POST.get('Sexpire', ''),
        )
        new_sparepart.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_spart',
        'state': state,
    }
    return render(request, 'management/add_sparepart.html', content) 

def up_spart(request):
    user = request.user if request.user.is_authenticated() else None
    spart_id = request.POST.get('Sid', '')
    if spart_id == '':
        return HttpResponseRedirect(reverse('view_sparepart_list'))
    try:
        spart = SparePart.objects.get(Sid=spart_id)
    except spart.DoesNotExist:
        return HttpResponseRedirect(reverse('view_sparepart_list'))
    
    p = SparePart.objects.get(Sid=spart_id)
    p.Sname = request.POST.get('Sname')
    p.Sbrand = request.POST.get('Sbrand')
    p.Sbuy_time = request.POST.get('Sbuy_time')
    p.Sprice = request.POST.get('Sprice')
    p.Sexpire = request.POST.get('Sexpire')
    p.Sdetail = request.POST.get('Sdetail')
    p.save()
    spart = SparePart.objects.get(Sid=server_id)
    content = {
        'user': user,
        'active_menu': 'sparepartdetail',
        'server': spart,
    }
    return render(request,'management/sparepartdetail.html',content)

def del_spart(request):
    user = request.user if request.user.is_authenticated() else None
    spart_id = request.GET.get('Sid', '')
    if spart_id == '':
        return HttpResponseRedirect(reverse('view_spart_list'))    
    SparePart.objects.get(Sid=spart_id).delete()
    return HttpResponseRedirect(reverse('view_spart_list'))

def view_spart_list(request):
    user = request.user if request.user.is_authenticated() else None
    Sid_list = SparePart.objects.values_list('Sid', flat=True).distinct()
    query_Sid = request.GET.get('Sid', 'all')
    if (not query_Sid) or SparePart.objects.filter(Sid=query_Sid).count() is 0:
        query_Sid = 'all'
        spart_list = SparePart.objects.all()
    else:
        spart_list = SparePart.objects.filter(category=query_category)
#    computer_list = Computer.objects.all().values()
    if request.method == 'POST':
         keyword = request.POST.get('keyword', '')
         spart_list = SparePart.objects.filter(Sid__contains=keyword)
         query_Sid = 'all'
    paginator = Paginator(spart_list, 20)
    page = request.GET.get('page')
    try:
        spart_list = paginator.page(page)
    except PageNotAnInteger:
        spart_list = paginator.page(1)
    except EmptyPage:
        spart_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_sparepart',
        'category_list': Sid_list,
        'query_category': query_Sid,
        'spart_list': spart_list,
    }
#     return render_to_response('management/view_computer_list.html', {'computer_list':computer_list})
    return render(request, 'management/view_sparepart_list.html', content)

def modify_spart(request):
    user = request.user if request.user.is_authenticated() else None
    spart_id = request.GET.get('Sid', '')
    if spart_id == '':
        return HttpResponseRedirect(reverse('view_sparepart_list'))
    try:
        spart = SparePart.objects.get(Sid=spart_id)
    except server.DoesNotExist:
        return HttpResponseRedirect(reverse('view_sparepart_list'))
    print spart.Sid
    spart.Sbuy_time= spart.Sbuy_time.strftime('%Y-%m-%d')
    spart.Sexpire= spart.Sexpire.strftime('%Y-%m-%d')
    content = {
        'user': user,
        'active_menu': 'view_book',
        'spart': spart,
    }

    return render(request,'management/modify_sparepart.html',content)

def spartdetail(request):
    user = request.user if request.user.is_authenticated() else None
    spart_id = request.GET.get('Sid', '')
    if spart_id == '':
        return HttpResponseRedirect(reverse('view_sparepart_list'))
    try:
        spart = SparePart.objects.get(Sid=spart_id)
    except spare.DoesNotExist:
        return HttpResponseRedirect(reverse('view_sparepart_list'))
    content = {
        'user': user,
        'active_menu': 'view_spart',
        'server': spart,
    }

    return render(request,'management/sparepartdetail.html',content)
