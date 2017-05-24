from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^hello-world/', views.HelloWorld.as_view(), name='overview'),
    url(r'^docs/', views.schema_view, name='docs'),
]
