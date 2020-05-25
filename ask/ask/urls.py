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
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from app.models import LikeDislike
from app.models import Article, Comment
from app.views import CreateAccount, SettingProfile, CreatePost, Questions
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('hot/', views.index, name='hot'),

    path('question/<int:qid>/', Questions.as_view(), name='question_page'),
    path('signup/', CreateAccount.as_view(), name='signup'),
    path('ask/', CreatePost.as_view(), name='new_question'),
    path('profile', SettingProfile.as_view(), name='user_profile'),

    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('tag/<slug:tag_slug>', views.index, name='tag_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

