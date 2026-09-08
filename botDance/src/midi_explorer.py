from typing import Literal, TypedDict
from src.constants import *
from mido import tempo2bpm
import subprocess
import os

POSITIVE = ["sim","s","1","y","yes"]
NEGATIVE = ["nao","n","0","não","no",""," "]

class menu_response(TypedDict):
    action: Literal['dance','create','exit']
    path: str

def dances_options() -> list[str]:
    """Retorna as atuais opções de dança na pasta `dances`"""
    dances_options = []
    for child in os.listdir(PATH_DANCES):
        try:
            # Guarda em `dances_options` as opções validas de dança
            file_name = os.path.basename(child)
            if not file_name == "dance_constant":
                dances_options.append(f"{file_name}")
        except ValueError:
            pass # Acessou alguma pasta, oque não é uma oção de dança

    return dances_options


def midi_options() -> list[str]:
    """Retorna as atuais opções de midi na pasta `musics`"""
    midi_options = []
    for child in os.listdir(PATH_MUSICS):
        try:
            # Guarda em `dances_options` as opções validas de dança
            file_name, extension = os.path.basename(child).split(".")
            if extension in ["mid","midi"]:
                midi_options.append(f"{file_name}")
        except ValueError:
            pass # Acessou alguma pasta, oque não é uma oção de dança

    return midi_options


def menu() -> menu_response:
    response : menu_response = {}
    while True:
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
        print("""
————————————————————————————————————————————————
·▄▄▄▄   ▄▄▄·  ▐ ▄  ▄▄· ▄▄▄ .    ▄▄▄▄·       ▄▄▄▄▄    
██▪ ██ ▐█ ▀█ •█▌▐█▐█ ▌▪▀▄.▀·    ▐█ ▀█▪▪     •██      
▐█· ▐█▌▄█▀▀█ ▐█▐▐▌██ ▄▄▐▀▀▪▄    ▐█▀▀█▄ ▄█▀▄  ▐█.▪    
██. ██ ▐█ ▪▐▌██▐█▌▐███▌▐█▄▄▌    ██▄▪▐█▐█▌.▐▌ ▐█▌·    
▀▀▀▀▀•  ▀  ▀ ▀▀ █▪·▀▀▀  ▀▀▀     ·▀▀▀▀  ▀█▄▀▪ ▀▀▀       
————————————————————————————————————————————————                           
sair : sair do programa
criar : cria um novo script de dança apartir de um MIDI armazenado em `musics`
dançar : faça o robô dançar e cantar uma musica:    """
)

        print("————————————————————————————————————————————————")
        input_menu = input("┌ Informe a ação desejada ❯ ").split(" ")

        if len(input_menu) > 0:
            match input_menu[0]:
                case "sair":
                    response['action'] = "exit"
                    response['path'] = ""
                    print("└ Saindo...")
                    return response
                
                case "dançar":
                    while True:

                        print("├ Opções de dança: ")

                        dances_options_list = dances_options()

                        print("│ 0: Sair dessa tela")
                        for i,dance in enumerate(dances_options_list):
                            print(f"│ {i+1}: {dance}")

                        input_dance = input("├ Informe a dança desejada ❯ ").split(" ")

                        if len(input_dance) > 0:
                            if input_dance[0] == "0":
                                break
                            else:
                                try:
                                    choice = dances_options_list[int(input_dance[0])-1]
                                    response['action'] = 'dance'
                                    response['path'] = os.path.join(PATH_DANCES,choice+'.py')
                                    print("│\n├ Iniciando Dança!\n│")
                                    return response
                                except:
                                    print("│\n│ Valor informado inválido!\n│")

                case "criar":
                    while True:
                        print("├ Opções de musicas: ")

                        midi_options_list = midi_options()

                        print("│ 0: Sair dessa tela")
                        for i,midi in enumerate(midi_options_list):
                            print(f"│ {i+1}: {midi}")

                        input_create = input("├ Informe a musica desejada ❯ ").split(" ")

                        if len(input_create) > 0:
                            if input_create[0] == "0":
                                break
                            else:
                                try:
                                    choice = midi_options_list[int(input_create[0])-1]
                                    response['action'] = 'create'
                                    response['path'] = os.path.join(PATH_MUSICS,choice+'.mid')

                                    if not(os.path.exists(response['path'])):
                                        response['path'] = os.path.join(PATH_MUSICS,choice+'.midi')

                                    print("│\n├ Iniciando Criação!\n│")
                                    return response
                                except:
                                    print("│\n│ Valor informado inválido!\n│")

class create_response(TypedDict):
    BPM: int
    track_choiced: str
    pitch_choiced : float
    TEMPO: int
    lite_ver : bool

    midi_map : list[str]

def create_menu(midi_file, file_name) -> create_response:
    midi_map = {}
    TEMPO = 500_000
    BPM = round(tempo2bpm(TEMPO if TEMPO else 500_000))
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == "set_tempo":
                TEMPO = msg.tempo

        midi_map[track.name.strip().lower()] = len(list(midi_map.keys()))

    track_choiced = ""
    pitch_choiced = 0.0

    while True:
        tracks_names = list(midi_map.keys())
        print(f"├ Dados da Musica {file_name}:")
        print(f"│   ├ Tempo: {TEMPO}")
        print(f"│   ├ BPM: {BPM}")
        print(f"│   ├ Tracks: {len(midi_file.tracks)}")

        for i,key in enumerate(tracks_names): 
            if i == len(tracks_names) - 1:
                print(f"│   │   └ '{i} : {key}' - Notas: {len(midi_file.tracks[i])}")
            else:
                print(f"│   │   ├ '{i} : {key}' - Notas: {len(midi_file.tracks[i])}")

        track_choiced = input("│   ├ Informe a track desejada (Recomendo escolher o instrumento da melodia): ")

        try:
            track_choiced = tracks_names[int(track_choiced)]
            break
        except:
            print("│   │\n│   ├ Informe uma track válida!\n│   │")
            continue

    while True:
        pitch_choiced = input("│   ├ Informe (caso queira) a mudança de oitava: ")
        if pitch_choiced in NEGATIVE:
            pitch_choiced = 0.0
            break
        else:
            try:
                pitch_choiced = float(pitch_choiced)
                break
            except:
                print("│   │\n│   ├ Informe um mudança de pitch válida!\n│   │")

    while True:
        lite_ver = input("│   ├ Deseja um nxc mais leve (Robô não terá rosto): ")
        if lite_ver in POSITIVE:
            lite_ver = True
            break
        elif lite_ver in NEGATIVE:
            lite_ver = False
            break             
        else:
            print("│   │\n│   ├ Informe uma resposta valida! \n│   │")

    return {
        'BPM': BPM,
        'track_choiced': track_choiced,
        'TEMPO': TEMPO,
        'pitch_choiced': pitch_choiced,
        'lite_ver': lite_ver,
        'midi_map': midi_map
    }