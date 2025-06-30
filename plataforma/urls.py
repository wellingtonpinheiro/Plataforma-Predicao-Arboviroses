from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from plataformaapp import views
import os

urlpatterns = [  #rotas
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('casos/', views.casos, name='casos'), 
    path('criadouros/', views.criadouros, name='criadouros'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))