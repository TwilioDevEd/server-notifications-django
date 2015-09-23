from django.conf.urls import url


def error_handler(request):
    raise Exception('Uh on an error happened')

urlpatterns = [
    # Your URLs go here
    url(r'^error/$', error_handler),
]
