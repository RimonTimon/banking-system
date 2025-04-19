from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from transaction.views import landing_page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('transaction/',include('transaction.urls')),
    path('',landing_page,name='landing_page')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
