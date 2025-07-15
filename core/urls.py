from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    path('', include('school.urls', namespace ='school')),
    path('admin/', admin.site.urls),
    
]

if settings.DEBUG:
    
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR,'static'))
   
    
if settings.DEBUG:
    
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)