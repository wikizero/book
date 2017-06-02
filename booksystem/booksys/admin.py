#admin:admin
#password:booksystem
from django.contrib import admin
from booksys.models import *

# Register your models here.
class BookInformationAdmin(admin.ModelAdmin):
    list_display = ('bookname','bookauthor','bookpublisher','bookpl','bookstar','bookdate','is_recommand',)
    search_fields = ('bookname','bookauthor','bookpublisher',)
    list_filter = ('bookdate',)
    list_select_related = True

class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('username','sex','userpassword',)
    search_fields = ('username',)

admin.site.register(BookInformation,BookInformationAdmin)
admin.site.register(UserInformation,UserInformationAdmin)
admin.site.register(BookTags)
# admin.site.register(AdminInformation)
# admin.site.register(Relations)