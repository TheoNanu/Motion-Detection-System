import numpy as np
import pandas as pd


class ClassifierGenerator:
    """All classifiers split data into a training set and a test set, so we can have a generic classifier class with
    these functionalities """
    def __init__(self, dataset="datasets/features_processed.csv"):
        self.colNames = []
        self.featureList = []
        self.dataset = dataset
        self.outputModel = None

        self.dataframe = pd.read_csv(self.dataset, header=0)

        self.numberOfFeatures = self.dataframe.shape[1] - 1

#        self.dataframe.columns = self.colNames
        self.numberOfLabels = len(self.dataframe["Label"].unique())

        self.classNames = [str(i) for i in self.dataframe["Label"].unique()]

        self.dataframe.describe().to_csv("dataset_description.csv")

        for f in self.dataframe.columns:
            if f == "label" or f == "Label":
                continue
            self.featureList.append(f)
        # split dataset in dataset and target variable
        self.features = self.dataframe[self.featureList]  # dataset
        self.labels = self.dataframe["Label"]  # Target variable

        self.features = np.asarray(self.features).astype('float32')
        self.labels = np.asarray(self.labels).astype('float32')

        # Split dataset into training set, validation set and test set
        dataset_samples = len(self.features)
        train_samples_number = int(0.6 * dataset_samples)
        val_samples_number = int(0.2 * dataset_samples)

        self.trainFeatures = self.features[:train_samples_number]
        self.valFeatures = self.features[train_samples_number:train_samples_number + val_samples_number]
        self.testFeatures = self.features[train_samples_number + val_samples_number:]

        self.trainLabels = self.labels[:train_samples_number]
        self.valLabels = self.labels[train_samples_number:train_samples_number + val_samples_number]
        self.testLabels = self.labels[train_samples_number + val_samples_number:]

        print('Training Features Shape:', self.trainFeatures.shape)
        print('Training Labels Shape:', self.trainLabels.shape)
        print('Validation Features Shape:', self.valFeatures.shape)
        print('Validation Labels Shape:', self.valLabels.shape)
        print('Testing Features Shape:', self.testFeatures.shape)
        print('Testing Labels Shape:', self.testLabels.shape)
    
    def generate(self, file_name):
        weights = []
        biases = []
        functions = []
        matrices = []

        if self.outputModel is not None:
            for layer in self.outputModel.layers:
                if not layer.get_config()['name'].startswith('dropout'):
                    functions.append(layer.get_config()['activation'])
                    weights.append(layer.get_weights()[0])
                    print(layer.get_weights()[0].shape)
                    biases.append(layer.get_weights()[1])

            print(weights)
            print()
            print(biases)
            for matrix in weights:
                matrices.append(np.transpose(matrix))

            dir_name = "output/"
            source_filename = file_name + '.c'

            with open(dir_name + source_filename, 'w+') as source:
                source.write('#include <stdio.h>\n#include <stdlib.h>\n')
                source.write('#include <math.h>\n\n')

                source.write(f'#define INPUT_SIZE {str(len(weights[0]))}\n')
                source.write(f'#define OUTPUT_SIZE {str(len(weights[-1][0]))}\n\n')

                source.write('#define ADD(a, b) (a + b)\n')
                source.write('#define SUBTRACT(a, b) (a - b)\n')
                source.write('#define MULTIPLY(a, b) (a * b)\n')
                source.write('#define DIVIDE(a, b) (a / b)\n')
                source.write('#define sigmoid(x) 1 / (1 + exp(-x))\n')
                source.write('#define tanh(x) 2 / (1 + exp(-2 * x)) - 1\n')
                source.write('#define relu(x) x > 0 ? x : 0\n')
                source.write('#define selu(x) x > 0 ? 1.05070098 * x : 1.05070098 * 1.67326324 * (exp(x) - 1)\n')
                source.write('#define softplus(x) log(exp(x) + 1)\n')
                source.write('#define softsign(x) x / (abs(x) + 1)\n')
                source.write('#define exponential(x) exp(x)\n')
                source.write('#define elu(x) x > 0 ? x : 1.67326324 * (exp(x) - 1)\n\n')

                source.write('float *softmax(float vector[], int len)\n')
                source.write('{\n')
                source.write('\tfloat* result = (float*) malloc(len * sizeof(float));\n')
                source.write('\n')
                source.write('\tif(!result)\n')
                source.write('\t\treturn NULL;\n')
                source.write('\n')
                source.write('\tfor(int i = 0; i < len; i++)\n')
                source.write('\t{\n')
                source.write('\t\tfloat sum = 0;\n')
                source.write('\t\tfor(int j = 0; j < len; j++)\n')
                source.write('\t\t{\n')
                source.write('\t\t\tsum += exp(vector[j]);\n')
                source.write('\t\t}\n')
                source.write('\t\tresult[i] = exp(vector[i]) / sum;\n')
                source.write('\t}\n')
                source.write('\treturn result;\n')
                source.write('}\n\n')

                for index, matrix in enumerate(matrices):
                    source.write('static const float bias_' + str(index) + '[' + str(len(biases[index])) + '] = {')
                    for i, bias in enumerate(biases[index]):
                        if i == len(biases[index]) - 1:
                            source.write(str(bias))
                        else:
                            source.write(str(bias) + ", ")
                    source.write('};\n\n')

                    source.write('static const float weights_' + str(index) + '[' + str(len(matrix)) + '][' +
                                 str(len(matrix[0])) + '] = {\n')

                    for row_index, row in enumerate(matrix):
                        source.write('\t\t{')
                        for i, elem in enumerate(row):
                            if i == len(row) - 1:
                                source.write(str(elem))
                            else:
                                source.write(str(elem) + ', ')
                        if row_index == len(matrix) - 1:
                            source.write('}\n')
                        else:
                            source.write('},\n')
                    source.write('};\n\n')

                source.write('void ' + file_name + '(const float input[INPUT_SIZE], float output[OUTPUT_SIZE])\n')
                source.write('{\n')

                for i in range(len(functions)):
                    output_size = len(weights[i][0])
                    input_size = len(weights[i])

                    source.write('\tfloat output_' + str(i) + '[' + str(output_size) + '];\n\n')

                    source.write('\tfor(int i = 0; i < ' + str(output_size) + '; i++)\n')
                    source.write('\t{\n')
                    source.write('\t\tfloat res = 0;\n')

                    source.write('\t\tfor(int j = 0; j < ' + str(input_size) + '; j++)\n')
                    source.write('\t\t{\n')
                    if i == 0:
                        source.write('\t\t\tres += input[j] * weights_' + str(i) + '[i][j];\n')
                    else:
                        source.write('\t\t\tres += output_' + str(i - 1) + '[j] * weights_' + str(i) + '[i][j];\n')
                    source.write('\t\t}\n')

                    if functions[i] == 'relu':
                        source.write('\t\toutput_' + str(i) + '[i] = relu(res + bias_' + str(i) + '[i]);\n')
                    elif functions[i] == 'sigmoid':
                        source.write('\t\toutput_' + str(i) + '[i] = sigmoid(res + bias_' + str(i) + '[i]);\n')
                    elif functions[i] == 'selu':
                        source.write('\t\toutput_' + str(i) + '[i] = selu(res + bias_' + str(i) + '[i]);\n')
                    elif functions[i] == 'elu':
                        source.write('\t\toutput_' + str(i) + '[i] = elu(res + bias_' + str(i) + '[i]);\n')
                    elif functions[i] == 'softsign':
                        source.write('\t\toutput_' + str(i) + '[i] = softsign(res + bias_' + str(i) + '[i]);\n')
                    elif functions[i] == 'softplus':
                        source.write('\t\toutput_' + str(i) + '[i] = softplus(res + bias_' + str(i) + '[i]);\n')
                    elif functions[i] == 'exponential':
                        source.write('\t\toutput_' + str(i) + '[i] = exponential(res + bias_' + str(i) + '[i]);\n')
                    elif functions[i] == 'softmax':
                        source.write('\t\toutput_' + str(i) + '[i] = res + bias_' + str(i) + '[i];\n')
                    else:
                        source.write('\t\toutput_' + str(i) + '[i] = tanh(res + bias_' + str(i) + '[i]);\n')

                    if i == len(functions) - 1:
                        source.write('\t}\n')
                    else:
                        source.write('\t}\n\n')

                if functions[-1] == 'sigmoid':
                    source.write('\toutput[0] = output_' + str(i) + '[0];\n')
                else:
                    source.write('\toutput = softmax(output_' + str(i) + ', ' + str(output_size) + ');\n')

                source.write('}')

            return source_filename
        else:
            print("You need to create a network in order to generate C code for it.")
            return None
