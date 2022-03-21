import os
import json
import music21 as m21
import numpy as np
import tensorflow.keras as keras

VIVALDI_DATASET_PATH = "soundtracks/vivaldi_op8"
FOLK_DATASET_PATH = "soundtracks/deutschl/erk"
DEBUSSY_DATASET_PATH = "soundtracks/debussy_et_al"

CLASSICAL_SAVE_PATH = "dataset/classical"
FOLK_SAVE_PATH = "dataset/folk"
DEBUSSY_SAVE_PATH = "dataset/debussy_et_al"

CLASSICAL_SINGLE_FILE = "dataset/classical/combined"
FOLK_SINGLE_FILE = "dataset/folk/combined"

CLASSICAL_MAPPING = "dataset/classical/mapping.json"
FOLK_MAPPING = "dataset/folk/mapping.json"

DEBUSSY_SINGLE_FILE = "dataset/debussy_et_al/combined"
DEBUSSY_MAPPING = "dataset/debussy_et_al/mapping.json"
SEQUENCE_LENGTH = 64

ACCEPTED_DURATIONS = [
    0.25, # sixteenth note
    0.5,  # eigth note
    0.75, # dotted eight note - adds half the value of note to itself
    1,    # quarter note
    1.5,  # dotted quarter note - adds half the value of note to itself
    2,    # half note
    3,    # 3 quarter notes - needed for 3/4 time signatures
    4     # whole note
]

def load_songs(data_path, str):

    songs = []

    # iterate through songs and load with music21
    for path, subdirs, files in os.walk(data_path):
        for file in files:
            if file[-3:] == str:
                song = m21.converter.parse(os.path.join(path, file))
                songs.append(song)
    return songs


def acceptable_note_durations(song, accepted_durations):
    for note in song.flat.notesAndRests:
        if note.duration.quarterLength not in accepted_durations:
            return False
    return True


# transposing so that the model does not have to learn all possible 24 keys
# essentially we are simplifying our input data to 2 keys which will allow us 
# to use less data for training

def transpose_key(song):
    # get key from the song file
    parts = song.getElementsByClass(m21.stream.Part)
    measures_in_start = parts[0].getElementsByClass(m21.stream.Measure)
    key = measures_in_start[0][4]

    # if key info not in file, estimate key using music21
    if not isinstance(key, m21.key.Key):
        key = song.analyze("key")

    # get interval for transposition e.g. Bmaj -> Cmaj (distance between tonic B and tonic C)
    if key.mode == "major":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
    elif key.mode == "minor":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

    # transpose the song by the calculated interval using music21
    transposed_song = song.transpose(interval)

    return transposed_song


def encode_to_timeseries(song, time_step = 0.25):
    # in timeseries each note has pitch followed by duration in terms of 16th note
    # eg 1 quarter note = 4 sixteenth notes = need to hold pitch for 3 more 16th note duration 
    # pitch = 60, duration = 1.0 -> [60, "_", "_", "_"]

    timeseries_song = []

    for obj in song.flat.notesAndRests:

        # handle the notes
        if isinstance(obj, m21.note.Note):
            symbol = obj.pitch.midi
        # handle the rests
        elif isinstance(obj, m21.note.Rest):
            symbol = "r"
        
        # convert to timeseries
        samples = int(obj.duration.quarterLength/ time_step)
        for sample in range(samples):
            if sample == 0:
                timeseries_song.append(symbol)
            else:
                timeseries_song.append("_")
    
    # cast timeseries list to a string
    timeseries_song = " ".join(map(str, timeseries_song))
    return timeseries_song


def preprocess(data_path, save_path, music_file_type):
    pass

    # load songs
    print("Loading songs...")
    songs = load_songs(data_path, music_file_type)
    print(f"Loaded {len(songs)} songs.")
        
    for index, song in enumerate(songs):

        # filter out songs that have non-acceptable note durations
        if not acceptable_note_durations(song, ACCEPTED_DURATIONS):
            continue

        # transpose to Cmaj/Amin 
        song = transpose_key(song)

        # encode songs with music time series representation
        timeseries_song = encode_to_timeseries(song)

        # save songs to text file
        save_file = os.path.join(save_path, str(index))
        with open(save_file, "w") as fp:
            fp.write(timeseries_song)


def load(file_path):
    with open(file_path, "r") as fp:
        song = fp.read()
    return song


