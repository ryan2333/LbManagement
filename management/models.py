#!/usr/bin/env python
#_*_coding:utf-8_*_

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username


class Book(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    author = models.CharField(max_length=128)
    publish_date = models.DateField()
    category = models.CharField(max_length=128)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Img(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    img = models.ImageField(upload_to='image/%Y/%m/%d/')
    book = models.ForeignKey(Book)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class UserType(models.Model):
    user_type_choices = (
        ('super', u'超级用户'),
        ('admin', u'管理员'),
        ('user', u'普通用户'),
    )
    user_type = models.CharField(choices=user_type_choices, max_length=10, default='user')
    class Meta:
        verbose_name = '用户类型'
        verbose_name_plural = "用户类型"
    def __unicode__(self):
        return self.user_type
class aUser(models.Model):
    uid = models.IntegerField(primary_key=True,unique=True)
    lname = models.CharField(u'用户名',max_length=15, unique=True)
    password = models.CharField(max_length=18)
    name = models.CharField(u'姓名', max_length=8)
    email = models.EmailField(u'Email', max_length=30,null=True,blank=True)
    position = models.CharField(u'职位', max_length=10)
    dept = models.CharField(u'部门',max_length=10)
    user_type = models.OneToOneField(UserType)
    def __unicode__(self):
        return self.name
class Computer(models.Model):   
    Did = models.CharField(u'资产编号',max_length=15,unique=True)
    Dname = models.CharField(max_length=10)
    Dbrand = models.CharField(max_length=10)
    Ddetail = models.TextField()
    Duser = models.CharField(max_length=10)
    Dallot = models.DateField()
    Dposition = models.CharField(max_length=10)
    Dmac = models.CharField(max_length=20,unique=True)    
    Dstatus = models.CharField(max_length=4)
    Dbuy_time = models.DateField(null=True, blank=True)
    Dprice = models.IntegerField(null=True, blank=True)
    Dexpire = models.DateField()
    Dservices = models.TextField()
    def __unicode__(self):
        return self.Did

class Server(models.Model):
    Sid = models.CharField(u'资产SN号',max_length=20, unique=True)
    Sname = models.CharField(max_length=30)
    Sbrand = models.CharField(max_length=10)
    Escode = models.CharField(max_length=20,default='xxxxxxxx')
    Sdetail = models.TextField()
    Sposition = models.CharField(max_length=10)
    Sip1 = models.CharField(max_length=20,unique=True)
    Sip2 = models.CharField(max_length=20,null=True, blank=True)
    Sstatus = models.CharField(max_length=4)
    Sbuy_time = models.DateField(null=True, blank=True)
    Sprice = models.IntegerField(null=True, blank=True)
    Sexpire = models.DateField()
    Sidc = models.CharField(max_length=10,null=True, blank=True)
    Spod = models.CharField(max_length=15,null=True, blank=True)
    Sues = models.CharField(max_length=15,null=True, blank=True)
    Sservices = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return self.Sname
    
class SparePart(models.Model):
    Sid = models.CharField(max_length=10,unique=True)
    Sname = models.CharField(max_length=10)
    Sbrand = models.CharField(max_length=20)
    Sdetail = models.TextField()
    Sbuy_time = models.DateField(null=True, blank=True)
    Sprice = models.IntegerField(null=True, blank=True)
    Sexpire = models.DateField(null=True,blank=True)
    def __unicode__(self):
        return self.Sname
class IdcInfo(models.Model):
    Iname = models.CharField(max_length=20)
    Icontact = models.CharField(max_length=30)
    Iaddress = models.TextField(null=True,blank=True)
    Itel = models.CharField(max_length=30)
    Ipods = models.CharField(max_length=20,null=True,blank=True)
    Ibw = models.CharField(max_length=8, null=True,blank=True)
    Iservices = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return self.Iname