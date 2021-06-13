from keras import models
from keras import layers
from keras import callbacks
from keras import backend
from keras import optimizers
import numpy as np
import tensorflow as tf
import random
import matplotlib.pyplot as plt

from classifier_generator import ClassifierGenerator
from exceptions.invalid_layers import InvalidLayersNumber
from exceptions.invalid_neurons import InvalidNeuronsNumber
from exceptions.invalid_structure import InvalidNeuralNetStructure
from genetic_algorithm import GeneticAlgorithm


class GeneticAlgorithmNetworkOptimizer(ClassifierGenerator, GeneticAlgorithm):
    def __init__(self, dataset_file, min_layers, max_layers, min_neurons, max_neurons, population_size=12, epochs=20,
                 mutation_rate=0.05):
        super().__init__(dataset=dataset_file)

        if min_layers < 1:
            raise InvalidLayersNumber

        if min_neurons < 1:
            raise InvalidNeuronsNumber

        if min_layers > max_layers:
            raise InvalidNeuralNetStructure

        if min_neurons > max_neurons:
            raise InvalidNeuralNetStructure

        self.epochs = epochs
        self.populationSize = population_size
        self.mutationRate = mutation_rate
        self.verbose = None

        self.minLayers = min_layers
        self.maxLayers = max_layers
        self.minNeurons = min_neurons
        self.maxNeurons = max_neurons
        self.population = []
        self.nextPopulation = []
        self.scores = []
        self.ordered = []
        self.plotted = True
        self.functions = ['relu', 'selu', 'tanh', 'softplus', 'softsign', 'elu', 'exponential']
        self.dropoutRates = []

        for i in range(self.populationSize):
            backend.clear_session()
            np.random.seed(42)
            tf.random.set_seed(42)

            new_individual = models.Sequential()
            layers_number = random.randint(self.minLayers, self.maxLayers)
            for j in range(layers_number):
                if j == 0:
                    new_individual.add(layers.Dense(random.randint(self.minNeurons, self.maxNeurons),
                                                    activation=random.choice(self.functions),
                                                    input_shape=(self.numberOfFeatures,)))
                elif j == layers_number - 1:
                    if self.numberOfLabels > 2:
                        new_individual.add(layers.Dense(self.numberOfLabels, activation='softmax'))
                    else:
                        new_individual.add(layers.Dense(1, activation='sigmoid'))
                else:
                    new_individual.add(layers.Dense(random.randint(self.minNeurons, self.maxNeurons),
                                                    activation=random.choice(self.functions)))

            self.population.append(new_individual)

        for i in range(self.populationSize):
            self.scores.append(0)
            self.ordered.append(0)

        for individual in self.population:
            self.compile_and_train(individual, self.epochs)

    def neural_net_factory(self, layer_neurons: list, activations: list, epochs):
        backend.clear_session()
        np.random.seed(42)
        tf.random.set_seed(42)

        print('Layers:')
        print(layer_neurons)

        new_individual = models.Sequential()
        for index, n in enumerate(layer_neurons):
            if index == 0:
                new_individual.add(layers.Dense(n, activation=activations[index],
                                                input_shape=(self.numberOfFeatures,)))
            else:
                new_individual.add(layers.Dense(n, activation=activations[index]))
            # elif index == len(layer_neurons) - 1:
            #     if n >= 2:
            #         new_individual.add(layers.Dense(n, activation='softmax'))
            #     else:
            #         new_individual.add(layers.Dense(n, activation='sigmoid'))
            # else:
            #     new_individual.add(layers.Dense(n, activation=self.function))

        print('Compiling...')
        new_individual.compile(optimizer=optimizers.Adam(learning_rate=0.001), loss='binary_crossentropy',
                               metrics=['accuracy'])

        callback = callbacks.EarlyStopping(monitor='accuracy', patience=4)

        weights = []

        # print('Weights before training:')
        for layer in new_individual.layers:
            weights.append(layer.get_weights()[0])

        # print(weights)

        print('Training...')
        new_individual.fit(self.trainFeatures, self.trainLabels, epochs=epochs, batch_size=128, verbose=False)

        # print(outputModel.summary())

        weights = []
        # print('Weights after training:')
        for layer in new_individual.layers:
            weights.append(layer.get_weights()[0])

        # print(weights)

        return new_individual

    def crossover(self, parent1_layers: list, parent2_layers: list, parent1_activations: list,
                  parent2_activations: list, *args, **kwargs):
        child_layers = []
        child_activations = []

        layers_number = random.randint(min(len(parent1_layers), len(parent2_layers)),
                                       max(len(parent1_layers), len(parent2_layers)))

        if len(parent1_layers) > len(parent2_layers):
            temp_layers = parent1_layers
            parent1_layers = parent2_layers
            parent2_layers = temp_layers

            temp_activations = parent1_activations
            parent1_activations = parent2_activations
            parent2_activations = temp_activations

        split = random.randint(0, len(parent1_layers) - 1)

        j = 0
        for i in range(layers_number):
            if i >= split:
                child_layers.append(parent2_layers[len(parent2_layers) - (layers_number - split) + j])
                child_activations.append(parent2_activations[len(parent2_activations) - (layers_number - split) + j])
                j += 1
            else:
                if i == layers_number - 1:
                    child_layers.append(parent1_layers[-1])
                    child_activations.append(parent1_activations[-1])
                else:
                    child_layers.append(parent1_layers[i])
                    child_activations.append(parent1_activations[i])

        return child_layers, child_activations

    def mutation(self, child_layers, child_activations):
        if len(child_layers) <= 2:
            return child_layers, child_activations
        else:
            layer_to_modify = random.randint(1, len(child_layers) - 2)
            layer_to_modify_act = random.randint(1, len(child_activations) - 2)
            mutation_rate = random.uniform(0, 1)
            if mutation_rate <= self.mutationRate:
                if child_layers[layer_to_modify] <= 2:
                    child_layers[layer_to_modify] = child_layers[layer_to_modify] + 1
                else:
                    child_layers[layer_to_modify] = child_layers[layer_to_modify] + random.randint(-1, 1)
                child_activations[layer_to_modify_act] = random.choice(self.functions)

            return child_layers, child_activations

    def evaluate(self):
        for i in range(self.populationSize):
            loss, acc = self.population[i].evaluate(self.testFeatures, self.testLabels, verbose=False)
            self.scores[i] = acc

    def order(self):
        scores_copy = self.scores.copy()
        for i in range(self.populationSize):
            largest = max(scores_copy)
            indexOfLargest = scores_copy.index(largest)
            self.ordered[i] = indexOfLargest
            scores_copy[indexOfLargest] = -9999

    def print_scores(self):
        for i in range(self.populationSize):
            print('Neural network ' + str(i + 1) + ' has accuracy ' + str(self.scores[i]))

    def compile_and_train(self, network, epochs):
        network.compile(optimizer=optimizers.Adam(learning_rate=0.001), loss='binary_crossentropy',
                        metrics=['accuracy'])

        history = network.fit(self.trainFeatures, self.trainLabels, epochs=epochs, batch_size=128, verbose=False)
        # history_dict = history.history

    @staticmethod
    def get_configuration(network):
        network_layers = []
        network_activations = []
        for layer in network.layers:
            network_layers.append(layer.get_config()['units'])
            network_activations.append(layer.get_config()['activation'])

        return network_layers, network_activations

    @staticmethod
    def plot(values: list, axis1_title, axis2_title):
        iterations = range(1, len(values) + 1)

        plt.plot(iterations, values, 'b')

        plt.xlabel(axis1_title)
        plt.ylabel(axis2_title)

        plt.show()

    def accuracy_average(self):
        return sum(self.scores) / len(self.scores)

    def create_child(self, child_layers, child_activations, child_epochs):
        child = self.neural_net_factory(child_layers, child_activations, child_epochs)
        return child

    def create_new_population(self, best_models, elitism_percent):
        print("Best models number: " + str(len(best_models)))
        split = int(round(elitism_percent * len(best_models)))
        print("Elitism split: " + str(split))

        for i in range(split):
            print("append")
            self.nextPopulation.append(best_models[i])

        while len(self.nextPopulation) < self.populationSize:
            random_model1 = random.randint(0, len(best_models) - 1)
            random_model2 = random.randint(0, len(best_models) - 1)

            if random_model1 == random_model2:
                continue
            else:
                parent1_layers, parent1_activations = self.get_configuration(best_models[random_model1])
                parent2_layers, parent2_activations = self.get_configuration(best_models[random_model2])

                child_layers, child_activations = self.crossover(parent1_layers, parent2_layers,
                                                                 parent1_activations, parent2_activations)

                child_layers_mutated, child_activations_mutated = self.mutation(child_layers, child_activations)

                child = self.create_child(child_layers_mutated, child_activations_mutated, self.epochs)

                self.nextPopulation.append(child)

        # for i in range(0, len(best_models)):
        #     for j in range(0, len(best_models)):
        #         if i == j:
        #             continue
        #         else:
        #             if len(self.nextPopulation) >= self.populationSize:
        #                 return
        #             else:
        #                 parent1_layers, parent1_activations = self.get_configuration(best_models[i])
        #                 parent2_layers, parent2_activations = self.get_configuration(best_models[j])
        #
        #                 child_layers, child_activations = self.crossover(parent1_layers, parent2_layers,
        #                                                                  parent1_activations, parent2_activations)
        #
        #                 child_layers_mutated, child_activations_mutated = self.mutation(child_layers, child_activations)
        #
        #                 child = self.create_child(child_layers_mutated, child_activations_mutated, self.epochs)
        #
        #                 self.nextPopulation.append(child)

    def genetic_process(self, iterations, include_only_fittest=True, fittest_percentage=0.9, verbose=False):
        self.verbose = verbose

        averages = []
        best_scores = []

        for i in range(iterations):
            if verbose is True:
                print()
                print('----------------------------------------')
                print('Iteration ' + str(i) + ' in progress...')
                print('----------------------------------------')
                print()

                for j in range(self.populationSize):
                    print(self.population[j].summary())

            self.evaluate()
            self.order()

            if verbose is True:
                self.print_scores()

            averages.append(self.accuracy_average())
            best_scores.append(self.scores[self.ordered[0]])
            if verbose is True:
                print('Best networks ' + str(self.ordered[:int(self.populationSize / 2)]))

            models_for_reproduction = []

            if include_only_fittest:
                for j in range(int(self.populationSize / 2)):
                    models_for_reproduction.append(self.population[self.ordered[j]])
            else:
                fittest_individuals_number = int(round(fittest_percentage * int((self.populationSize / 2))))
                print("Fittest individuals number: " + str(fittest_individuals_number))
                for j in range(fittest_individuals_number):
                    models_for_reproduction.append(self.population[self.ordered[j]])

                t = -1
                worst_individuals_number = int(self.populationSize / 2) - fittest_individuals_number
                print("Worst individuals number: " + str(worst_individuals_number))
                for j in range(worst_individuals_number):
                    print("T: " + str(t))
                    models_for_reproduction.append(self.population[self.ordered[t]])
                    t -= 1

            self.create_new_population(models_for_reproduction, elitism_percent=0.0)
            self.population = self.nextPopulation
            print("Population size: " + str(len(self.population)))
            self.nextPopulation = []

        print('Best accuracy after ' + str(iterations) + ' iterations is ' + str(self.scores[self.ordered[0]]))

        self.plot(averages, 'Iterations', 'Population average accuracy')
        self.plot(best_scores, 'Iterations', 'Best accuracy')

        self.outputModel = self.population[self.ordered[0]]
        print(self.outputModel.summary())
        output_layers, output_activations = self.get_configuration(self.outputModel)
        print("Output Layers: " + str(output_layers))
        print("Output Activations: " + str(output_activations))


if __name__ == '__main__':
    genetic = GeneticAlgorithmNetworkOptimizer('datasets/features_processed.csv', min_layers=2,
                                               max_layers=5, min_neurons=4, max_neurons=16, population_size=20,
                                               mutation_rate=0.1, epochs=100)
    genetic.genetic_process(300, include_only_fittest=True, verbose=True)
    genetic.generate('ESP_NN_OPTIMIZED')
