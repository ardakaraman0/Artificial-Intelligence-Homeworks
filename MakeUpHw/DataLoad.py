class IrisLoad():
    @staticmethod
    def loadData(file_path):
        data = []
        one_hot_labels = []
        with open(file_path, "r") as file:
            for line in file:
                if len(line) < 4:
                    continue
                line = line.strip("\n\r")
                parts = line.split("#")
                data.append([float(parts[0]), float(parts[1]), float(parts[2])])
                one_hot_labels.append(eval(parts[3]))
        return data, one_hot_labels

class RegressionDataLoad():
    @staticmethod
    def loadData(file_path):
        data = []
        labels = []
        with open(file_path, "r") as file:
            for line in file:
                if len(line) < 4:
                    continue
                line = line.strip("\n\r")
                parts = line.split(",")
                data.append([float(parts[0]), float(parts[1]), float(parts[2])])
                labels.append(float(parts[3]))
        return data, labels