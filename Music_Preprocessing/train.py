import tensorflow.keras as keras
from preprocess import generate_training_sequences, SEQUENCE_LENGTH, FOLK_SAVE_PATH,FOLK_SINGLE_FILE, FOLK_MAPPING, CLASSICAL_SINGLE_FILE, CLASSICAL_MAPPING, DEBUSSY_SINGLE_FILE, DEBUSSY_MAPPING, MIXED_SINGLE_FILE, MIXED_MAPPING
from tensorflow.keras.callbacks import ModelCheckpoint

OUTPUT_UNITS = 63
NUM_UNITS = [128]
LOSS = "sparse_categorical_crossentropy"
LEARNING_RATE = 0.001
EPOCHS = 15
BATCH_SIZE = 64
SAVE_MODEL_PATH = "mixed_model.h5"


def build_model(output_units, num_units, loss, learning_rate):
    """Builds and compiles model
    :param output_units (int): Num output units
    :param num_units (list of int): Num of units in hidden layers
    :param loss (str): Type of loss function to use
    :param learning_rate (float): Learning rate to apply
    :return model (tf model): Where the magic happens :D
    """

    # create the model architecture
    input = keras.layers.Input(shape=(None, output_units))
    x = keras.layers.LSTM(num_units[0])(input)
    x = keras.layers.Dropout(0.2)(x)

    output = keras.layers.Dense(output_units, activation="softmax")(x)

    model = keras.Model(input, output)

    # compile model
    model.compile(loss=loss,
                  optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                  metrics=["accuracy"])

    model.summary()

    return model


def train(single_file_path, json_path, output_units=OUTPUT_UNITS, num_units=NUM_UNITS, loss=LOSS, learning_rate=LEARNING_RATE):
    """Train and save TF model.
    :param output_units (int): Num output units
    :param num_units (list of int): Num of units in hidden layers
    :param loss (str): Type of loss function to use
    :param learning_rate (float): Learning rate to apply
    """

    # generate the training sequences
    inputs, targets = generate_training_sequences(SEQUENCE_LENGTH, single_file_path, json_path)

    # build the network
    model = build_model(output_units, num_units, loss, learning_rate)

    # train the model
    filepath="{epoch:02d}-{accuracy:.2f}-"+SAVE_MODEL_PATH
    checkpoint = ModelCheckpoint(filepath, monitor='accuracy', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]

    model.fit(inputs, targets, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=callbacks_list)

    # save the model
    model.save(SAVE_MODEL_PATH)


if __name__ == "__main__":
    train(MIXED_SINGLE_FILE, MIXED_MAPPING)