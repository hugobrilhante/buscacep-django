from django.conf.urls import patterns, include, url
from buscacep_python_django.views import BuscaCep

urlpatterns = patterns('',

    url(r'^buscacep/', BuscaCep.as_view()),

)
