#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import Context, Template
from boletos.models import *
from django.contrib.messages import constants as messages

import pyodbc                           #Biblioteca para conexao com banco de dados SQL Server
from datetime import datetime


def home(request):
    return render(request, 'home.html')

def bloco(request):
    return render(request, 'blocos.html')

#Funcao para conectar ao servidor de banco de dados
def conecta_servidor_bd():
    servidor = '131.221.84.38'
    db = 'ContilNetSGP'
    usuario = 'sac'
    senha = 'CNTsac18'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (servidor, db, usuario, senha))
    cursor = cnxn.cursor()
    return cursor

#Recebe o CPF do cliente e faz validacao do login
def valida_login(cpf_digitado, senha_digitada):

    if len(cpf_digitado) > 14:
        cursor = conecta_servidor_bd()
        cursor.execute("select ClienteID from Clientes where CNPJ='%s';" % (cpf_digitado))
        cliente = cursor.fetchone()
        cliente_id = str(cliente).replace(' ', '').replace(',', '').replace('(', '').replace(')', '')
    else:
        cursor = conecta_servidor_bd()
        cursor.execute("select ClienteID from Clientes where CPF='%s';" % (cpf_digitado))
        cliente = cursor.fetchone()
        cliente_id = str(cliente).replace(' ', '').replace(',', '').replace('(', '').replace(')', '')


    if str(cliente_id).count('None') == 0:
        cursor.execute("select Encerrado from Contratos where ClienteID='%s';" % (cliente_id))
        encerrado = cursor.fetchone()
        encerrado_id = str(encerrado).replace(' ', '').replace(',', '').replace('(', '').replace(')', '')

        if str(encerrado_id).count('False') == 1:
            cursor.execute("select Senha from Contratos where ClienteID='%s';" % (cliente_id))
            senha = cursor.fetchone()
            senha_id = str(senha).replace(' ', '').replace(',', '').replace('(', '').replace(')', '').replace('u\'','').replace('\'', '')

            if senha_digitada == senha_id:
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0


def captura_nome_id_cliente(cpf_digitado):
    cliente_inf = ''
    cursor = conecta_servidor_bd()
    if len(str(cpf_digitado)) < 16:
        cursor.execute("select ClienteID from Clientes where CPF=?;", (cpf_digitado))
        cliente = cursor.fetchone()
        cliente_id = str(cliente).replace(' ', '').replace(',', '').replace('(', '').replace(')', '')
    else:
        cursor.execute("select ClienteID from Clientes where CNPJ=?;", (cpf_digitado))
        cliente = cursor.fetchone()
        cliente_id = str(cliente).replace(' ', '').replace(',', '').replace('(', '').replace(')', '')

    cursor.execute("select Nome from Clientes where ClienteID='%s';" % (cliente_id))
    nome_ = cursor.fetchone()
    nome_cliente = str(nome_).replace(',', '').replace('(', '').replace(')', '').replace('u\'', '').replace('\'', '')

    cliente_inf += cliente_id +','+ nome_cliente
    return cliente_inf

