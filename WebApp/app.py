from flask import Flask, render_template, request, jsonify, redirect
import sys
import time
sys.path.append('../Music_Preprocessing')
from melodygenerator import MelodyGenerator
from preprocess import SEQUENCE_LENGTH, FOLK_MAPPING, CLASSICAL_SINGLE_FILE, CLASSICAL_MAPPING, DEBUSSY_SINGLE_FILE, DEBUSSY_MAPPING, CLASSICAL_SINGLE_FILE, CLASSICAL_MAPPING, MIXED_MAPPING

app = Flask(__name__)
music_type_mapping = {'folk': FOLK_MAPPING, 'classical':CLASSICAL_MAPPING, 'debussy':DEBUSSY_MAPPING, 'mixed':MIXED_MAPPING}
model_path_mapping = {'folk': "folk_music_model.h5", 'classical':"classical_music_model.h5", 'debussy':"debussy_et_al_model.h5", 'mixed':"mixed_model.h5"}


def current_milli_time():
    return round(time.time() * 1000)

@app.route('/')
def index():
    return render_template('index.html')

# GET requests will be blocked
@app.route('/create-melody', methods=['POST'])
def create_melody():
    temperature = float(request.form['temperature'])
    initial_seed = request.form['Initial Seed']
    music_type = request.form['music-type']
    num_steps = int(request.form['number-steps'])
    music_mapping = music_type_mapping[music_type]
    music_model_path = model_path_mapping[music_type]
    print("init seed = " + initial_seed)
    print(music_mapping)
    print(music_model_path)
    print(num_steps)

    mg = MelodyGenerator(mapping='../Music_Preprocessing/'+music_mapping, model_path='../Music_Preprocessing/'+music_model_path)
    melody = mg.generate_melody(initial_seed, num_steps, SEQUENCE_LENGTH, temperature)
    print("generated melody", melody)
    mg.save_melody(melody, file_name="static/saved_songs/"+ str(current_milli_time())+"-temp-"+ str(temperature) +"-seed-" + initial_seed + "-"+ music_type + "-mel.mid")
    mg.save_melody(melody, file_name="static/mel.mid")

    return redirect('/')
