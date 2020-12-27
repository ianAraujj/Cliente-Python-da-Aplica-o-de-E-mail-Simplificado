import requests
import time


url_base = "https://servidor-email.herokuapp.com/"
nome_usuario = ""


def verifica_nome(nome):

    if nome == "":
        print("[um nome deve ser fornecido]\n")
        return False
    
    url = url_base + "api/usuario/entrar"
    parametros = {
        "nome": nome
    }

    try:
        r = requests.post(url.encode(), data=parametros)

        if r.status_code == 200:
            print("\n --->> Ola novamente, " + nome + "!!!\n")
            return True
        
        if r.status_code == 201:
            print("\n --->> Seja Bem-vindo(a), " + nome + "!!!\n")
            return True

    except:
        print("\nxxxxxxxx---------> SERVIDOR INDISPONÍVEL\n")
        return False

def obter_nome():
    while True:
        nome_usuario = input("\n\nDigite seu Nome para Entrar: ")

        if verifica_nome(nome_usuario):
            break
    
    print('\n')
    return nome_usuario

def menu_principal():
    print("\n###################### MENU ####################################\n")
    print('1 - Enviar Mensagem\n')
    print('2 - Listar Minhas Mensagens\n\n')

def escolha_menu_principal():
    while True:
        escolha = input("Opção: ")

        if escolha == "1" or escolha == "2":
            break
        else:
            print(" --> Opção Inválida !!!\n")
    return escolha

def enviar_mensagem():

    print("\n+++++++++++++++++++++++ Nova Mensagem +++++++++++++++++++++++++++++")
    destinatario = input("\nDigite o nome do Destinatário: ")
    assunto = input("\nDigite o Assunto: ")
    corpo = input("\nDigite o Corpo da Mensagem: ")


    dados = {'destinatario': destinatario, "assunto": assunto, "corpo": corpo}
    url = url_base + "api/usuario/" + nome_usuario + "/mensagem/enviar"

    r = requests.post(url.encode(), data=dados)

    if r.status_code == 201:
        print("\n ----------------> Mensagem Enviada !!!")
        time.sleep(1)

    else:
        print("\n xxxxxx--------> " + str(r.json()['detalhes']))
        time.sleep(1)

def listar_mensagens():

    print("\n===================================================================")
    print("\n                       Suas Mensagens:")

    url = url_base + "api/usuario/" + nome_usuario + "/mensagem/listar"
    r = requests.get(url.encode())

    if r.status_code == 200:
        mensagens_json = r.json()
        mensagens = []

        for i in mensagens_json:
            numero = i['id']
            remetente = i['remetente']['nome']
            assunto = i['assunto']
            corpo = i['corpo']
            data = i['data']

            mensagens.append((numero, remetente, assunto, corpo, data))
        
        for m in mensagens:
            print("\n               ID da Mensagem: " + str(m[0]))
            print("\n                       - Remetente: " + m[1])
            print("\n                       - Assunto: " + m[2])
            print("\n")
        
        if len(mensagens) == 0:
            print("\n --> Voce não tem Mensagens !!!  :(  :( :(  :( :(  :( \n")

    else:
        print(r.text)
        print("Erro no Servidor!!!\n\n")

def menu_secundario():
    print("########################### OPÇÕES ################################")
    print('\n1 - Apagar Mensagem\n')
    print('2 - Abrir Mensagem\n')
    print('3 - Encaminhar Mensagem\n')
    print('4 - Responder Mensagem\n')
    print('5 - Listar Mensagens Novamente\n')
    print('6 - Voltar\n\n')

def escolha_menu_secundario():
    while True:
        escolha = input("Opção: ")

        if escolha == "1" or escolha == "2" or escolha == "3" or escolha == "4" or escolha == "5" or escolha == "6":
            break
        else:
            print(" --> Opção Inválida !!!\n")
    return escolha

def obter_id():

    while True:
        id = input("\n-> Digite o ID da Mensagem: ")

        try: 
            int(id)
            return id
        except ValueError:
            print("---- O ID deve ser um Inteiro ----\n")

def apagar_mensagem(id_mensagem):

    url = url_base + "api/usuario/" + nome_usuario + "/mensagem/" + str(id_mensagem) + "/apagar"
    r = requests.delete(url.encode())

    if r.status_code == 200:
        print("Mensagem Deletada !!!\n")
        time.sleep(1)
    else:
        print("\n xxxxx-----> " + str(r.json()['detalhes']) + "\n")

def abrir_mensagem(id_mensagem):

    url = url_base + "api/usuario/" + nome_usuario + "/mensagem/" + str(id_mensagem) + "/abrir"
    r = requests.get(url.encode())

    if r.status_code == 200:
        mensagem_json = r.json()

        print("\nID da Mensagem: " + str(mensagem_json['id']))
        print("\n       - Remetente: " + mensagem_json['remetente']['nome'])
        print("\n       - Assunto: " + mensagem_json['assunto'])
        print("\n       - Corpo: " + mensagem_json['corpo'])
        print("\n       - Data: " + mensagem_json['data'])
        print("\n")
    else:
        print("\n xxxxx-----> " + str(r.json()['detalhes']) + "\n")

def encaminhar_mensagem(id_mensagem):

    while True:
        destinatario = input("\nDigite o Nome do Destinatario: ")

        if destinatario != "":
            break
    
    url = url_base + "api/usuario/" + nome_usuario +  "/mensagem/" + str(id_mensagem) + "/encaminhar"
    dados = {
        "destinatario": destinatario
    }
    r = requests.post(url.encode(), data=dados)

    if r.status_code == 201:
        print("\n --> Mensagem Encaminhada para: " + destinatario + "\n")
        print("                         ....                           \n")
        time.sleep(1)
    else:
        print("\n xxxxx-----> " + str(r.json()['detalhes']) + "\n")

def responder_mensagem(id_mensagem):
    while True:
        resposta = input("\n ----> Digite a Resposta: ")

        if resposta != "":
            break
    
    url = url_base + "api/usuario/" + nome_usuario + "/mensagem/" + str(id_mensagem) + "/responder"
    dados = {
        "corpo": resposta
    }
    r = requests.post(url, data=dados)

    if r.status_code == 201:
        print("\n --> Mensagem Enviada !!!\n")
        time.sleep(1)
    else:
        print("\n xxxxx-----> " + str(r.json()['detalhes']) + "\n")



nome_usuario = obter_nome()

while True:

    menu_principal()

    opcao = escolha_menu_principal()

    if opcao == "1":
        enviar_mensagem()
    else:

        listar_mensagens()

        while True:

            menu_secundario()

            opcao_dois = escolha_menu_secundario()

            if opcao_dois != "6" and opcao_dois != "5":
                id_mensagem = obter_id()

                if opcao_dois == "1":
                    apagar_mensagem(id_mensagem)
                
                if opcao_dois == "2":
                    abrir_mensagem(id_mensagem)
                
                if opcao_dois == "3":
                    encaminhar_mensagem(id_mensagem)
                
                if opcao_dois == "4":
                    responder_mensagem(id_mensagem)
                
            if opcao_dois == "5":
                listar_mensagens()

            if opcao_dois == "6":
                break