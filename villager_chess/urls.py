"""
URL configuration for villager_chess project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
# removed AiView from line below for deployment
from villager_chess_api.views import PlayerView, GameView, CommunityPostView, MessageView, TimeSettingView, TournamentView, login_user, register_user, GuestView
# from villager_chess_api.views.ai_handler import AiView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'players', PlayerView, 'player')
router.register(r'games', GameView, 'game')
router.register(r'timesettings', TimeSettingView, 'time_setting')
router.register(r'tournaments', TournamentView, 'tournament')
router.register(r'messages', MessageView, 'message')
router.register(r'communityposts', CommunityPostView, 'community_post')
# router.register(r'ai_response', AiView, 'ai')
router.register(r'guests', GuestView, 'guest')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
    # path('ai', view=AiView, name="ai"),
]
