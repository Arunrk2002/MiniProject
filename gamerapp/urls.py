from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('home',views.home,name="home"),
    path('ind',views.ind,name="ind"),
    #path('news',views.news,name="news"),
    path('log',views.log,name="reg"),
    path('reg',views.reg,name="reg"),
    path('spec',views.spec,name="spec"),
    path('get_pc_specs/',views.get_pc_specs,name="get_pc_specs"),
    path('indexus',views.indexus,name="indexus"),
    path('homeus',views.home,name="homeus"),
   # path('newsus',views.newsus,name="newsus"),
    path('games',views.games,name="games"),
    path('profile',views.profile,name="profile"),
    path('chatbot',views.chatbot,name="chatbot"),
    path('join',views.join,name="join"),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('save_pc_specs/', views.save_pc_specs, name='save_pc_specs'),
    path('chat/', views.chat_with_bot, name='chat_with_bot'),
    path('newsus/',views.newsus,name="newsus/"),
    path('search/', views.search, name='search_games'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('password-reset/', views.forget, name='password_reset'),  # This line
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('join',views.join,name="join"),
    path('events/', views.event_list, name='event_list'),
    path('search_games/', views.search_games, name='search_games'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
