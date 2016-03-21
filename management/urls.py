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
    url(r'^add_sparepart/$', views.add_spart, name='add_spart'),
    url(r'^add_idcinfo/$', views.add_idcinfo, name='add_idcinfo'),
    url(r'^add_img/$', views.add_img, name='add_img'),
    url(r'^add_user/$', views.signup, name='signup'),
    url(r'^view_book_list/$', views.view_book_list, name='view_book_list'),
    url(r'^view_computer_list/$', views.view_computer_list, name='view_computer_list'),
    url(r'^view_server_list/$', views.view_server_list, name='view_server_list'),
    url(r'^view_sparepart_list/$', views.view_spart_list, name='view_spart_list'),
    url(r'^view_idcinfo_list/$', views.view_idcinfo_list, name='view_idcinfo_list'),
    #url(r'^view_book/detail/$', views.detail, name='detail'),
    url(r'^cpudetail/', views.cpudetail, name='detail'),
    url(r'^serverdetail/', views.serverdetail, name='serverdetail'),
    url(r'^sparepartdetail/', views.spartdetail, name='spartdetail'),
    url(r'^modify_computer/', views.modify_computer, name='modify_computer'),
    url(r'^modify_server/', views.modify_server, name='modify_server'),
    url(r'^modify_sparepart/', views.modify_spart, name='modify_spart'),
    url(r'^up_idcinfo/', views.up_idcinfo, name='up_idcinfo'),
    url(r'^modify_idcinfo/', views.modify_idcinfo, name='modify_idcinfo'),
    url(r'^up_computer/', views.up_computer, name='up_computer'),
    url(r'^up_server/', views.up_server, name='up_server'),
    url(r'^up_spart/', views.up_spart, name='up_spart'),
    url(r'^delete_computer/', views.del_computer, name='del_computer'),
    url(r'^delete_server/', views.del_server, name='del_server'),
    url(r'^delete_sparepart/', views.del_spart, name='del_spart'),
    url(r'^delete_idcinfo/', views.del_idcinfo, name='del_idcinfo'),
]
