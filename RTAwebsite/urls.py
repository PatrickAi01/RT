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

    path('aiModels', views.aiModels, name='aiModels'),
    path('contact', views.contact, name='contact'),
    path('pricing', views.pricing, name='pricing'),
    path('conversion', views.conversion, name='conversion'),
    path('player', views.list_and_download_audio, name='list_and_download_audio'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)