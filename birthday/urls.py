from django.urls import path
from . import views
from .recent import LatestBirthDayFeed


app_name = 'birthday'

urlpatterns = [
    path('', views.home, name='home'),  # Define the URL pattern for the home view
    path('',views.post_list, name = 'post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name = 'post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/',LatestBirthDayFeed(), name='post_feed'),
    path('about/', views.about, name='about'),  # Define URL pattern for the about view
    path('events/', views.events, name='events'),  # Define URL pattern for the events view
    path('gallery/', views.gallery, name='gallery'),  # Define URL pattern for the gallery view
    path('contact/', views.contact, name='contact'),  # Define URL pattern for the contact view
]

