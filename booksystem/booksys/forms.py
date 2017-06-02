#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django import forms
from booksys.models import UserInformation,Comment
from django.core.exceptions import ValidationError

#表单字段的验证器
def validate_name(value):
    try:
        UserInformation.objects.get(username=value)
        raise ValidationError("%s该用户已被注册"%value)
    except UserInformation.DoesNotExist:
        pass
#表单form
# class UserInformationsForm(forms.Form):
#     username=forms.CharField(label='用户名',error_messages={"required":"必填"})
#     userpassword=forms.CharField(label='密码',error_messages={"required":"必填"})
#     sex=forms.ChoiceField(label=u'性别：',
#                  choices=((u'0', u'男'), (u'1', u'女'),),
#                  widget=forms.RadioSelect(),error_messages={"required":"必填"})


#使用Model.Form
class UserInformationsForm(forms.ModelForm):
#
    username=forms.CharField(label='昵称',widget=forms.TextInput(attrs={"placeholder": "昵称","required": "required",}),
                              max_length=20,error_messages={"required": "username不能为空",},validators=[validate_name])#对某字段的验证
    userpassword=forms.CharField(label='密码',widget=forms.PasswordInput(attrs={"placeholder": "密码","required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})
#clean_filename验证字段，针对某个字段进行验证
    # def clean_name(self):
    #     value=self.cleaned_data.get('username')
    #     try:
    #         UserInformation
    class Meta:
        model=UserInformation
        exclude=('id','book',)

class LoginForm(forms.Form):
    '''
    登录Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "昵称", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    userpassword = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "密码", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})


class CommentForm(forms.ModelForm):
    '''
    评论表单
    '''
    author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
                                                           "required": "required","tabindex": "1"}),
                              max_length=50,error_messages={"required":"username不能为空",})
    userpassword = forms.CharField(widget=forms.TextInput(attrs={"id":"userpassword","placeholder": "密码","class": "comment_input", "required": "required","tabindex": "2" }),
                                   max_length=20, error_messages={"required": "password不能为空", })

    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "3"}),
                                                    error_messages={"required":"评论不能为空",})

    # class Meta:
    #     model=Comment
    #     exclude=('id','user_id',)