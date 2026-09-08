# Música: Happy-Birthday.mid utilizando a track bells com 1.0 oitvava abaixo
import nxt.locator, nxt.motor
from time import sleep
import numpy as np
import usb.core

try: 
    print("Conectando ao NXT...")
    brick = nxt.locator.find()

    # Definindo quais motores são as pernas
    motor_direito = brick.get_motor(nxt.motor.Port.A)  # perna direita
    motor_esquerdo = brick.get_motor(nxt.motor.Port.B)  # perna esquerda
except:
    input("NXT não encontrado!")
    
POTENCIA = 90

print("NXT conectado!")

class methods:
    """Metodos uteis para o funcionamento do robô"""
    @staticmethod
    def pausa_usb():
        sleep(0.05)

    @staticmethod
    def brake_motores():
        """Para os dois motores de uma vez"""
        try:
            motor_direito.brake()
            methods.pausa_usb()
            
            motor_esquerdo.brake()
            methods.pausa_usb()
        except:
            pass

class dance_methods:
    """
        Metodos relacionados a dança, utilizando o BPM da musica alvo. 
        ---
        - `tempo`: Define em quantas batidas a ação deve ocorrer.
        - `note`: É a frequencia da nota.
    """
    @staticmethod
    def cantar(note,d):
        brick.play_tone(note,d)

    @staticmethod
    def right_step( segundos):
        """Passinho pra esquerda"""
        motor_direito.run(POTENCIA)
        motor_esquerdo.run(-POTENCIA)
        sleep(segundos)

    @staticmethod
    def left_step( segundos):
        """Passinho pra direita"""
        motor_direito.run(-POTENCIA)
        motor_esquerdo.run(POTENCIA)
        sleep(segundos)

    @staticmethod
    def vibration(n, segundos):
        """Faz o roblo balançar `n` vezes em `tempo` da musica. """

        t = segundos / (n*4) # Duração de cada movimento

        for _ in range(n):
            # Os dois motores pra frente
            motor_direito.run(POTENCIA)
            motor_esquerdo.run(POTENCIA)
            
            sleep(t)
            methods.brake_motores()
            sleep(t)
            
            # Os dois motores pra trás
            motor_direito.run(-POTENCIA)
            motor_esquerdo.run(-POTENCIA)
            
            sleep(t)
            methods.brake_motores()
            sleep(t)

def dance(NOTES, DURATION):
    to_right = True
    for i,N in enumerate(NOTES):
            delta = N[1]*1000/DURATION

            dance_methods.cantar(N[0],round(N[1]*100)+300)
            sleep(min(N[1],500)/1000)
            
            move = ""
            if(delta < .8):
                if to_right:
                    to_right = False
                    dance_methods.right_step(N[1])
                else:
                    to_right = True
                    dance_methods.left_step(N[1])

                move = "Dança Curta"
            elif(delta > 1.2):
                move = "Dança Longa"
                move = "Dança Normal"
                dance_methods.vibration(1,N[1])
            else:
                if to_right:
                    to_right = False
                    dance_methods.right_step(N[1]/2)
                    dance_methods.right_step(N[1]/2)
                else:
                    to_right = True
                    dance_methods.left_step(N[1]/2)
                    dance_methods.left_step(N[1]/2)

            perc = round(i/len(NOTES)*20)
            print(
                f"\r└ [{"█"*perc}{"░"*(20-perc)}]{perc*5}% - {move} ", 
                end="", 
                flush=True
            )
    

def play(NOTES : list[tuple], Duration):
    try: 
        dance(NOTES,Duration)
    except KeyboardInterrupt: 
        print("! \nShow interrompido pelo usuário.") 
    except usb.core.USBError as erro:
         print("\nErro de comunicação USB:") 
         print(erro) 
    except Exception as erro: 
        print("! \nOcorreu um erro inesperado:") 
        print(erro) 
    finally: # Garante que os motores param mesmo se der erro parar() oq isso faz?
        methods.brake_motores()
BPM = 120
D = (60/BPM)*1000

NOTES = ((988, 0.435),(988, 0.224),(1109, 0.652),(988, 0.652),(1319, 0.649),(1245, 1.308),(988, 0.431),(988, 0.217),(1109, 0.656),(988, 0.652),(1480, 0.649),(1319, 1.308),(988, 0.431),(988, 0.221),(1976, 0.652),(1661, 0.652),(1319, 0.431),(1319, 0.217),(1245, 0.652),(1109, 0.656),(1760, 0.431),(1760, 0.217),(1661, 0.652),(1319, 0.656),(1480, 0.649),(1319, 1.308),(988, 0.431),(988, 0.221),(1109, 0.649),(988, 0.656),(1319, 0.649),(1245, 1.308),(988, 0.431),(988, 0.217),(1109, 0.652),(988, 0.656),(1480, 0.649),(1319, 1.308),(988, 0.431),(988, 0.217),(1976, 0.003),(1760, 0.652),(1661, 0.652),(1319, 0.431),(1319, 0.217),(1245, 0.652),(1109, 0.656),(1760, 0.431),(1760, 0.217),(1661, 0.656),(1319, 0.652),(1480, 0.652),(1319, 1.0),)

if __name__=='__main__':
    play(NOTES,D)