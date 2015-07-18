from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^miniter/', include('miniter.urls'))
]