#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
# from booksys.views import collectLogin

# Create your models here.
# 图书标签
class BookTags(models.Model):
    name = models.CharField('标签名', max_length=100,unique=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

#图书信息模型
class BookInformation(models.Model):
    bookimg=models.ImageField('图片',upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200, null=True)
    bookname=models.CharField(max_length=200,verbose_name='图书名',null=True,blank=True,default=None)
    bookdescribe=models.TextField('简介',null=True,blank=True,default=None)
    bookpublisher=models.CharField(max_length=200,verbose_name='出版商',null=True,blank=True,default=None)
    bookauthor=models.CharField('作者',max_length=200,null=True,blank=True,default=None)
    bookpl=models.IntegerField('评价人数',null=True,blank=True,default=None)
    bookstar=models.DecimalField('评分',max_digits=4,decimal_places=2,null=True,blank=True,default=None)
    bookdate=models.DateField('日期',null=True,blank=True,default=None)
    bookprice=models.CharField('价格',max_length=20,null=True,blank=True,default=None)
    booktag=models.ManyToManyField(BookTags,verbose_name='标签',blank=True,default=None)
    is_recommand = models.BooleanField('推荐', default=False)

    class Meta:
        verbose_name='图书信息'
        verbose_name_plural = verbose_name
        ordering = ['-bookdate']

    def date_display(self):
        return self.bookdate.strftime('%Y'[:4]+'-'+'%m'[:2])

    def __unicode__(self):
        return self.bookname



    # def get_absolute_url(self):
    #     return reverse('booksys.views.collectLogin',args=[str(self.id)])



#用户信息模型
class UserInformation(models.Model):
    username=models.CharField('昵称',unique=True,max_length=20,default=None)
    userpassword=models.CharField('密码',max_length=20)
    sex=models.CharField('性别',max_length=2,choices=(('0','男'),('1','女')))
    book=models.ManyToManyField(BookInformation,verbose_name='图书',blank=True)
    class Meta:
        verbose_name='用户'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.username

# 评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    userpassword = models.CharField('密码', max_length=20)
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(UserInformation, blank=True, null=True, verbose_name='用户')
    # article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章')
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)






