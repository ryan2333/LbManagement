from django.conf.urls import url
from management import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^add_book/$', views.add_book, name='add_book'),
    url(r'^add_computer/$', views.add_computer, name='add_computer'),
    url(r'^add_server/$', views.add_server, name='add_server'),
    url(r'^add_img/$', views.add_img, name='add_img'),
    url(r'^view_book_list/$', views.view_book_list, name='view_book_list'),
    url(r'^view_computer_list/$', views.view_computer_list, name='view_computer_list'),
    url(r'^view_server_list/$', views.view_server_list, name='view_server_list'),
    #url(r'^view_book/detail/$', views.detail, name='detail'),
    url(r'^cpudetail/', views.cpudetail, name='detail'),
    url(r'^serverdetail/', views.serverdetail, name='serverdetail'),
    url(r'^modify_computer/', views.modify_computer, name='modify_computer'),
    url(r'^modify_server/', views.modify_server, name='modify_server'),
    url(r'^up_computer/', views.up_computer, name='up_computer'),
    url(r'^up_server/', views.up_server, name='up_server'),
    url(r'^delete_computer/', views.del_computer, name='del_computer'),
    url(r'^delete_server/', views.del_server, name='del_server'),
]
