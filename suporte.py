import cv2                                                                      # Importing the opencv
import pyrebase
import os
import sys

face_cascade = cv2.CascadeClassifier('Haar/haarcascade_frontalcatface.xml') # Classifier "frontal-face" Haar Cascade
eye_cascade = cv2.CascadeClassifier('Haar/haarcascade_eye.xml') # Classifier "eye" Haar Cascade

recognise = cv2.face.EigenFaceRecognizer_create(15,4000)  # creating EIGEN FACE RECOGNISER
recognise.read("Recogniser/trainingDataEigan.xml")                              # Load the training data


config = {
    "apiKey": "AIzaSyALp47c9KYsGN21KuYMLBiXztJzkTB9_RQ",
    "authDomain": "banmequer-devloide.firebaseio.com",
    "databaseURL": "https://banmequer-devloide.firebaseio.com",
    "projectID": "banmequer-devloide",
    "storageBucket": "banmequer-devloide.appspot.com",
    "messagingSenderId": "61021516767"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('diego.ijcpm2017@gmail.com', 123456)
db = firebase.database()

def error():
    print('Nao foi possivel identificar cliente! Tente novamente mais tarde!')
    sys.exit()


def loop():
    print ('1 - Menu Completo')
    print ('2 - Finalizar Sessao')
    opcao1 = int(eval(input(': ')))
    if opcao1 == 1:
        a = funcao_menu(nome, code)
        print(a)
    elif opcao1 == 2:
        f = finalizar_sessao()
        print(f)
    else:
        os.system('cls')
        print("Nao ha essa opcao!")

def finalizar_sessao():
    os.system('cls')
    print ('Sessao Encerrada! Obrigado!')
    espera = eval(input(""))

def funcao_menu(nome,code):
    acesso = db.child('devloide/clientes').child(nome).child('usuario').get(user['idToken'])
    passe = db.child('devloide/clientes').child(nome).child('senha').get(user['idToken'])
    if (nome == acesso.val()) and (code == passe.val()):
            os.system('cls')
            print ('Seja bem vindo, {}'.format(nome))
            print ('1 - Credito')
            print ('2 - Saldo')
            print ('3 - Saque')
            print ('4 - Transferencia')
            opcao = int(eval(input("Escolha uma opcao : ")))
            if opcao == 1:
                credito = db.child('devloide/clientes').child(nome).child('credito').get(user['idToken'])
                os.system('cls')
                print(('Voce tem R$ {} de credito'.format(credito.val())))
                print('1 - Menu Completo')
                print('2 - Finalizar Sessao')
                opcao1 = int(eval(input(': ')))
                if opcao1 == 1:
                    a = funcao_menu(nome, code)
                    print(a)
                elif opcao1 == 2:
                    f = finalizar_sessao()
                    print(f)
                else:
                    os.system('cls')
                    print("Nao ha essa opcao!")


            elif opcao == 2:
                saldo = db.child('devloide/clientes').child(nome).child('saldo').get(user['idToken'])
                os.system('cls')
                print(('Voce tem R$ {} de saldo'.format(saldo.val())))
                print('1 - Menu Completo')
                print('2 - Finalizar Sessao')
                opcao1 = int(eval(input(': ')))
                if opcao1 == 1:
                    a = funcao_menu(nome, code)
                    print(a)
                elif opcao1 == 2:
                    f = finalizar_sessao()
                    print(f)
                else:
                    os.system('cls')
                    print("Nao ha essa opcao!")

            elif opcao == 3:
                os.system('cls')
                saque = float(eval(input("Informe a quantia do saque: ")))
                saldo = db.child('devloide/clientes').child(nome).child('saldo').get(user['idToken'])
                if (saque > saldo.val()):
                    print ("Voce nao tem saldo suficiente!")
                    print('1 - Menu Completo')
                    print('2 - Finalizar Sessao')
                    opcao1 = int(eval(input(': ')))
                    if opcao1 == 1:
                        a = funcao_menu(nome, code)
                        print(a)
                    elif opcao1 == 2:
                        f = finalizar_sessao()
                        print(f)
                    else:
                        os.system('cls')
                        print("Nao ha essa opcao!")
                else:
                    saldo_atualizado = saldo.val() - saque
                    db.child('devloide/clientes').child(nome).update({'saldo':saldo_atualizado}, user['idToken'])
                    print(("Saque de R$ {} realizado com sucesso.".format(saque)))
                    print('1 - Menu Completo')
                    print('2 - Finalizar Sessao')
                    opcao1 = int(eval(input(': ')))
                    if opcao1 == 1:
                        a = funcao_menu(nome, code)
                        print(a)
                    elif opcao1 == 2:
                        f = finalizar_sessao()
                        print(f)
                    else:
                        os.system('cls')
                        print("Nao ha essa opcao!")
            elif opcao == 4:
                os.system('cls')
                titular = input("Informe o destinatario do deposito: ")
                conta = int(eval(input("Informe a conta para a transferencia: ")))
                valor = float(eval(input("Informe a quantia a ser depositada: ")))

                acesso1 = db.child('devloide/clientes').child(titular).child('usuario').get(user['idToken'])
                conta_1 = db.child('devloide/clientes').child(titular).child('conta').get(user['idToken'])
                saldo = db.child('devloide/clientes').child(nome).child('saldo').get(user['idToken'])

                if (titular == acesso1.val() and conta == conta_1.val() and saldo.val() >= valor ):

                #ala destinatario
                    saldo1 = db.child('devloide/clientes').child(titular).child('saldo').get(user['idToken'])
                    saldo_atualizado_transferencia_destinatario = valor + saldo1.val()
                    db.child('devloide/clientes').child(titular).update({'saldo': saldo_atualizado_transferencia_destinatario}, user['idToken'])

                # ala origem
                    saldo2 = db.child('devloide/clientes').child(nome).child('saldo').get(user['idToken'])
                    saldo_atualizado_transferencia_origem = saldo2.val()- valor
                    db.child('devloide/clientes').child(nome).update({'saldo': saldo_atualizado_transferencia_origem},user['idToken'])
                    os.system('cls')
                    print(("Deposito no valor de {} realizado com sucesso".format(valor)))
                print('1 - Menu Completo')
                print('2 - Finalizar Sessao')
                opcao1 = int(eval(input(': ')))
                if opcao1 == 1:
                    a = funcao_menu(nome, code)
                    print(a)
                elif opcao1 == 2:
                    f = finalizar_sessao()
                    print(f)
                else:
                    os.system('cls')
                    print("Nao ha essa opcao!")
            else:
                    os.system('cls')
                    print ("Verifique os dados inseridos!")
                    print('1 - Menu Completo')
                    print('2 - Finalizar Sessao')
                    opcao1 = int(eval(input(': ')))
            if opcao1 == 1:
                a = funcao_menu(nome, code)
                print(a)
            elif opcao1 == 2:
                f = finalizar_sessao()
                print(f)
            else:
                os.system('cls')
                print("Nao ha essa opcao!")
                ver = eval(input(""))
    else:
            os.system('cls')
            print("Verifique suas credenciais!")