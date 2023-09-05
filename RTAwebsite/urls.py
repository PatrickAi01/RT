from django.contrib import admin
from django.urls import path, include
from RTAwebsite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),

    path('register', views.register, name='register'), 
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('aiModels', views.aiModels, name='aiModels'),
    path('contact', views.contact, name='contact'),
    path('pricing', views.pricing, name='pricing'),
    path('conversion', views.conversion, name='conversion'),

    path('admin/', admin.site.urls),
    path('', views.dropUpload, name='dropUpload'),
    path('convert-mp3', views.convert_mp3, name='convert_mp3'),
    path('', views.download_converted_audio),
    path('download_converted_audio/', views.download_converted_audio, name='download_converted_audio'),
      # Map the default page to the same view
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)