from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('catracadigital.core.urls', namespace='core')),
    url(r'^api/', include('catracadigital.api.urls', namespace='api')),
    url(r'^admin/', admin.site.urls),
]
