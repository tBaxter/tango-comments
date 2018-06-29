from django.urls import path, include

urlpatterns = [
    path('', include('django_comments.urls')),
    path('accounts/login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    path('accounts/logout/', 'django.contrib.auth.views.logout'),
]
