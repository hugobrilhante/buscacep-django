#! /usr/bin/env python
# -*- coding: utf-8-*-
import os
import sys
import json
import urllib
import urllib2
from bs4 import BeautifulSoup

def cep_json_javascript_xml(cep,formato):
    cepEntrada = cep
    tipoCep    =""
    cepTemp    =""
    metodo     ="buscarCep"
    formato    = formato.lower()

    url = 'http://m.correios.com.br/movel/buscaCepConfirma.do'
    
    post_data_dictionary = {'cepEntrada': cepEntrada, 'tipoCep': tipoCep, 'cepTemp': cepTemp, 'metodo':metodo}
    
    #codifica os dados POST para ser enviado em uma URL
    post_data_encoded = urllib.urlencode(post_data_dictionary)
    
    try:
        #objeto request que armazena os dados do POST e da URL
        request_object = urllib2.Request(url, post_data_encoded)
        
        #faz o request usando o objeto request como um argumento e armazena a resposta em uma variavel
        response = urllib2.urlopen(request_object)
        
        #armazena a resposta em uma string
        result = response.read()
        
        #extrair dados de arquivos HTML (result)
        soup = BeautifulSoup(result)
        
        #seleciona as tags com essas classes
        values = soup.select(".caixacampobranco span.respostadestaque ")
        

        if len(values) > 2:
            resultado=1
            resultado_txt = "Sucesso cep completo"
            #remove outras informacoes que vem junto ao logradouro. Exemplo: - de 1000 a 2000 e impar
            logradouro = (values[0].get_text().strip()).split('-')
            logradouro = logradouro[0]
            #extrai os valores das tags
            bairro = values[1].get_text().strip()
            cidade_estado = values[2].get_text().split()
            cidade = cidade_estado[0]
            estado = cidade_estado[1].strip('/')
            cep = values[3].get_text().strip()            
        elif len(value) < 2:
            resultado=2
            resultado_txt = "Sucesso cep unico"
            logradouro = ""
            bairro = ""
            cidade_estado = values[0].get_text().split()
            cidade = cidade_estado[0]
            estado = cidade_estado[1].strip('/')
            cep = values[1].get_text().strip()
        else:
            resultado = 0
            resultado_txt = "Servico indisponivel ou cep invalido"
            logradouro = ""
            bairro = ""
            cidade = ""
            estado = ""
            cep = ""

    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file = exc_tb.tb_frame.f_code.co_filename
        retorno = json.dumps({'cod': 400, 'msg': 'Type: %s, Error: %s, File: %s, Line %s' % (exc_type, exc_obj, file, exc_tb.tb_lineno)})
        return retorno,formato

        
        
    dict_json = {'resultado': resultado, 'resultado_txt': resultado_txt, 'logradouro' :logradouro, 'bairro': bairro, 'cidade': cidade, 'uf': estado, 'cep':cep}
    
   
    if formato == 'json':
        retorno = json.dumps(dict_json)
    elif formato == 'javascript':
        retorno = "var resultadoCEP = ",json.dumps(dict_json, sort_keys=True, indent=20)
    elif formato == 'xml':
        retorno = open(os.path.join(os.path.dirname(__file__), 'cep.xml'),'r').read()%dict_json
    elif formato == 'plist':
        retorno = open(os.path.join(os.path.dirname(__file__), 'cep.plist'),'r').read()%dict_json
        formato = 'xml'
    else:
        retorno = "Opcao nao existe"


    return retorno,formato
