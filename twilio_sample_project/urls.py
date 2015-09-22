from django.conf.urls import include, url
from django.contrib import admin


def error_handler(request):
    raise Exception('Uh on an error happened')

urlpatterns = [
    # Your URLs go here
    url(r'^error/$', error_handler),

    # Include the Django admin
    url(r'^admin/', include(admin.site.urls)),
]
