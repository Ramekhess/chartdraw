from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'index_page'

urlpatterns = [
    # /
    url(r'^$', views.index_view, name='index'),
    url(r'^manip/$', views.manip, name='manip'),
    url(r'^ictest/$', views.IC_test, name='IC_test'),
    url(r'^hypo/$', views.hypo, name='Hypo'),
    url(r'^features/$', views.features, name='features'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
