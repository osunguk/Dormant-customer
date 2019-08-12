"""dormant_account URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',app.views.home,name='home'),
    path('login',app.views.login,name='login'),
    path('logout',app.views.logout,name='logout'),
    path('signup',app.views.signup,name='signup'),
    path('write',app.views.write,name='write'),
    path('user',app.views.user,name='user'),
    path('board',app.views.board,name='board'),
    path('detail/<int:number>',app.views.detail,name='detail'),
    path('detail/<int:number>/edit',app.views.edit,name='edit'),
    path('detail/<int:number>/delete',app.views.delete,name='delete')
]