def captura_inf_boleto(cpf_digitado):
    status_cobranca = {}
    cursor = conecta_servidor_bd()

    if len(str(cpf_digitado)) < 16:
        cursor.execute("select ClienteID from Clientes where CPF=?;", (cpf_digitado))
        cliente = cursor.fetchone()
        cliente_id = str(cliente).replace(' ', '').replace(',', '').replace('(', '').replace(')', '')
    else:
        cursor.execute("select ClienteID from Clientes where CNPJ=?;", (cpf_digitado))
        cliente = cursor.fetchone()
        cliente_id = str(cliente).replace(' ', '').replace(',', '').replace('(', '').replace(')', '')

    cursor.execute("select ContratoID from Contratos where ClienteID='%s';" % (cliente_id))
    contrato = cursor.fetchone()
    contrato_id = str(contrato).replace(' ', '').replace(',', '').replace('(', '').replace(')', '')

    cursor.execute("select CobrancaID from Contratos_Cobrancas where ContratoID='%s';" % (contrato_id))
    cobranca = cursor.fetchone()
    cobranca_id = ''
    while cobranca:
        cobranca_id += str(cobranca[0]) + ','
        cobranca = cursor.fetchone()
    cobranca_id = cobranca_id.split(',')
    cobranca_id = sorted(cobranca_id, reverse=True)

    for i in range(len(cobranca_id)):
        cursor.execute("select Cancelada from Contratos_Cobrancas where CobrancaID='%s';" % (cobranca_id[i]))
        cancelada = cursor.fetchone()
        cancelada_id = str(cancelada).replace(' ', '').replace(',', '').replace('(', '').replace(')','').replace('u\'', '').replace('\'', '')

        cursor.execute("select Recebido from Contratos_Cobrancas where CobrancaID='%s';" % (cobranca_id[i]))
        recebido = cursor.fetchone()
        status_recebimento = str(recebido).replace(' ', '').replace(',', '').replace('(', '').replace(')', '').replace('u\'', '').replace('\'', '')

        if cancelada_id.count('False'):
            #print 'https://sgp.contilnet.net/Contratos_Ativos_Boleto_Imprimir?CobrancaID='
            cursor.execute("select Valor from Contratos_Cobrancas where CobrancaID='%s';" % (cobranca_id[i]))
            valor = cursor.fetchone()
            valor_id = str(valor).replace(' ', '').replace(',', '').replace('(', '').replace(')', '').replace('u\'', '').replace('\'', '').replace('Decimal', '')

            cursor.execute("select Vencimento from Contratos_Cobrancas where CobrancaID='%s';" % (cobranca_id[i]))
            vencimento = cursor.fetchone()
            vencimento_id = str(vencimento).replace(' ', '').replace('(', '').replace(')', '').replace('u\'','').replace('\'','').replace('datetime.datetime', '').replace(',0,0,', '')
            vencimento_id = vencimento_id.split(',')
            data_vencimento = str(vencimento_id[2]) +'/'+ str(vencimento_id[1]) +'/'+ str(vencimento_id[0])
            status_cobranca[cobranca_id[i]] = data_vencimento, float(valor_id), status_recebimento
    return status_cobranca

def elimina_acentua(palavra):
    palavra = palavra.replace('\\','')
    if palavra.count('xc7'):
        palavra = palavra.replace('xc7','C')
    if palavra.count('xc3'):
        palavra = palavra.replace('xc3','A')
    if palavra.count('xc9'):
        palavra = palavra.replace('xc9','E')
    if palavra.count('xda'):
        palavra = palavra.replace('xda','U')
    if palavra.count('xd1'):
        palavra = palavra.replace('xd1','N')
    if palavra.count('xc2'):
        palavra = palavra.replace('xc2','A')
    if palavra.count('xc1'):
        palavra = palavra.replace('xc1','A')
    if palavra.count('xc0'):
        palavra = palavra.replace('xc0','A')
    if palavra.count('xc8'):
        palavra = palavra.replace('xc8','E')
    if palavra.count('xca'):
        palavra = palavra.replace('xca','E')
    if palavra.count('xcd'):
        palavra = palavra.replace('xcd','I')
    if palavra.count('xcc'):
        palavra = palavra.replace('xcc','I')
    if palavra.count('xce'):
        palavra = palavra.replace('xce','I')
    if palavra.count('xd4'):
        palavra = palavra.replace('xd4','O')
    if palavra.count('xd3'):
        palavra = palavra.replace('xd3','O')
    if palavra.count('xd2'):
        palavra = palavra.replace('xd2','O')
    if palavra.count('xd9'):
        palavra = palavra.replace('xd9','U')
    if palavra.count('xdc'):
        palavra = palavra.replace('xdc','U')
    return palavra
    #é,ú,ç,ã,ñ,Â Á À È Ê Í Ì Î Ô Ó Ò Ù Ü


