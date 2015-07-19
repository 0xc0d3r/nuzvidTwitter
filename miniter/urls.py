from django.conf.urls import url

from miniter.views.register import register
from miniter.views.following import following
from miniter.views.followers import get_followers
from miniter.views.searchProfile import search

urlpatterns = [
    # Examples:
    # url(r'^$', 'nuzvidTwitter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^register/$', register),
    url(r'^following/$',following),
    url(r'^followers/$',get_followers),
    url(r'^search/$',search),
]
