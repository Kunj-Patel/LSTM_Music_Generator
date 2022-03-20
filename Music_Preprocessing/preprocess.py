from json import load
import os
import music21 as m21

VIVALDI_DATASET_PATH = "C:/Users/sendt/Documents/Year_4/MTE 546/Project/Music_Preprocessing/soundtracks/vivaldi_op8"
FOLK_DATASET_PATH = "C:/Users/sendt/Documents/Year_4/MTE 546/Project/Music_Preprocessing/soundtracks/deutschl/test"

VIVALDI_SAVE_PATH = "C:/Users/sendt/Documents/Year_4/MTE 546/Project/Music_Preprocessing/dataset/vivaldi"
FOLK_SAVE_PATH = "C:/Users/sendt/Documents/Year_4/MTE 546/Project/Music_Preprocessing/dataset/folk"

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

    # load pokemon songs
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


if __name__ == "__main__":
    preprocess(FOLK_DATASET_PATH, FOLK_SAVE_PATH, "krn")


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

        