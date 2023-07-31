import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tqdm import tqdm

# Загрузка данных из файла разметки
data_file = "mod_images_list.txt"

with open(data_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

image_paths = []
text_labels = []

for line in lines:
    image_path, label = line.strip().split("    ")
    image_paths.append(image_path)
    text_labels.append(label)

# Загрузка изображений и их преобразование в числовой формат
images = []
for image_path in tqdm(image_paths, desc="Loading Images", unit="image"):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(128, 128))
    image = tf.keras.preprocessing.image.img_to_array(image)
    images.append(image)

images = np.array(images)

# Создание автокодировщика
input_shape = images[0].shape
encoder_input = layers.Input(shape=input_shape)

# Слои для сжатия изображения
x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(encoder_input)
x = layers.MaxPooling2D((2, 2), padding='same')(x)
x = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(x)
encoded = layers.MaxPooling2D((2, 2), padding='same')(x)

# Слои для раскодирования изображения
x = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(encoded)
x = layers.UpSampling2D((2, 2))(x)
x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = layers.UpSampling2D((2, 2))(x)
decoded = layers.Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

autoencoder = models.Model(encoder_input, decoded)
autoencoder.compile(optimizer='adam', loss='mse')

# Обучение автокодировщика
autoencoder.fit(images, images, epochs=50, batch_size=32, validation_split=0.2)

# Сохранение модели
autoencoder.save("autoencoder_model.keras")
