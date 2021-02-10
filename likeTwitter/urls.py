"""likeTwitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

from app import views
from app.handlers.tweet_action_handler import TweetActionHandler
from app.handlers.user_mgmt import UserManagementHandler
from app.handlers.follow_action_handler import FollowActionHandler

schema_view = get_swagger_view(title="likeTwitter API")
tweet_action_handler = TweetActionHandler.as_view()
user_mgmt_handler = UserManagementHandler.as_view()
follow_action_handler = FollowActionHandler.as_view()


urlpatterns = [
    path(r'^$', schema_view),
    path('admin/', admin.site.urls),
    path('user', user_mgmt_handler),
    path('follow', follow_action_handler),
    path('tweet', tweet_action_handler)
]
