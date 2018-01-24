from django.conf.urls import url

from demo import views

urlpatterns = [
    url(
        r'^$',
        views.HelloWorld.as_view(),
        name='hello-world',
    ),
]
