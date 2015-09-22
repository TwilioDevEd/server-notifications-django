from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Your URLs go here

    # Include the Django admin
    url(r'^admin/', include(admin.site.urls)),
]
