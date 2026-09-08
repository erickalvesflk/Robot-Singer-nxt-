from src.constants import *
from typing import TypedDict
from os import path
import mido

class Program(TypedDict):
    python: str
    nxc: str

def noteToFrequency(note : int) -> int:
    """
    Transforma uma nota (de um teclado de 88 teclas) para Frequencia
    """
    return round(440 * 2**((note-49)/12))

def getNotes(track, TPS : int, tempo : int, pitch :int):
    """
    Transforma todas as notas e seus respectivos ticks para um frquencia e sua duração
    """
    notes = []
    current_tick = 0

    for msg in track:
        current_tick += msg.time

        if msg.type == "note_on" and msg.velocity > 0:
            notes.append({
                "note": noteToFrequency(msg.note + 12 * pitch),
                "tick": current_tick
            })

    # duração = distância até a próxima nota
    for i in range(len(notes) - 1):
        ticks = notes[i + 1]["tick"] - notes[i]["tick"]
        notes[i]["d"] = round(mido.tick2second( ticks, TPS, tempo) * 1000)

    # última nota não tem próxima nota para comparar
    if notes:
        notes[-1]["d"] = 1000

    # remove campo auxiliar
    for note in notes:
        del note["tick"]

    return notes

def trackToProgram(track, TPS : int, BPM: int, tempo=500_000, pitch=0.0, music_name="", lite_ver=False) -> Program:
    """
    Transforma uma track de um arquivo MIDI, para um algoritimo em python e em nxc.
    ---
    - `track`: Faixa da música utilizada (normalmente o instrumento). Recomendado ser a _melodia_
    - `TPS`: ticks por segundo, arquivos MIDIs não leem a duração, eles leem o intervalo entre comandos
    - `BPM`: Batidas por minuto, a BPM da música
    - `tempo`: tempo de batida de 1/4 do compasso
    - `pitch`: Diferença da oitava atual para a desejada. Aumente caso queira deixar mais fino ou Diminua para
    """

    NOTES = getNotes(track, TPS, tempo, pitch)

    command = ""
    with open(path.join(PATH_TEMPLATES,'dance_constant.py'),'r') as dance_constants:
        command += dance_constants.read()
        dance_constants.close()

    command += '\n'
    command += f"BPM = {BPM}"
    command += "\nD = (60/BPM)*1000\n\nNOTES = ("

    for NOTE in NOTES:
        command += f"{NOTE['note'], NOTE['d']/1000},"

    command+=f")\n\nif __name__=='__main__':\n    play(NOTES,D)"

    with open(path.join(PATH_TEMPLATES,'dance_constant.nxc' if not lite_ver else 'dance_constant_lite.nxc'),'r') as nxc_template:
        nxc_template_content = nxc_template.read()
        nxc_template.close()

        nxc_template_content = nxc_template_content.replace('{%BPM%}',f'{BPM}')
        nxc_template_content = nxc_template_content.replace('{%D%}',f'{round((60.0/BPM)*1000,2)}')
        nxc_template_content = nxc_template_content.replace('{%NAME%}',f'{music_name}')

        notes_in_nxc = ""
        for i,note in enumerate(NOTES):
            notes_in_nxc += f"{{ {note['note']},{note['d']} }}{'' if i == len(NOTES)-1 else ','}"
            if i > 0 and i%10 == 0:
                notes_in_nxc+='\n    '

        nxc_template_content = nxc_template_content.replace('{%NOTES%}',notes_in_nxc)
    
    return {
        'python': command,
        'nxc': nxc_template_content
    }