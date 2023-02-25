import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import argparse

DATA_DIR = os.environ["SM_CHANNEL_FLOWERS"]
OUTPUT_DIR = os.environ["SM_MODEL_DIR"]
HPS = os.environ["SM_HPS"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_size", type=int)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--validation_split", type=float, default=0.2)
    parser.add_argument("--epochs", type=int, default=2)
    args, _ = parser.parse_known_args()
    return args


def train():
    args = parse_args()
    IMG_SIZE = (args.image_size, args.image_size)
    BATCH_SIZE = args.batch_size
    VALIDATION_SPLIT = args.validation_split
    EPOCHS = args.epochs

    image_gen = ImageDataGenerator(rescale=1.0 / 255, validation_split=VALIDATION_SPLIT)

    train_data_gen = image_gen.flow_from_directory(
        batch_size=BATCH_SIZE,
        directory=DATA_DIR,
        subset="training",
        shuffle=True,
        target_size=IMG_SIZE,
        class_mode="sparse",
    )

    test_data_gen = image_gen.flow_from_directory(
        batch_size=BATCH_SIZE,
        directory=DATA_DIR,
        subset="validation",
        target_size=IMG_SIZE,
        class_mode="sparse",
    )

    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Conv2D(
                32, (3, 3), activation="relu", input_shape=(*IMG_SIZE, 3)
            ),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(6),
        ]
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr=1e-4),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    model.fit(train_data_gen, epochs=EPOCHS)
    test_loss, test_accuracy = model.evaluate(test_data_gen)
    print(f"Test accuracy: {test_accuracy}")

    model.save(OUTPUT_DIR + "/model.h5")


if __name__ == "__main__":
    train()
