from django.urls import include, path, re_path

from tango_comments.feeds import LatestCommentFeed

from testapp import views

feeds = {
     'comments': LatestCommentFeed,
}

urlpatterns = [
    path('', include('tango_comments.urls')),
    path('accounts/login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    path('accounts/logout/', 'django.contrib.auth.views.logout'),
    path('post/', views.custom_submit_comment),
    re_path(r'^flag/(\d+)/$', views.custom_flag_comment),
    re_path(r'^delete/(\d+)/$', views.custom_delete_comment),
    re_path(r'^approve/(\d+)/$', views.custom_approve_comment),
    re_path(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
    path('rss/comments/', LatestCommentFeed),
]
