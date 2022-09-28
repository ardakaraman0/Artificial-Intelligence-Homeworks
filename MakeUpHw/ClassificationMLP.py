# Arda Karaman 2237568
from DataLoad import IrisLoad
import numpy as np

learning_rate = 0.001
np.random.seed(10)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(Z):
    s = 1 / (1 + np.exp(-Z))
    return s * (1 - s)



class MLPClassification:

    def __init__(self, train_data_file, test_data_file):
        self.train_data, self.train_label = IrisLoad.loadData(train_data_file)
        self.test_data, self.test_label = IrisLoad.loadData(test_data_file)
        self.hidden_layer = [[np.random.normal(0.0, 1) for i in range(3)] for i in range(3)]
        self.output_layer = [[np.random.normal(0.0, 1) for i in range(4)] for i in range(3)]
        self.network = [3, 4, 3]
        """
        Your code part that creates weights and initializes them goes here...
        You may initialize each weight with the value yielded by numpy.random.normal(0.0, 1)
        """

    # for a given single instance it returns the neural network output
    def forward(self, instance):
        result = [0 for x in instance]
        """
        Your code for the forward pass goes here
        (Hint: you may need to store the middle layer outputs on a class variable
         Since these output values are going to be used later during training)
        """
        for index in range(len(instance)):
            for i in range(len(self.hidden_layer[index])):
                result[i] += instance[i] * self.hidden_layer[index][i]

        result = [sigmoid(x) for x in result]
        hidden_neuron_values = [1]
        for x in result:
            hidden_neuron_values.append(x)

        for index in range(len(result)):
            result[index] += self.output_layer[index][0]
            for i in range(len(self.hidden_layer[index])):
                result[i] = result[i] * self.output_layer[index][i + 1]

        result = [sigmoid(x) for x in result]
        return result, hidden_neuron_values

    # updates the weights of the network with the stochastic gradient descent method
    def train(self, iteration=20):
        for current_iteration in range(iteration):
            loss_value = 0.0
            correct_count = 0
            false_count = 0

            # for each instance the network weights are updated...
            for instance_index in range(len(self.train_data)):
                instance = self.train_data[instance_index]
                label = self.train_label[instance_index]
                res, Z1 = self.forward(instance)
                cross_entropy_value = np.sum(-np.log(res) * np.array(label, dtype=np.float32))
                """
                The code part that updates all network weights depending on the error value (cross_entropy_value) goes here
                """
                # Output layer weights
                for index in range(len(self.output_layer)):
                    for i in range(len(self.output_layer[index])):
                        self.output_layer[index][i] = self.output_layer[index][i] - learning_rate * ((label[index] / (res[index] * np.log(10) + 0.000000001)) * (sigmoid_derivative(res[index]) * (1 - sigmoid_derivative(res[index]))) * Z1[index])

                # Hidden layer weights
                for index in range(len(self.hidden_layer)):
                    for i in range(len(self.hidden_layer[index])):
                        self.hidden_layer[index][i] = self.hidden_layer[index][i] - learning_rate * ((label[index] / (res[index] * np.log(10) + 0.000000001)) * (sigmoid_derivative(res[index]) * (1 - sigmoid_derivative(res[index]))) * (self.output_layer[index][i + 1]) * (sigmoid_derivative(Z1[index]) * (1 - sigmoid_derivative(Z1[index]))) * instance[index])

                loss_value += cross_entropy_value

            # We calculate the accuracy score on the train dataset
            for instance_index in range(len(self.train_data)):
                instance = self.train_data[instance_index]
                label = self.train_label[instance_index]
                res = self.forward(instance)
                if np.argmax(res) == np.argmax(label):
                    correct_count += 1
                else:
                    false_count += 1
            test_correct_count = 0
            test_false_count = 0

            # We calculate the accuracy score on the test dataset
            for instance_index in range(len(self.test_data)):
                instance = self.test_data[instance_index]
                label = self.test_label[instance_index]
                res = self.forward(instance)
                if np.argmax(res) == np.argmax(label):
                    test_correct_count += 1
                else:
                    test_false_count += 1
            print(
                f"Iteration {current_iteration} CE Loss: {loss_value} - Train Accuracy: {correct_count / (correct_count + false_count) * 100} - Test Accuracy: {test_correct_count / (test_correct_count + test_false_count) * 100}")


mlp_classifiation = MLPClassification("iris_train.txt", "iris_test.txt")
mlp_classifiation.train(100)
