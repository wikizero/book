#coding:utf-8
# import re
# from django.shortcuts import render_to_response
# from django.template import loader,Context
from cookielib import logger

from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.shortcuts import render,redirect


from .import models
# from models import *
from django.http import HttpResponseRedirect,HttpResponse
from booksys.forms import UserInformationsForm,LoginForm,CommentForm
from booksys.recommendations import *

# Create your views here.
def test(request):
    return render(request, 'booksys/bootstrap_test.html')
def about(request):
    return render(request,'booksys/about.html')

#首页
def index(request):
    #图书分类部分
    tag_list=models.BookTags.objects.all()

    #记住登录的用户
    username=request.session.get('username',None)

   #收藏碑榜展示部分
    rank = bookCountTop(request)

    return render(request,'booksys/index.html',locals())

#收藏碑榜功能实现，主要是搜索已经已经被收藏过的书籍
def bookCountTop(request):
    user_list = models.UserInformation.objects.all()
    user_book = {}

    for user in user_list:
        user_book.setdefault(user, user.book.all())

    book_user = transtData(user_book)

    book_count = {}
    for b, u in book_user.items():
        userCount = len(u)
        book_count.setdefault(b, userCount)
    # print book_count
    rank = sorted(book_count.items(), key=lambda d: (d[1],d[0].bookdate))[-12:]  # （图书，收藏人数）元组组成的列表

    rank.reverse()

    return rank


#图书标签分类显示图书信息列表部分
def tag_page(request,tag_id):
    tag_list = models.BookTags.objects.all()
    tag_id=models.BookTags.objects.get(pk=tag_id)
    # 记住登录的用户
    username = request.session.get('username', None)
    booktag_list=models.BookInformation.objects.filter(booktag=tag_id)
    #分页显示
    booktag_list=getPage(request,booktag_list)

    return render(request,'booksys/tag_page.html',locals())

#分页功能部分
def getPage(request,book_list):
    paginator=Paginator(book_list,7)
    try:
        page=int(request.GET.get('page',1))
        book_list=paginator.page(page)
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        book_list=paginator.page(1)
    return book_list

#获取图书详情功能
def bookDetail(request,bookid):
    tag_list = models.BookTags.objects.all()

    username=request.session.get('username',None)
    try:
        # 获取图书信息book
        book = models.BookInformation.objects.get(pk=bookid)
    except models.BookInformation.DoesNotExist:
        return render(request, 'booksys/fail_page.html', {'reason': '没有找到对应的图书'})
    # book=models.BookInformation.objects.get(pk=bookid)#得到获取的图书详情
    user_list = models.UserInformation.objects.all()
    # 利用物品相似度实现收藏该书的用户也收藏其它书的功能
    # 构造一个用户与书籍列表的字典
    user_book = {}
    recommendByBook = []
    for u in user_list:
        user_book.setdefault(u, u.book.all())
        # print user_book
    book_user = transtData(user_book)
    # print book_user
    # 推荐列表
    if book in book_user:
        recommendByBook = itemSimilarity(user_book, book)
        if username:
            user = models.UserInformation.objects.get(username=username)
            for ubook in recommendByBook:
                if ubook in user.book.all():
                    recommendByBook.remove(ubook)

    if username:
        user = models.UserInformation.objects.get(username=username)
        #如果打开的书籍是曾经收藏过的，设置收藏按钮不可用
        for cbook in user.book.all():
            if cbook == book:
                stated = 'disabled'
                stated = request.session.get('stated','active')


    return render(request,'booksys/bookdetail.html',locals())

#收藏图书
#以用户天天id=2收藏图书<世界的凛冬>id=15为例
#####################################
#user=models.UsernameInformation.objects.get(id=2)
#c_book=models.BookInformation.objects.get(id=15)
#user.book.add(c_book)
####################################
#收藏图书功能
def collectBook(request,bookid):
    tag_list = models.BookTags.objects.all()

    stated = 'active'
    username=request.session.get('username',None)
    user=models.UserInformation.objects.get(username=username)
    book=models.BookInformation.objects.get(pk=bookid)

    if request.method=='POST':
        #添加收藏的图书
        user.book.add(book)
        #设置按钮状态并且记住
        stated='disabled'
        request.session['stated']='disabled'

        return render(request,'booksys/bookdetail.html',locals())
    else:
        pass
    return render(request,'booksys/bookdetail.html',locals())

#用户删除收藏过的图书的功能
def delBook(request,bookid):
    username = request.session.get('username',None)
    user = models.UserInformation.objects.get(username=username)

    bookdel = models.BookInformation.objects.get(pk = bookid)

    if request.method == 'POST':
        if bookdel in user.book.all():
            user.book.remove(bookdel)
            # print bookdel
            # print bookdel.id
            return redirect('/booksys/usercenter/')

    return render(request,'booksys/usercenter.html')






