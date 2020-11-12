from __future__ import print_function


# General rules
# 1. If temperature > 40
# 2. If CO > 150
# 3. If Gas = 1
# Sound the alarm when 2 of the above is valid
# training_data = [
#     [25.3, 76, 66, 49.5, False],
#     [56.2, 180, 120, 22, True],
#     [28.4, 90, 80, 43, False],
#     [32, 150, 100, 22.9, False],
#     [79.2, 210, 190, 12, True],
#     [24, 150, 60, 49.5, False],
#     [29, 70, 130, 70, False]
# ]

training_data = [
    [1, 149, 41, True],
    [1, 149, 40, False],
    [0, 149, 40, False],
    [0, 150, 41, True],
    [0, 150, 40, False],
    [1, 150, 41, True],
    [1, 150, 40, True],
    # [49.5, 70, 70, 45, True],
]

# header = ["temperature", "gas", "co", "humidity", "label"]
header = ["gas", "co", "temperature", "label"]



def unique_vals(rows, col):
    return set([row[col] for row in rows])


def class_counts(rows):
    counts = {}
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


class Question:
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))


def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity


def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def find_best_split(rows):
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1

    for col in range(n_features):

        values = set([row[col] for row in rows])

        for val in values:

            question = Question(col, val)
            true_rows, false_rows = partition(rows, question)
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            gain = info_gain(true_rows, false_rows, current_uncertainty)
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question

class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    gain, question = find_best_split(rows)
    if gain == 0:
        return Leaf(rows)
    true_rows, false_rows = partition(rows, question)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)
    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    print (spacing + str(node.question))
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


if __name__ == '__main__':
    my_tree = build_tree(training_data)
    print_tree(my_tree)
    # testing_data = [
    #     [22.3, 75, 61, 43.5, False],
    #     [75.2, 200, 122, 21, True],
    #     [28.4, 90, 80, 43, False],
    #     [30.2, 149, 99, 28.9, False],
    #     [79.2, 222, 199, 10.9, True],
    #     [27.3, 119, 60, 49.5, False],
    #     [22, 20, 130, 70, False],
    # ]

    testing_data = [
        
    ]

    for row in testing_data:
        # print("Predicted: %s" %
        #       (print_leaf(classify(row, my_tree))))
        print ("Actual: %s. Predicted: %s" %
               (row[-1], print_leaf(classify(row, my_tree))))