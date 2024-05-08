from django.contrib import admin
from .models import Birthday, BirthdayMessage, BirthdayCard, Event, Gift, Photo
from .models import Post

@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth')

@admin.register(BirthdayMessage)
class BirthdayMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'date_sent')

@admin.register(BirthdayCard)
class BirthdayCardAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'sent_date')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location')

@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'date_given')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'upload_date')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
