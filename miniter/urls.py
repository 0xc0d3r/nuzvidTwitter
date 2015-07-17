from django.conf.urls import url

from miniter.views.register import register

urlpatterns = [
    # Examples:
    # url(r'^$', 'nuzvidTwitter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^register/$', register),
    url(r'^following/$',following),
    
]