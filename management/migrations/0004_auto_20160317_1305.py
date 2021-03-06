# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-17 05:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20160317_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='aUser',
            fields=[
                ('uid', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('lname', models.CharField(max_length=15, unique=True, verbose_name='\u7528\u6237\u540d')),
                ('password', models.CharField(max_length=18)),
                ('name', models.CharField(max_length=8, verbose_name='\u59d3\u540d')),
                ('email', models.EmailField(blank=True, max_length=30, null=True, verbose_name='Email')),
                ('position', models.CharField(max_length=10, verbose_name='\u804c\u4f4d')),
                ('dept', models.CharField(max_length=10, verbose_name='\u90e8\u95e8')),
            ],
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Did', models.CharField(max_length=15, unique=True, verbose_name='\u8d44\u4ea7\u7f16\u53f7')),
                ('Dname', models.CharField(max_length=10)),
                ('Dbrand', models.CharField(max_length=10)),
                ('Ddetail', models.TextField()),
                ('Duser', models.CharField(max_length=10)),
                ('Dallot', models.DateField()),
                ('Dposition', models.CharField(max_length=10)),
                ('Dmac', models.CharField(max_length=20, unique=True)),
                ('Dstatus', models.CharField(max_length=4)),
                ('Dbuy_time', models.DateField(blank=True, null=True)),
                ('Dprice', models.IntegerField(blank=True, null=True)),
                ('Dexpire', models.DateField()),
                ('Dservices', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='IdcInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Iname', models.CharField(max_length=20)),
                ('Icontact', models.CharField(max_length=30)),
                ('Iaddress', models.TextField(blank=True, null=True)),
                ('Itel', models.CharField(max_length=30)),
                ('Ipods', models.CharField(blank=True, max_length=20, null=True)),
                ('Ibw', models.CharField(blank=True, max_length=8, null=True)),
                ('Iservices', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sid', models.CharField(max_length=20, unique=True, verbose_name='\u8d44\u4ea7SN\u53f7')),
                ('Sname', models.CharField(max_length=10)),
                ('Sbrand', models.CharField(max_length=10)),
                ('Escode', models.CharField(default='xxxxxxxx', max_length=20)),
                ('Sdetail', models.TextField()),
                ('Sposition', models.CharField(max_length=10)),
                ('Sip1', models.CharField(max_length=20, unique=True)),
                ('Sip2', models.CharField(blank=True, max_length=20, null=True)),
                ('Sstatus', models.CharField(max_length=4)),
                ('Sbuy_time', models.DateField(blank=True, null=True)),
                ('Sprice', models.IntegerField(blank=True, null=True)),
                ('Sexpire', models.DateField()),
                ('Sidc', models.CharField(blank=True, max_length=10, null=True)),
                ('Spod', models.CharField(blank=True, max_length=15, null=True)),
                ('Sues', models.CharField(blank=True, max_length=15, null=True)),
                ('Sservices', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SparePart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sid', models.CharField(max_length=10, unique=True)),
                ('Sname', models.CharField(max_length=10)),
                ('Sbrand', models.CharField(max_length=20)),
                ('Sdetail', models.TextField()),
                ('Sbuy_time', models.DateField(blank=True, null=True)),
                ('Sprice', models.IntegerField(blank=True, null=True)),
                ('Sexpire', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('super', '\u8d85\u7ea7\u7528\u6237'), ('admin', '\u7ba1\u7406\u5458'), ('user', '\u666e\u901a\u7528\u6237')], default='user', max_length=10)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u7c7b\u578b',
                'verbose_name_plural': '\u7528\u6237\u7c7b\u578b',
            },
        ),
        migrations.AddField(
            model_name='auser',
            name='user_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='management.UserType'),
        ),
    ]
