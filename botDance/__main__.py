import src.midi_converter as midi_converter
import src.midi_explorer as midi_explorer
from src.constants import *
from os import path,name, mkdir
import subprocess
import mido

nbc_path = path.join(
    NXT_DIR,
    "nbc-compiler",
    "NXT",
    "nbc"
)

while True:
    response = midi_explorer.menu()

    if response['action'] == 'exit':
        break

    match response['action']:
        case 'dance':
            try:
                python_file = path.join(
                    response['path'],
                    path.basename(response['path']) + '.py'
                )
                subprocess.run(["python",python_file])
            except KeyboardInterrupt:
                print("! \nExecução interrompida.")

        case 'create':
            file_name = path.basename(response['path'])
            midi_file = mido.MidiFile(response['path'])

            create_response = midi_explorer.create_menu(midi_file,file_name)
            track_choiced = create_response['track_choiced']
            pitch_choiced = create_response['pitch_choiced']
            midi_map = create_response['midi_map']

            formated_file_name = file_name.split('.')[0].replace(' ','-')
            dance_sequence = midi_converter.trackToProgram(
                midi_file.tracks[midi_map[track_choiced]],
                midi_file.ticks_per_beat,
                create_response['BPM'],
                create_response['TEMPO'],
                pitch_choiced,
                formated_file_name if len(formated_file_name) < 12 else formated_file_name[:12],
                create_response['lite_ver']
            )

            folder_path = path.join(PATH_DANCES,formated_file_name)

            if not(path.exists(folder_path)):
                mkdir(folder_path)

            with open(path.join(folder_path,f'{formated_file_name}.py'),'w',encoding="utf-8") as script:
                pitch_choiced_comment = f"com {abs(pitch_choiced)} oitvava {"abaixo" if pitch_choiced < 0 else "acima"}"
                comment = f"# Música: {file_name} utilizando a track {track_choiced} {pitch_choiced_comment if pitch_choiced != 0 else ""}\n"
                script.write(comment+dance_sequence['python'])
                script.close()

            with open(path.join(folder_path,f'{formated_file_name}.nxc'),'w',encoding="utf-8") as script:
                pitch_choiced_comment = f"com {abs(pitch_choiced)} oitvava {"abaixo" if pitch_choiced < 0 else "acima"}"
                comment = f"// Música: {file_name} utilizando a track {track_choiced} {pitch_choiced_comment if pitch_choiced != 0 else ""}\n"
                script.write(comment+dance_sequence['nxc'])
                script.close()

                output_path = path.join(folder_path,f'{formated_file_name}.rxe')
                input_path = path.join(folder_path,f'{formated_file_name}.nxc')
                subprocess.run([
                    nbc_path, 
                    f'-O={output_path}', 
                    input_path
                ],check=True)

            input(f"└   └ Dança {file_name} usando a track {track_choiced} com pitch {pitch_choiced} criada com sucesso!")