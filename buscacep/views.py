#! /usr/bin/env python
# -*- coding: utf-8-*-
from django.views.generic import View
from django.http.response import HttpResponse

from buscacep_python_django.buscaCep import cep_json_javascript_xml


class BuscaCep(View):

    def get(self,request):
        if(request.GET.get("cep")):
            cep = request.GET.get("cep")
            formato = request.GET.get("formato") if request.GET.get("formato") else "json"
            retorno = cep_json_javascript_xml(cep,formato)
            return HttpResponse(retorno[0], content_type="application/"+retorno[1])
        else:
            return HttpResponse("Informe um cep válido por get. Ex: /buscacep/?cep=********&formato=(json/xml/plist/javascript)")
