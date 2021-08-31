import pyrebase
import cv2  # Importing the opencv
import numpy as np  # Import Numarical Python
import NameFind # Import NameFind function
import os

WHITE = [255, 255, 255]

#   import the Haar cascades for face ditection
face_cascade = cv2.CascadeClassifier('Haar/haarcascade_frontalcatface.xml')  # Classifier "frontal-face" Haar Cascade
eye_cascade = cv2.CascadeClassifier('Haar/haarcascade_eye.xml')  # Classifier "eye" Haar Cascade

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

class Master(object):
    #def __init__(self,nome,idade,cpf,renda,senha):
    def __init__(self,nome,cpf):
        self.nome = nome
        self.cpf = cpf

class cliente(Master):
    def __init__(self,nome,cpf,idade,renda,senha):
        super(cliente,self).__init__(nome,cpf)
        self.idade = idade
        self.renda = renda
        self.senha = senha

class gerente(Master):
    def __init__(self,nome,cpf,genero):
        super(gerente,self).__init__(nome,cpf)
        self.genero=genero

def fim():
    os.system('cls')
    print ('Sessao Encerrada!')



def insert_cliente(nome,idade,cpf,renda,senha,credito):
    id = db.child('devloide/clientes/id').child('id_atualizado').get(user['idToken'])
    id_cliente = id.val() + 1

    db.child('devloide/clientes').child(nome).update({'usuario': nome}, user['idToken'])
    db.child('devloide/clientes').child(nome).update({'conta': id_cliente}, user['idToken'])
    db.child('devloide/clientes').child(nome).update({'idade': idade}, user['idToken'])
    db.child('devloide/clientes').child(nome).update({'cpf': cpf}, user['idToken'])
    db.child('devloide/clientes').child(nome).update({'renda': renda}, user['idToken'])
    db.child('devloide/clientes').child(nome).update({'credito': credito}, user['idToken'])
    db.child('devloide/clientes').child(nome).update({'senha': senha}, user['idToken'])
    db.child('devloide/clientes').child(nome).update({'saldo': credito}, user['idToken'])
    db.child('devloide/clientes/id').update({'id_atualizado': id_cliente}, user['idToken'])

    ID = NameFind.AddName(nome)
    Count = 0
    cap = cv2.VideoCapture(0)  # Camera object

    while Count < 50:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the Camera to grayScale
        if np.average(gray) > 110:  # Testing the brightness of the image
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # Detect the faces and store the positions
            for (x, y, w, h) in faces:  # Frames  LOCATION X, Y  WIDTH, HEIGHT
                FaceImage = gray[y - int(h / 2): y + int(h * 1.5),
                            x - int(x / 2): x + int(w * 1.5)]  # The Face is isolated and cropped
                Img = (NameFind.DetectEyes(FaceImage))
                cv2.putText(gray, "FACE DETECTED", (x + int((w / 2)), y - 5), cv2.FONT_HERSHEY_DUPLEX, .4, WHITE)
                if Img is not None:
                    frame = Img  # Show the detected faces
                else:
                    frame = gray[y: y + h, x: x + w]
                cv2.imwrite("dataSet/User." + str(ID) + "." + str(Count) + ".jpg", frame)
                cv2.waitKey(300)
                cv2.imshow("CAPTURED PHOTO", frame)  # show the captured image
                Count = Count + 1
        cv2.imshow('Face Recognition System Capture Faces', gray)  # Show the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print('FACE CAPTURE FOR THE SUBJECT IS COMPLETE')
    cap.release()
    cv2.destroyAllWindows()


    print('Cliente inserido!')
    print('1 - Menu Completo')
    print('2 - Encerrar Sessao')
    op = int(eval(input("")))
    if op == 1:
         return menu(nome, code)
    elif op == 2:
        p = fim()
        print(p)
    ####FALTA CONTINUAR (DAR A CONTINUIDADE)


