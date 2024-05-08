from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from birthday.mapped_to import PostSitemap  # Import PostSitemap class
from django.contrib.sitemaps.views import sitemap

# Define sitemaps dictionary
sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    # Other URL patterns
    path('admin/', admin.site.urls),  # Include Django's admin URLs
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    # Include the URL configuration for your app(s) here
    path('', include('birthday.urls')),  # Include the app's URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