def login(request):
    if request.method == 'POST':
        lista = []
        data_ = ''
        valor = ''
        datas = []
        cpf_cliente = request.POST.get('username')
        senha_cliente = request.POST.get('password')

        if str(cpf_cliente).count('.') == 0:
            cpf_valido = ''
            if len(cpf_cliente) > 12:
                for id, i in enumerate(cpf_cliente):
                    cpf_valido += i
                    if id == 1:
                        cpf_valido += '.'
                    elif id == 4:
                        cpf_valido += '.'
                    elif id == 7:
                        cpf_valido += '/'
                    elif id == 11:
                        cpf_valido += '-'
                cpf_cliente = cpf_valido

            else:
                for id,i in enumerate(cpf_cliente):
                    cpf_valido += i
                    if id == 2:
                        cpf_valido += '.'
                    elif id == 5:
                        cpf_valido += '.'
                    elif id == 8:
                        cpf_valido += '-'
                cpf_cliente = cpf_valido

        print cpf_cliente
        print senha_cliente

        vl = valida_login(cpf_cliente,senha_cliente)
        if vl == 0:
            msg = "CPF ou Senha Invalido!"
            return render(request, 'index.html', {'erro':msg})
        else:
            msg = ''
            cliente_inf = captura_nome_id_cliente(cpf_cliente)
            boleto_inf = captura_inf_boleto(cpf_cliente)

            cliente_inf = cliente_inf.split(',')
            for i in boleto_inf:
                status = ''
                data = ''
                valor = ''
                if str(boleto_inf[i][2]).count('False'):
                    status = 'F'
                else:
                    status = 'V'
                if str(boleto_inf[i][0]):
                    informacao = str(boleto_inf[i][0]).split('/')
                    dia = informacao[0]
                    mes = informacao[1]
                    ano = informacao[2]
                    if len(dia) == 1:
                        dia = '0' + dia + '/'
                    else:
                        dia = dia + '/'
                    if len(mes) == 1:
                        mes = '0' + mes + '/'
                    else:
                        mes = mes + '/'
                    data = str(dia) + str(mes) + str(ano)
                if str(boleto_inf[i][1]):
                    informacao = str(boleto_inf[i][1]).split('.')
                    inf = str(informacao[1])
                    if len(inf) == 1:
                        inf = inf+'0'
                    valor = str(informacao[0]) +','+ inf

                now = datetime.now()
                an = str(now.year)
                if str(ano).count(an):
                    lista.append((i,data,valor,status))
                    data_ += data + ','
                    datas.append(data)
            lista_ = []
            vals = []
            data_ = data_.split(',')
            data_ = sorted(data_, reverse=True)
            for i in lista:
                vals.append(int(i[0]))
            if vals:
                uniques = [i for i in vals if vals.count(i) < 2]  # lista de todos os valores unicos de vals
                max_value = max(uniques)
                min_value = min(uniques)
            else:
                min_value = ''
                max_value = ''


            #inicio = lista[0][0]
            #fim = lista[len(lista)-1][0]
            cliente = ''
            if cliente_inf[1]:
                cliente = elimina_acentua(str(cliente_inf[1]))
                c = str(cliente).split(' ')
                if len(c) > 2:
                    cliente = str(c[0]) + ' ' + str(c[1])
                    if len(c[2]) > 2:
                        cliente += ' ' + str(c[2])
            cliente = cliente.upper()

            for y in range(len(lista)):
                for i in lista:
                    if str(i).count(str(data_[y])):
                        lista_.append((data_[y],i[2],i[3],int(i[0])))
                        valor = i[2]
            print cliente
            print valor
            return render(request, 'logado.html', {'lista': lista_,'maximo': max_value, 'minimo': min_value, 'erro':msg, 'nome': cliente, 'valor':valor, 'data':datas})
    else:
        return render(request, 'index.html')





'''
<script language="Javascript">
function login()
{
var username = document.getElementById("usr").value;
var pass = document.getElementById("pwd").value;

if (username == "anderson" && pass == "123"){
    window.location.assign("localhost:8000/admin");
	alert("ok")
}else{
  if (username.length < 1 && pass.length < 1){
   alert("Preencha o campo usuario e senha");
  }else{
    if (username.length < 1){
        alert("Preencha o campo usuario corretamente");
    }else{
      alert("Preencha o campo senha corretamente");
    }
  }
}
}
</script>

'''