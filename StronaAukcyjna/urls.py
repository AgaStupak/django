from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from Aukcje import views as view_core
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^signup/$', view_core.signup, name='signup'),
    url(r'^accounts/password/$', view_core.change_password, name='change_password'),
    url(r'accounts/edit_profile/$', view_core.edit_profile, name='edit_profile'),
    url(r'', include('Aukcje.urls')),
    url(r'^chaining/', include('smart_selects.urls')),


]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)