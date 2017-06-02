"""create booksys urls in there"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bootstrap_test/$',views.test,name='test'),
    url(r'^about/$',views.about,name='about'),
    url(r'^index/$',views.index,name='index'),
    # url(r'^comment/$', views.article, name='article'),
    # url(r'^comment/post/$',views.comment_post,name='comment'),
    url(r'^tag/(?P<tag_id>[0-9]+)$',views.tag_page,name='tag_page'),
    url(r'^subject/(?P<bookid>[0-9]+)$',views.bookDetail,name='bookDetail'),
    url(r'^collect/(?P<bookid>[0-9]+)$',views.collectBook,name='collectBook'),
    url(r'^collectlogin/$',views.collectLogin,name='collectLogin'),
    url(r'^search/$',views.search_page,name='search_page'),

    url(r'^home/$',views.home,name='home'),
    url(r'^news/$',views.newsshow,name='newsshow'),
    url(r'^pop/$',views.popshow,name='popshow'),
    url(r'^styleshow/$',views.styleshow,name='styleshow'),
    # url(r'^register/(?P<userid>[0-9]+)/$',views.userregister,name='register_page'),
    # url(r'^register/$',views.re)
    url(r'^register/action$',views.registeraction,name='registeraction'),
    url(r'^login/$',views.userlogin,name='userlogin'),
    url(r'^usercenter/$',views.userCenter,name='userCenter'),
    url(r'^userinfo/$',views.userInformation,name='userinfo'),
    url(r'^delbook/(?P<bookid>[0-9]+)$',views.delBook,name='delBook'),
    url(r'^userEdit/(?P<user_id>[0-9]+)$',views.userEdit,name='userEdit'),
    url(r'^userEdit/action/$',views.userEditAction,name='userEditAction'),
    url(r'^logout/$',views.logout,name='logout'),
    # url(r'^recommendation/$',views.recommendationDemo,name='recommendation'),

]