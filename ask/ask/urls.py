"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from app import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('hot/', views.index, name='hot'),

    path('question/<int:qid>/', views.question_page, name='question_page'),
    path('question/<int:qid>/leave_answer', views.leave_answer, name='leave_answer'),

    path('signup/', views.signup, name='signup'),
    path('singup/create_accaunt', views.create_accounts_add, name="create_accounts_add"),


    path('ask/', views.create_post, name='new_question'),
    path('ask/ask_question', views.ask_question, name='ask_question'),

    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('tag/<slug:tag_slug>', views.index, name='tag_page'),

    path('profile', views.user_profile, name='user_profile'),
    path('profile/done', views.user_profile_done, name='user_profile_done'),
    path('accounts/', include('django.contrib.auth.urls')),

]
