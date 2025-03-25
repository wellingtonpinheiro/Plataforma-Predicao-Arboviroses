from django.contrib import admin
from django.urls import path
from plataformaapp import views

urlpatterns = [  #rotas
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('casos/', views.casos, name='casos'), #EDITAR
    path('criadouros/', views.criadouros, name='criadouros'), #EDITARS
    path('logout/', views.logout_view, name='logout'),

]