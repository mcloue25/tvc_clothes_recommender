# save the final model to file
# import tensorflow as tf
# from keras.datasets import fashion_mnist
# from keras.utils import to_categorical
# from keras.models import Sequential
# from keras.layers import Conv2D
# from keras.layers import MaxPooling2D
# from keras.layers import Dense
# from keras.layers import Flatten
# from keras.optimizers import SGD

'''
    https://machinelearningmastery.com/how-to-develop-a-cnn-from-scratch-for-fashion-mnist-clothing-classification/
'''

# # load train and test dataset
# def load_dataset():
#     # load dataset
#     (trainX, trainY), (testX, testY) = fashion_mnist.load_data()
#     # reshape dataset to have a single channel
#     trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
#     testX = testX.reshape((testX.shape[0], 28, 28, 1))
#     # one hot encode target values
#     trainY = to_categorical(trainY)
#     testY = to_categorical(testY)
#     return trainX, trainY, testX, testY
 
# # scale pixels
# def prep_pixels(train, test):
#     # convert from integers to floats
#     train_norm = train.astype('float32')
#     test_norm = test.astype('float32')
#     # normalize to range 0-1
#     train_norm = train_norm / 255.0
#     test_norm = test_norm / 255.0
#     # return normalized images
#     return train_norm, test_norm


# # define cnn model
# def define_model():
#     model = Sequential()
#     model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
#     model.add(MaxPooling2D((2, 2)))
#     model.add(Flatten())
#     model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
#     model.add(Dense(10, activation='softmax'))
#     # compile model
#     opt = SGD(lr=0.01, momentum=0.9)
#     model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
#     return model





# def tf_fashion_mnist_model():
#     fashion_mnist = tf.keras.datasets.fashion_mnist

#     (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
#     class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
#     train_images = train_images / 255.0
#     test_images = test_images / 255.0

#     model = tf.keras.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(10)])

#     model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
#     model.fit(train_images, train_labels, epochs=10)
#     test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
#     print('\nTest accuracy:', test_acc)
#     model.save('saved_model/clothes_detection_model_tf_example')


# def clothes_detection_main():
#     '''
#     '''

#     tf_fashion_mnist_model()
#     a-b

#     # load & prepare dataset
#     trainX, trainY, testX, testY = load_dataset()
#     trainX, testX = prep_pixels(trainX, testX)
#     # define model
#     model = define_model()
    
#     # Fit & save model
#     model.fit(trainX, trainY, epochs=10, batch_size=32, verbose=0)
#     model.save('saved_model/clothes_detection_model')


# if __name__ == "__main__":
#     clothes_detection_main()



# TensorFlow and tf.keras
import tensorflow as tf
import cv2
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt


def plot_image_mine(image):
    ''' Used for plotting images using cv2
    '''

    print()
    print()
    print(image.shape)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    return


class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

def tensorflow_clothes_detection_setup():
    '''
    '''
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    train_images = train_images / 255.0

    test_images = test_images / 255.0

    print(train_images[0].shape)
    print()
    print(train_images[0])
    plot_image_mine(train_images[0])
    a-b
    plt.figure(figsize=(10,10))
    for i in range(25):
        plt.subplot(5,5,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(train_images[i], cmap=plt.cm.binary)
        plt.xlabel(class_names[train_labels[i]])
    plt.show()


    model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)])


    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=10)
    model.save('saved_model/clothes_detection_model')
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

    print('\nTest accuracy:', test_acc)

    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    predictions = probability_model.predict(test_images)




    # Plot the first X test images, their predicted labels, and the true labels.
    # Color correct predictions in blue and incorrect predictions in red.
    num_rows = 5
    num_cols = 3
    num_images = num_rows*num_cols
    plt.figure(figsize=(2*2*num_cols, 2*num_rows))
    for i in range(num_images):
        plt.subplot(num_rows, 2*num_cols, 2*i+1)
        plot_image(i, predictions[i], test_labels, test_images)
        plt.subplot(num_rows, 2*num_cols, 2*i+2)
        plot_value_array(i, predictions[i], test_labels)
    plt.tight_layout()
    plt.show()



def plot_image(i, predictions_array, true_label, img):
    true_label, img = true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label], 100*np.max(predictions_array), class_names[true_label]), color=color)


def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')



def clothes_detection_main():
    ''' NNED TO DUAL BOOT PC TO GET FULL USE OF GPU'S
    '''
    # print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    # https://www.tensorflow.org/tutorials/keras/classification
    # tf.config.list_physical_devices('GPU')
    # a-b
    tensorflow_clothes_detection_setup()
    a-b

    # load & prepare dataset
    trainX, trainY, testX, testY = load_dataset()
    trainX, testX = prep_pixels(trainX, testX)
    # define model
    model = define_model()
    
    # Fit & save model
    model.fit(trainX, trainY, epochs=10, batch_size=32, verbose=0)
    model.save('saved_model/clothes_detection_model')


if __name__ == "__main__":
    clothes_detection_main()