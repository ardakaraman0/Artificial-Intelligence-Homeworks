# Arda Karaman 2237568
from DataLoad import RegressionDataLoad
import numpy as np

learning_rate = 0.01
np.random.seed(10)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(Z):
    s = 1 / (1 + np.exp(-Z))
    return s * (1 - s)


def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation


class MLPRegression:

    def __init__(self, train_data_file, test_data_file):
        self.train_data, self.train_label = RegressionDataLoad.loadData(train_data_file)
        self.test_data, self.test_label = RegressionDataLoad.loadData(test_data_file)
        self.hidden_layer = [[np.random.normal(0.0, 1) for i in range(3)] for i in range(3)]
        self.output_layer = [np.random.normal(0.0, 1) for i in range(4)]
        self.network = [3, 3, 1]
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

        reg_res = 1 * self.output_layer[0]
        for index in range(len(result)):
            reg_res += result[index] * self.output_layer[index+1]

        reg_res = sigmoid(reg_res)
        return reg_res, hidden_neuron_values

    # updates the weights of the network with the stochastic gradient descent method
    def train(self, iteration=20):
        for current_iteration in range(iteration):
            loss_value = 0.0
            # for each instance the network weights are updated...
            for instance_index in range(len(self.train_data)):
                instance = self.train_data[instance_index]
                label = self.train_label[instance_index]
                res, Z1 = self.forward(instance)
                sse_value = (res - label) ** 2
                """
                The code part that updates all network weights depending on the error value (sse_value) goes here
                """
                # Output layer weights
                for index in range(len(self.output_layer)):
                    self.output_layer[index] = self.output_layer[index] - learning_rate * ((-2 * (label - res)) * (sigmoid_derivative(res) * (1 - sigmoid_derivative(res))) * Z1[index])
                # Hidden layer weights
                for index in range(len(self.hidden_layer)):
                    for i in range(len(self.hidden_layer[index])):
                        self.hidden_layer[index][i] = self.hidden_layer[index][i] - learning_rate * ((-2 * (label - res)) * (sigmoid_derivative(res) * (1 - sigmoid_derivative(res))) * (self.output_layer[i+1]) * (sigmoid_derivative(Z1[index]) * (1 - sigmoid_derivative(Z1[index]))) * instance[index])

                loss_value += sse_value

            test_loss = 0.0
            # we measure the sse error on the test data set
            for instance_index in range(len(self.test_data)):
                instance = self.test_data[instance_index]
                label = self.test_label[instance_index]
                res, Z1 = self.forward(instance)
                sse_value = (res - label) ** 2
                test_loss += sse_value
            print(f"Iteration {current_iteration} SSE Loss: {loss_value} - Test SSE: {test_loss}")


mlp_regression = MLPRegression("regression_train.txt", "regression_test.txt")
mlp_regression.train(1000)