#收藏按钮的模态框登录
def collectLogin(request):
    username=request.POST.get('username',None)
    userpassword=request.POST.get('userpassword',None)
    # source_url = request.POST.get('source_url', None)
    id = request.POST.get('id')
    print request.path+id, '-'*100
    if username:
        user_list=models.UserInformation.objects.all()
        for user in user_list:
            if user.username==username and user.userpassword==userpassword:
                request.session['username']=username
                print username
                return redirect('/booksys/subject/'+id)
    return HttpResponse('用户密码错误！')





#模糊搜索功能
def search_page(request):
    text = request.GET.get('text',None)
    textClean = text.strip()#去除前后空格
   # tag_name=request.GET.get('booktag',None)
   #  book_name=book_name.strip()#去除前后空格
   #  print book_name  #<QuerySet [<BookInformation: 百年孤独>]>
    #搜索还需要考虑用户误输入的空格，能够剔除空格的输入以及用户输入的关键词精确搜索
    search_list=models.BookInformation.objects.filter(Q(bookname__icontains = textClean)
                                                      | Q(bookauthor__icontains = textClean)
                                                      | Q(bookpublisher__icontains = textClean) )
    print search_list
    if search_list:
        return render(request, 'booksys/search_page.html', locals())
    return render(request, 'booksys/search_page.html', locals())



def home(request):
    return render(request,'booksys/home.html')

#用户注册
# def userregister(request,userid):
#     if str(userid)=='0':
#        # print (userid)
#         return render(request,'booksys/register_page.html')
#     user=models.UserInformation.objects.get(pk=userid)
#     return render(request,'booksys/register_page.html',{'user':user})

# def registeraction(request):
#     username=request.POST.get('username','USERNAME')
#     userpassword=request.POST.get('userpassword','USERPASSWORD')
#     sex=request.POST.get('sex','SEX')
#
#
#     models.UserInformation.objects.create(username=username,userpassword=userpassword,sex=sex)
#     users=models.UserInformation.objects.all()
   # print username
   #  return render(request,'booksys/index.html',{'users':users})

#使用form
# def registeraction(request):
#     if request.method=='POST':
#         userinformation_form=UserInformationsForm(request.POST)
#         if userinformation_form.is_valid():
#             models.UserInformation.objects.create(
#                 username=userinformation_form.cleaned_data['username'],
#                 userpassword=userinformation_form.cleaned_data['userpassword'],
#                 sex=userinformation_form.cleaned_data['sex'],
#             )
#             return HttpResponse('注册成功')
#
#     else:
#         userinformation_form=UserInformationsForm
#     return render(request,'booksys/register_page.html',locals())


#使用Model.Form  用户注册
def registeraction(request):
    if request.method=='POST':
        userinformation_form=UserInformationsForm(request.POST)
        if userinformation_form.is_valid():
            userinformation_form.save()
            return render(request,'booksys/login.html')
    else:
        userinformation_form=UserInformationsForm()
    return render(request,'booksys/register_page.html',locals())


#用户登录
def userlogin(request):
    username=request.POST.get('username',None)
    userpassword=request.POST.get('userpassword',None)
    if username:
        user_list=models.UserInformation.objects.all()
        for user in user_list:
            if user.username==username and user.userpassword==userpassword:
                request.session['username']=username
                # print user.id
                return HttpResponseRedirect("/booksys/index/",{'username':username})
    return render(request,'booksys/login.html')

# def userlogin(request):
#     try:
#         if request.method == 'POST':
#             login_form = LoginForm(request.POST)
#             if login_form.is_valid():
#                 # 登录
#                 username = login_form.cleaned_data["username"]
#                 userpassword = login_form.cleaned_data["userpassword"]
#                 user = authenticate(username=username, userpassword=userpassword)
#                 if user is not None:
#                     user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
#                     login(request, user)
#                 else:
#                     return render(request, 'booksys/fail_page.html', {'reason': '登录验证失败'})
#                 return redirect(request.POST.get('source_url'))
#             else:
#                 return render(request, 'booksys/fail_page.html', {'reason': login_form.errors})
#         else:
#             login_form =LoginForm()
#     except Exception as e:
#         logger.error(e)
#     return render(request, 'booksys/login.html', locals())

#用户个人中心
def userCenter(request):
    # 记住登录的用户
    username = request.session.get('username', None)
    print type(username)
    if username:
        user = models.UserInformation.objects.get(username=username)
        bookCount=user.book.all().count()

        # #分页展示收藏图书
        book_list = user.book.all()
        book_list = getPage(request,book_list)
        # print type(user)
    return render(request,'booksys/usercenter.html',locals())

#查看个人信息
def userInformation(request):
    username = request.session.get('username',None)
    user = models.UserInformation.objects.get(username=username)

    return  render(request,'booksys/usercenter.html',locals())

#用户修改改个人信息
def userEdit(request,user_id):
    user=models.UserInformation.objects.get(pk=user_id)
    return render(request,'booksys/user_edit.html',locals())