def menu(nome, code):
    autuser = db.child('devloide/gerentes').child(nome).child('nome').get(user['idToken'])
    autid = db.child('devloide/gerentes').child(nome).child('id').get(user['idToken'])
    if (nome == autuser.val()) and (code == autid.val()):
        os.system('cls')
        print ('1 - Criar Gerente Chefe')
        print ('2 - Inserir Cliente')
        print ('3 - Remover  Cliente')
        print ('4 - Encerrar Sessao')
        escolha = int(eval(input('')))

        if (escolha == 1):
            gerente1 = gerente('joao', 1234, 'masculino')
            os.system('cls')
            gerente1.nome = input('Nome: ')
            gerente1.cpf = float(eval(input('CPF: ')))
            gerente1.genero = input('Sexo: ')
            id = db.child('devloide/gerentes/id').child('id_atualizado').get(user['idToken'])
            id_gerente = id.val() + 100
            db.child('devloide/gerentes').child(gerente1.nome).update({'nome': gerente1.nome}, user['idToken'])
            db.child('devloide/gerentes').child(gerente1.nome).update({'cpf': gerente1.cpf}, user['idToken'])
            db.child('devloide/gerentes').child(gerente1.nome).update({'genero': gerente1.genero}, user['idToken'])
            db.child('devloide/gerentes').child(gerente1.nome).update({'id': id_gerente}, user['idToken'])
            db.child('devloide/gerentes/id').update({'id_atualizado': id_gerente}, user['idToken'])
            print('Gerente Chefe criado!')
            print ('1 - Menu Completo')
            print ('2 - Encerrar  sessao')
            op = int(eval(input("")))
            if op == 1:
                p = menu(nome,code)
                print(p)
            elif op==2:
                p = fim()
                print(p)
        elif escolha == 2:

            cliente1 = cliente('pedro', 12345, 0o53455, 12000, 123)
            os.system('cls')
            cliente1.nome = input('Informe o nome do cliente: ')
            cliente1.idade = int(eval(input('Informe a idade do cliente: ')))
            cliente1.cpf = float(eval(input('Informe o cpf do cliente: ')))
            cliente1.renda = int(eval(input('Informe a renda do cliente: ')))
            cliente1.senha = int(eval(input('Crie a senha do usuario: ')))
            if (cliente1.idade >= 18 and cliente1.idade <= 30 and cliente1.renda == 0):
                credito = 200
                chamada = insert_cliente(cliente1.nome, cliente1.idade, cliente1.cpf, cliente1.renda, cliente1.senha,credito)
                print(chamada)
            elif (cliente1.idade >= 18 and cliente1.idade <= 50 and cliente1.renda >= 900 and cliente1.renda <= 1000):
                credito = 500
                chamada = insert_cliente(cliente1.nome, cliente1.idade, cliente1.cpf, cliente1.renda, cliente1.senha,credito)
                print(chamada)
            elif (cliente1.idade >= 18 and cliente1.idade <= 90 and cliente1.renda >= 1000):
                credito = 1300
                chamada = insert_cliente(cliente1.nome, cliente1.idade, cliente1.cpf, cliente1.renda, cliente1.senha,credito)
                print(chamada)
            else:
                os.system('cls')
                print('Solicitacao indeferida!')
                print ('1 - Menu Completo')
                print ('2 - Encerrar  sessao')
                op = int(eval(input("")))
                if op == 1:
                    p = menu(nome, code)
                    print(p)
                elif op == 2:
                    p = fim()
                    print(p)

        elif (escolha == 3):
            os.system('cls')
            name = input('Informe o nome do cliente: ')
            cpf = float(eval(input('Informe o cpf do cliente: ')))


            autname = db.child('devloide/clientes').child(name).child('usuario').get(user['idToken'])
            autcpf = db.child('devloide/clientes').child(name).child('cpf').get(user['idToken'])
            if (name == autname.val()) and (cpf == autcpf.val()):
             os.system('cls')
             certeza = input("Voce tem certeza que deseja remover o cliente {} portador do cpf {}? S - sim / N - nao".format(name, cpf))
             if (certeza == 'S'):
                db.child('devloide/clientes').child(name).remove(user['idToken'])
                os.system('cls')
                print('Cliente excluido com sucesso!')
                print ('1 - Menu Completo')
                print ('2 - Encerrar  sessao')
                op = int(eval(input("")))
                if op == 1:
                    p = menu(nome, code)
                    print(p)
                elif op == 2:
                    p = fim()
                    print(p)
             elif (certeza == 'N'):
                 os.system('cls')
                 print ('1 - Menu Completo')
                 print ('2 - Encerrar  sessao')
                 op = int(eval(input("")))
                 if op == 1:
                     p = menu(nome, code)
                     print(p)
                 elif op == 2:
                     p = fim()
                     print(p)
            else:
                print(("Cliente {} nao existe!".format(name)))
                print ('1 - Menu Completo')
                print ('2 - Encerrar  sessao')
                op = int(eval(input("")))
                if op == 1:
                    p = menu(nome, code)
                    print(p)
                elif op == 2:
                    p = fim()
                    print(p)
        elif (escolha==4):
            z = fim()
            print(z)
    else:
        print("Verifique suas credenciais!")



#AUTENTICACAO CRIAR GERENTE E LOGAR
print ('Acesso Restrito - Acesso apenas do Gerente Chefe')
nome = input('Usuario: ')
code = int(eval(input('ID: ')))

x = menu(nome,code)
print(x)

