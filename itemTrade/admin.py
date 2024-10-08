from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Register your models here.

class ProfieInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('student_id','student_class','contact','facauty','dormitory')
    extra = 0

class UserAdmin(BaseUserAdmin):
    list_display = ('username','email')
    inlines = (ProfieInline,)

class ImageInline(admin.StackedInline):
    model = ItemImage
    can_delete = True
    verbose_name_plural = "images"
    fields = ('image',)

class CommentInline(admin.StackedInline):
    model = ReviewForItem
    can_delete = True
    verbose_name_plural = "comments"
    fields = ('owner','body')

class ItemAdmin(admin.ModelAdmin):
    fields = ('id','owner','name','description','count','price')
    readonly_fields = ('id','owner')

    inlines = (ImageInline,CommentInline)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Item,ItemAdmin)
admin.site.register(Trade)
admin.site.register(ItemImage)
admin.site.register(ReviewForItem)
admin.site.register(ReviewForTrade)
admin.site.register(ChatMessage)