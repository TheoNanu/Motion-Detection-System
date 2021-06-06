from keras import models, layers, optimizers
from matplotlib import pyplot as plt
import numpy as np

from classifier_generator import ClassifierGenerator


class KerasNeuralNet(ClassifierGenerator):
    def __init__(self, dataset: str, neurons: list):
        super().__init__(dataset=dataset)
        self.neurons = neurons
        self.layers = len(self.neurons)
        self.history = None

        self.outputModel = models.Sequential()
        for i in range(len(self.neurons)):
            if i == 0:
                self.outputModel.add(layers.Dense(self.neurons[i], activation='selu',
                                                  input_shape=(self.numberOfFeatures,)))
            elif i == len(self.neurons) - 1:
                if self.neurons[i] > 1:
                    self.outputModel.add(layers.Dense(self.neurons[i], activation='softmax'))
                else:
                    self.outputModel.add(layers.Dense(self.neurons[i], activation='sigmoid'))
            else:
                self.outputModel.add(layers.Dense(self.neurons[i], activation='selu'))
                self.outputModel.add(layers.Dropout(0.5))

        # initial_learning_rate = 0.1
        # lr_schedule = optimizers.schedules.ExponentialDecay(
        #     initial_learning_rate,
        #     decay_steps=100000,
        #     decay_rate=0.96,
        #     staircase=True
        # )

        print(self.outputModel.summary())

        self.outputModel.compile(optimizer=optimizers.Adam(learning_rate=0.001),
                                 loss='binary_crossentropy', metrics=['accuracy'])

    def train(self, epochs, batch_size):
        # early_stopping = callbacks.EarlyStopping(monitor='val_loss', patience=20)
        self.history = self.outputModel.fit(self.trainFeatures, self.trainLabels, epochs=epochs, batch_size=batch_size,
                                            validation_data=(self.valFeatures, self.valLabels))

    def predict(self):
        pred = self.outputModel.predict(np.array([[0.30, 0.09, 0.89, 0.28, 0.00, 0.99, 0.56, 1.00]]))
        print("Prediction: " + str(pred))

    def plot_learning_curves(self):
        history_dict = self.history.history

        loss_values = history_dict['loss']
        val_loss_values = history_dict['val_loss']

        acc = history_dict['accuracy']
        val_acc = history_dict['val_accuracy']

        epochs = range(1, len(acc) + 1)

        plt.plot(epochs, loss_values, 'r', label='Training loss')
        plt.plot(epochs, val_loss_values, 'b', label='Validation loss')

        plt.title('Training and validation loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')

        plt.legend()
        plt.show()

        plt.plot(epochs, acc, 'r', label='Training accuracy')
        plt.plot(epochs, val_acc, 'b', label='Validation accuracy')

        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')

        plt.legend()
        plt.show()


if __name__ == '__main__':
    net = KerasNeuralNet('datasets/features_processed.csv', [8, 12, 12, 6, 1])

    net.train(1000, 512)
    net.predict()
    net.plot_learning_curves()
    net.generate('ESP_NN')