def userEditAction(request):

    username=request.POST.get('username','USERNAME')
    userpassword=request.POST.get('userpassword','USERPASSWORD')
    sex=request.POST.get('sex')
    user_id=request.POST.get('user_id')
    # userinformation_form=UserInformationsForm(request.POST)

    user=models.UserInformation.objects.get(pk=user_id)
    user.username=username
    request.session['username'] = username
    user.userpassword=userpassword
    user.sex=sex
    user.save()
    return redirect('/booksys/usercenter/')



#/用户退出操作
def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect("/booksys/index/")
    # return HttpResponseRedirect("/booksys/login/")

def newsshow(request):
    tag_list = models.BookTags.objects.all()


    #记住登录的用户
    username = request.session.get('username', None)
    # book_latest=models.BookInformation.objects.all().order_by('-bookdate')[:10]
    book_list=models.BookInformation.objects.all().order_by('-bookdate')[:250]
    # print book_list
    # for book in book_list:
    #     print book
    book_list=getPage(request,book_list)#括号中的book_list等于上面的model的book_list
    return render(request,'booksys/newsshow.html',locals())


def popshow(request):
    tag_list = models.BookTags.objects.all()

    # 记住登录的用户
    username = request.session.get('username', None)
    #根据人数较多的以及人数较多的
    # bookpop=models.BookInformation.objects.all().order_by('-bookpl').order_by('-bookstar')
    #等价于以下
    book_list=models.BookInformation.objects.all().order_by('-bookstar').order_by('-bookpl')[:250]
    book_list=getPage(request,book_list)
    return render(request,'booksys/popshow.html',locals())

#用户个性化推荐模块
def styleshow(request):
    tag_list = models.BookTags.objects.all()

    #记住登录的用户
    username=request.session.get('username',None)
    # print type(username)
    if username:
        user=models.UserInformation.objects.get(username=username)
        # print type(user)
        user_list=models.UserInformation.objects.all()

        #站长推荐
        book_List=models.BookInformation.objects.filter(is_recommand='1').order_by('-bookpl').order_by('-bookstar')
        # booktest = user.book.all().order_by('bookdate')
        book_list = []
        for book in book_List:
            if book not in user.book.all():
                book_list.append(book)
        book_list=getPage(request,book_list)

        #构造用户-物品列表字典
        user_book=dict()#所有用户-物品列表
        for u in user_list:
            user_book.setdefault(u,u.book.all())#构造{user1:[book1,book2,...]，user2:[book2,book3,...]}形式的字典

        #基于用户的协同过滤算法
        bookOfRecommendByUser = recommendationByUserSimilarityToUser(user_book, user)
        print "bookOfRecommendByUser:",bookOfRecommendByUser
        print "\n"

        #基于物品的协同过滤算法
        bookOfRecommendByItemList = recommendationByItemSimilarityToUser(user_book,user)[:10]

        print ('bookOfRecommendByItemList:', bookOfRecommendByItemList)

    return render(request,'booksys/styleshow.html',locals())

#实现推荐功能部分
# def recommendationDemo(request):
#     usertest=models.UserInformation.objects.get(pk=3)
#     print ('type(usertest)=',type(usertest))
#     user_list=models.UserInformation.objects.all()
#     user_book=dict()
#     # print type(user_list)
#     for userdemo in user_list:
#         user_book.setdefault(userdemo,userdemo.book.all())
#
#     print user_book
#     who=userSimilarityTest(user_book,usertest)
#     print who
#     similarityUser=models.UserInformation.objects.get(username=who)
#     recommendBook=getRecommendationUser(user_book,usertest)
#     print ('recommendBook=',recommendBook)
#     R={}
#
#     userBookAll=usertest.book.all()
#     for book in userBookAll:
#         rB=itemSimilarity(user_book,book)
#         rB_Common_userBookAll=set(userBookAll)&set(rB)
#         if book not in R:
#             N = []
#             for b in rB:
#                 if b not in rB_Common_userBookAll:
#                     N.append(b)
#             R.setdefault(book,N)
#             print ('\n')
#     rl=R.keys()
#     for r in rl:
#         rv=R[r]
#         print ('rv:',rv)
#
#     print ('R:',R)


    # C=set(R)&set(usertest.book.all())
    # N=[]
    # for b in R:
    #     if b not in C:
    #         N.append(b)
    # print N

    # for book in similarityUser.book.all():


    # #转换成物品-用户表
    # book_user=dict()
    # for u,b in user_book.items():
    #     for bi in b:
    #         if bi not in book_user:
    #             book_user[bi]=[]
    #         book_user[bi].append(u)
    # print book_user

    # C=dict()
    # N=dict()
    # for b,users in book_user.items():
    #     for u in users:
    #         N[u.username]+=1
    #         for v in users:
    #             if u==v:
    #                 continue
    #             C[u.username][v.username]+=1
    #
    # W=dict()
    # for u,related_users in C.items():
    #     for v,cuv in related_users.items():
    #         W[u][v]=cuv/math.sqrt(N[u]*N[v])
    # print W


    # return render(request,'booksys/recommendation_page.html',locals())