def generate_single_file_dataset(dataset_path, single_file_path, sequence_length):
    new_song_delimiter = "/ " * sequence_length
    songs = ""

    # load timeseries files and add delimiters
    for path, _, files in os.walk(dataset_path):
        for file in files:
            file_path = os.path.join(path, file)
            song = load(file_path)
            songs = songs + song + " " + new_song_delimiter
    songs = songs[:-1]

    # save the string that contains the entire data set
    with open(single_file_path, "w") as fp:
        fp.write(songs)
    
    return songs


def create_dictionary(songs, mapping_path):
    dictionary = {}

    # identify look up table definitions
    songs = songs.split()
    definition = list(set(songs))

    # create look up table
    for i, symbol in enumerate(definition):
        dictionary[symbol] = i

    # save definitions to a json file
    with open(mapping_path, "w") as fp:
        json.dump(dictionary, fp, indent=4)


def convert_songs_to_ints(songs, mapping_path):
    int_songs = []

    # load the dictionary from the json file
    with open(mapping_path, "r") as fp:
        dictionary = json.load(fp)

    # cast songs string to a list
    songs = songs.split()

    # map songs list to ints
    for symbol in songs:
        int_songs.append(dictionary[symbol])
    
    return int_songs


def generate_training_sequences(sequence_length, single_file_path, json_path):
    # ex.
    # [11, 12, 13, 14, ...] -> i: [11, 12], t: 13, i: [12, 13], t: 14 ... 

    # load songs and map them to int
    songs = load(single_file_path)
    int_songs = convert_songs_to_ints(songs, json_path)
    print(type(int_songs[0]))
    print(type(sequence_length))

    # generate the training sequences
    # ex.
    # 100 symbol dataset, 64 sl, 100 - 64 = 36
    inputs = []
    targets = []

    num_sequences = len(int_songs) - sequence_length
    for i in range(num_sequences):
        inputs.append(int_songs[i:i+sequence_length])
        targets.append(int_songs[i+sequence_length])

    # one-hot encode the sequences
    # inputs: (# of seq, seq length, vocabulary size)
    vocabulary_size = len(set(int_songs))
    inputs = keras.utils.to_categorical(inputs, num_classes=vocabulary_size)
    targets = np.array(targets)
    print(len(inputs))
    print(len(inputs[0]))
    print(len(inputs[0][0]))

    return inputs, targets


def main():
    # preprocess(VIVALDI_DATASET_PATH, CLASSICAL_SAVE_PATH, "krn")
    # classical_songs = generate_single_file_dataset(CLASSICAL_SAVE_PATH, CLASSICAL_SINGLE_FILE, SEQUENCE_LENGTH)
    # create_dictionary(classical_songs, CLASSICAL_MAPPING)
    # classical_inputs, classical_targets = generate_training_sequences(SEQUENCE_LENGTH, CLASSICAL_SINGLE_FILE, CLASSICAL_MAPPING)

    preprocess(DEBUSSY_DATASET_PATH, DEBUSSY_SAVE_PATH, "krn")
    debussy_songs = generate_single_file_dataset(DEBUSSY_SAVE_PATH, DEBUSSY_SINGLE_FILE, SEQUENCE_LENGTH)
    create_dictionary(debussy_songs, DEBUSSY_MAPPING)
    debussy_inputs, debussy_targets = generate_training_sequences(SEQUENCE_LENGTH, DEBUSSY_SINGLE_FILE, DEBUSSY_MAPPING)


    # preprocess(FOLK_DATASET_PATH, FOLK_SAVE_PATH, "krn")
    # folk_songs = generate_single_file_dataset(FOLK_SAVE_PATH, FOLK_SINGLE_FILE, SEQUENCE_LENGTH)
    # create_dictionary(folk_songs, FOLK_MAPPING)
    # folk_inputs, folk_targets = generate_training_sequences(SEQUENCE_LENGTH, FOLK_SINGLE_FILE, FOLK_MAPPING)
 

# Testing individual functions using different datasets

    # songs = load_songs(VIVALDI_DATASET_PATH, "krn")
    # print(f"Loaded {len(songs)} songs.")
    
    # for song in songs:
    #     if not acceptable_note_durations(song, ACCEPTED_DURATIONS):
    #         print("Has acceptable duration? False")
    #         continue
    #     print("Has acceptable duration? True")
       
    #     current_key = song.getElementsByClass(m21.stream.Part)[0].getElementsByClass(m21.stream.Measure)[0][4]
    #     if not isinstance(current_key, m21.key.Key):
    #         current_key = song.analyze("key")

    #     new_key = transpose_key(song).analyze("key")
        
    #     print(f"The original key of the song is {current_key}")
    #     print(f"The new key of the song is {new_key}")

if __name__ == "__main__":
    main()


        