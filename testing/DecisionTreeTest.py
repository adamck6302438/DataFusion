from algorithm.DecisionTree import DecisionTree as DT

training_data = [
    [1, 149, 41, True],
    [1, 149, 40, False],
    [0, 149, 40, False],
    [0, 150, 41, True],
    [0, 150, 40, False],
    [1, 150, 41, True],
    [1, 150, 40, True],
]

if __name__ == '__main__':
    my_tree = DT.build_tree(training_data)
    DT.print_tree(my_tree)
    testing_data = [
        # [75, 61, 22.3, False],
        # [200, 122, 75.2, True],
        # [90, 80, 28.4, False],
        # [149, 99, 30.2, False],
        # [222, 199, 79.2, True],
        # [119, 60, 27.3, False],
        # [20, 130, 22, False],
        [75, 61, 22.3],
        [200, 122, 75.2],
        [90, 80, 28.4],
        [149, 99, 30.2],
        [222, 199, 79.2],
        [119, 60, 27.3],
        [20, 130, 22],
    ]

    for row in testing_data:
        # print("On Fire: %s" %
        #       (DT.classify(row, my_tree)))
        print("Predicted: %s" %
              (DT.print_leaf(DT.classify(row, my_tree))))
        # print("Actual: %s. Predicted: %s" %
        #       (row[-1], DT.print_leaf(DT.classify(row, my_tree))))