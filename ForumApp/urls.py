from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ForumApp import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ForumApp.posts.urls')),
    path('accounts/', include('ForumApp.accounts.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
