from keras import models
from keras import layers
import numpy as np
import random
import matplotlib.pyplot as plt

from classifier_generator import ClassifierGenerator
from exceptions.invalid_structure import InvalidNeuralNetStructure
from genetic_algorithm import GeneticAlgorithm


class GeneticAlgorithmNetworkTrainer(ClassifierGenerator, GeneticAlgorithm):
    def __init__(self, population_size, dataset_file, initial_model, mutation_rate=0.1):
        super(GeneticAlgorithmNetworkTrainer, self).__init__(dataset=dataset_file)
        self.populationSize = population_size
        self.model = initial_model
        self.nextPopulation = []
        self.population = []
        self.scores = []
        self.ordered = []
        self.mutationRate = mutation_rate
        self.layersNumber = 0
        self.units = []
        self.functions = []
        self.layersType = []
        self.dropoutRates = []

        for i in range(population_size):
            self.scores.append(0)
            self.ordered.append(0)

        for layer in self.model.layers:
            if layer.get_config()['name'].startswith('dropout'):
                self.layersType.append('dropout')
                self.units.append(0)
                self.functions.append('none')
                self.dropoutRates.append(layer.get_config()['rate'])
            else:
                self.units.append(layer.get_config()['units'])
                self.functions.append(layer.get_config()['activation'])
                self.layersType.append('dense')
                self.dropoutRates.append(-1)

            self.layersNumber += 1

        for i in range(self.populationSize):
            new_individual = models.Sequential()
            for j in range(self.layersNumber):
                if j == 0 and self.layersType[j] != 'dense':
                    print("The first layer of the network has to be a dense layer!")
                    raise InvalidNeuralNetStructure

                if self.layersType[j] == 'dense':
                    if j == 0:
                        new_individual.add(layers.Dense(self.units[j], activation=self.functions[j],
                                                        input_shape=(self.numberOfFeatures,)))
                    else:
                        new_individual.add(layers.Dense(self.units[j], activation=self.functions[j]))
                else:
                    new_individual.add(layers.Dropout(self.dropoutRates[j]))

            self.population.append(new_individual)

    def evaluate(self):
        for index in range(self.populationSize):
            self.population[index].compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
            loss, acc = self.population[index].evaluate(self.testFeatures, self.testLabels, verbose=0)
            self.scores[index] = acc

    def order(self):
        scoresCopy = self.scores.copy()
        for index in range(self.populationSize):
            largest = max(scoresCopy)
            indexOfLargest = scoresCopy.index(largest)
            self.ordered[index] = indexOfLargest
            scoresCopy[indexOfLargest] = -9999

    def print_scores(self):
        for index in range(self.populationSize):
            print('Neural network ' + str(index + 1) + ' has accuracy ' + str(self.scores[index]))

    @staticmethod
    def print_weights(network):
        weights = []

        for layer in network.layers:
            weights.append(layer.get_weights()[0])

        print(weights[0][0])

    def crossover(self, net1, net2, *args, **kwargs):
        nn1_weights = []
        nn2_weights = []
        nn1_biases = []
        nn2_biases = []

        child_weights = []
        child_biases = []

        for layer in net1.layers:
            nn1_weights.append(layer.get_weights()[0])
            nn1_biases.append(layer.get_weights()[1])
            # print(layer.get_config())

        for layer in net2.layers:
            nn2_weights.append(layer.get_weights()[0])
            nn2_biases.append(layer.get_weights()[1])
            # print(layer.get_config())

        # print('Weights for the first network: ' + str(nn1_weights))
        # print('Weights for the second network: ' + str(nn2_weights))
        # print('First network weights shape: ' + str(np.asarray(nn1_weights).shape))
        # print('Second network weights shape: ' + str(np.asarray(nn2_weights).shape))
        #
        # print('Biases for the first network: ' + str(nn1_biases))
        # print('Biases for the second network: ' + str(nn2_biases))
        # print('First network biases shape: ' + str(np.asarray(nn1_biases).shape))
        # print('Second network biases shape: ' + str(np.asarray(nn2_biases).shape))

        for i in range(len(nn1_weights)):
            split = random.randint(0, np.shape(nn1_weights[i])[1] - 1)
            # print("Split: " + str(split))
            for j in range(int(split), np.shape(nn1_weights[i])[1]):
                # print(str(i) + " " + str(nn1Weights[i][:, j]))
                nn1_weights[i][:, j] = nn2_weights[i][:, j]

            child_weights.append(nn1_weights[i])

        for i in range(len(nn1_biases)):
            # print("Before: " + str(nn1_biases[i]))
            split = random.randint(0, len(nn1_biases[i]) - 1)
            for j in range(int(split), len(nn1_biases[i]) - 1):
                nn1_biases[i][j] = nn2_biases[i][j]

            # print("After: " + str(nn1_biases[i]))

            child_biases.append(nn1_biases[i])

        # print('Weights for the child: ' + str(child_weights))
        # print('Child weights shape: ' + str(np.asarray(child_weights).shape))
        #
        # print('Biases for the child: ' + str(child_biases))
        # print('Child biases shape: ' + str(np.asarray(child_biases).shape))

        return child_weights, child_biases

    def mutation(self, child_weights, child_biases):
        weights_array_mutated = random.randint(0, len(child_weights) - 1)
        biases_array_mutated = random.randint(0, len(child_biases) - 1)
        mutation_rate = random.uniform(0, 1)
        if mutation_rate <= self.mutationRate:
            print('Mutating the genes...')
            child_weights[weights_array_mutated] = child_weights[weights_array_mutated] * random.randint(2, 10)
            child_biases[biases_array_mutated] = np.ones(len(child_biases[biases_array_mutated])) * random.uniform(-1,
                                                                                                                   1)

        return child_weights, child_biases

    @staticmethod
    def plot(values: list, axis1_title, axis2_title):
        iterations = range(1, len(values) + 1)

        plt.plot(iterations, values, 'b')

        plt.xlabel(axis1_title)
        plt.ylabel(axis2_title)

        plt.show()

    def accuracy_average(self):
        return sum(self.scores) / len(self.scores)

    def create_child(self, child_weights, child_biases):
        child = models.Sequential()

        for i in range(self.layersNumber):
            if self.layersType[i] == 'dense':
                if i == 0:
                    child.add(layers.Dense(self.units[i], activation=self.functions[i],
                                           input_shape=(self.numberOfFeatures,),
                                           weights=[np.asarray(child_weights[i]), np.asarray(child_biases[i])]))
                else:
                    child.add(layers.Dense(self.units[i], activation=self.functions[i],
                                           weights=[np.asarray(child_weights[i]), np.asarray(child_biases[i])]))
            else:
                child.add(layers.Dropout(self.dropoutRates[i]))

        weights = []
        biases = []

        for layer in child.layers:
            if not layer.get_config()['name'].startswith('dropout'):
                weights.append(layer.get_weights()[0])
                biases.append(layer.get_weights()[1])

        # print("Model weights: " + str(weights))
        # print()
        # print("Model biases: " + str(biases))

        return child

    def create_new_population(self, best_models, elitism_percent):
        split = int(round(elitism_percent * self.populationSize))

        print("Split: " + str(split))

        for i in range(split):
            print("appending")
            self.nextPopulation.append(best_models[i])

        while len(self.nextPopulation) < self.populationSize:
            random_model1 = random.randint(0, len(best_models) - 1)
            random_model2 = random.randint(0, len(best_models) - 1)

            if random_model1 == random_model2:
                continue
            else:
                child_weights, child_biases = self.crossover(best_models[random_model1], best_models[random_model2])
                child_weights_mutated, child_biases_mutated = self.mutation(child_weights, child_biases)
                child_model = self.create_child(child_weights_mutated, child_biases_mutated)
                self.nextPopulation.append(child_model)

        # for i in range(len(best_models)):
        #     for j in range(len(best_models)):
        #         if i is j:
        #             continue
        #         else:
        #             child_weights, child_biases = self.crossover(best_models[i], best_models[j])
        #             child_weights_mutated, child_biases_mutated = self.mutation(child_weights, child_biases)
        #             child_model = self.create_child(child_weights_mutated, child_biases_mutated)
        #             if len(self.nextPopulation) >= self.populationSize:
        #                 return
        #             else:
        #                 self.nextPopulation.append(child_model)

    def genetic_process(self, iterations, include_only_fittest=True, fittest_percentage=0.9, verbose=False):
        averages = []
        best_scores = []
        initial_mutation_rate = self.mutationRate

        for index in range(iterations):
            if verbose is True:
                print()
                print('----------------------------------------')
                print('Iteration ' + str(index) + ' in progress...')
                print('----------------------------------------')
                print()

                print("Mutation rate: " + str(self.mutationRate))

            self.evaluate()
            self.order()

            if verbose is True:
                self.print_scores()

            averages.append(self.accuracy_average())
            best_scores.append(self.scores[self.ordered[0]])

            if index != 0:
                if averages[index] == averages[index - 1]:
                    if self.mutationRate <= 0.8:
                        self.mutationRate += 0.1
                else:
                    self.mutationRate = initial_mutation_rate

            if verbose is True:
                print('Best networks ' + str(self.ordered[:int(self.populationSize / 2)]))

            models_for_reproduction = []

            if include_only_fittest:
                for j in range(int(self.populationSize / 2)):
                    models_for_reproduction.append(self.population[self.ordered[j]])
            else:
                fittest_individuals_number = int(round(fittest_percentage * int((self.populationSize / 2))))
                for j in range(fittest_individuals_number):
                    models_for_reproduction.append(self.population[self.ordered[j]])

                t = -1
                worst_individuals_number = int(self.populationSize / 2) - fittest_individuals_number
                for j in range(worst_individuals_number):
                    models_for_reproduction.append(self.population[self.ordered[t]])
                    t -= 1

            self.create_new_population(models_for_reproduction, 0.1)
            self.population = self.nextPopulation
            self.nextPopulation = []

        print('Best accuracy after ' + str(iterations) + ' iterations is ' + str(self.scores[self.ordered[0]]))

        self.plot(averages, 'Iterations', 'Population average accuracy')
        self.plot(best_scores, 'Iterations', 'Best accuracy')

        self.outputModel = self.population[self.ordered[0]]


if __name__ == '__main__':
    model = models.Sequential()
    model.add(layers.Dense(12, activation='selu', input_shape=(8,)))
    model.add(layers.Dense(6, activation='selu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    try:
        nn = GeneticAlgorithmNetworkTrainer(40, 'datasets/features_processed.csv', model, mutation_rate=0.1)
        nn.genetic_process(1000, include_only_fittest=False, verbose=True)
        out_files = nn.generate('ESP_NN_GA')
        print("Output:\n" + "\n".join(out_files))
    except InvalidNeuralNetStructure:
        print("The provided structure of the neural network is invalid." +
              "Please make sure the first layer of the network is a dense layer")
