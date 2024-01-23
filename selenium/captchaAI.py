from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import to_categorical
from keras.preprocessing import image
from sklearn.model_selection import train_test_split
import numpy as np
import os

# Assuming you have a dataset of captcha images in the 'captcha_images' directory
captcha_dir = 'temp'

# Load captcha images and labels
captcha_images = []
captcha_labels = []

for filename in os.listdir(captcha_dir):
    if filename.endswith(".png"):
        img_path = os.path.join(captcha_dir, filename)
        img = image.load_img(img_path, color_mode='grayscale', target_size=(50, 200))
        img_array = image.img_to_array(img)
        captcha_images.append(img_array)
        captcha_labels.append(filename[:-4])  # Assuming the label is the filename without the extension

# Convert to numpy arrays
captcha_images = np.array(captcha_images)
captcha_labels = np.array(captcha_labels)

# Preprocess the images
captcha_images = captcha_images / 255.0

# Convert labels to one-hot encoding
captcha_labels_onehot = to_categorical(captcha_labels)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    captcha_images, captcha_labels_onehot, test_size=0.2, random_state=42
)

# Build a simple convolutional neural network (CNN)
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(50, 200, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))  # Assuming there are 10 possible characters

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(X_test, y_test)
print('Test accuracy:', test_acc)
