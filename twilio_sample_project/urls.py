from django.urls import path


def error_handler(request):
    raise Exception('Uh oh an error happened')


urlpatterns = [
    # Your URLs go here
    path('error/', error_handler),
]
