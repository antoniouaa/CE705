# Author: Alexandros Antoniou
# username: aa16322
# ID: 1908855

from random import choices
from math import fabs
from statistics import median

def load_from_csv(file_name):
    """
    The csv module from the standard library is used to easily import
    the data from the csv file provided
    A context manager is used to handle
    opening and closing the file
    The values are converted to floating points
    before they are added to the matrix.
    """
    from csv import reader
    mat = []
    try:
        with open(file_name, "r") as csvfile:
            csvreader = reader(csvfile, delimiter=",")
            for row in csvreader:
                newline = [float(x) for x in row]
                mat.append(newline)
        return mat
    except FileNotFoundError:
        import sys
        print("File not found in current directory")
        sys.exit()

def get_distance(a, b):
    """
    The Manhattan distance is used to calculate the 
    distance between two lists, a and b
    The two lists are zipped together to easily access elements from both
    of them
    """
    manhattan_distance = 0
    for point_a, point_b in zip(a, b):
        manhattan_distance += fabs(point_a - point_b)
    return manhattan_distance

def get_column(mat, col_number):
    """
    Loops over the matrix selects elements of the same column and returns all of them in a list
    """
    col_list = []
    for row in mat:
        col_list.append(row[col_number])
    return col_list

def get_max(mat, col_number):
    """
    Uses get_column to retrieve a specified column from the matrix
    and then returns the maximum value of that column
    """
    return max(get_column(mat, col_number))

def get_min(mat, col_number):
    """
    Uses get_column to retrieve a specified column from the matrix 
    and then returns the minimum value of that column
    """
    return min(get_column(mat, col_number))

def get_standardised_matrix(mat):
    """
    The standardisation formula is used to create a new matrix of 
    range scaled data between -1 and 1
    For reference,
    D'(i,j) = (D(i,j) - mean(D(j))) / (max(D(j)) - min(D(j)))
    """
    standardised_matrix = []
    max_value, min_value, mean_of_col = [], [], [] 
    cols = range(len(mat[0]))
    for i in cols:
        col_list = get_column(mat, i)
        mean_of_col.append(sum(col_list, 0.0) / len(col_list))
        max_value.append(get_max(mat, i)) 
        min_value.append(get_min(mat, i))
    for lst in mat:
        standardised_list = []
        for i, element in enumerate(lst):
            standardised_element = (element - mean_of_col[i]) \
                    / (max_value[i] - min_value[i])
            standardised_list.append(standardised_element)
        standardised_matrix.append(standardised_list)
    return standardised_matrix

def get_median(mat, col_number):
    """
    The median() function from the statistics module is used to calculate 
    the median of the specified column in the matrix
    The median value of a collection is the value at the 50-percentile,
    half of the other values are larger and half of them are smaller
    """
    lst = get_column(mat, col_number) 
    return median(lst)
    
def get_groups(mat, k):
    """
    The clustering algorithm from the appendix is used to calculate the 
    distance of each data row from each of the cluster centers selected
    A list is returned, the value is the number of the cluster, the index 
    where the value is located is the number of the data row
    """
    population = range(len(mat))
    try:
        if not k in range(2, len(mat)):
            raise ValueError("k not in appropriate range")
    except ValueError as e:
        import sys
        print(str(e))
        sys.exit()
    k_indices = choices(population, weights=None, k=k)
    # check for duplicates by looking at the set of indices selected
    while len(set(k_indices)) != k:
        k_indices = choices(range(len(mat)), weights=None, k=k)
    c_matrix = [mat[i] for i in k_indices]
    s_list = populate_s_list(mat, c_matrix)
    c = None
    while not c == c_matrix:
        c = c_matrix
        c_matrix = get_centroids(mat, s_list, k)
        s_list = populate_s_list(mat, c_matrix)
    return s_list

def populate_s_list(mat, c_matrix):
    """
    Takes the matrix and the list of centroids and produces a list of integers 
    which show the number of the cluster they are closest to
    Dictionaries are used to keep track of the index of cluster [key] and the 
    distance to each wine
    The minimum of the distances to each cluster is then selected and the number 
    of the cluster is appended in the s_list
    """
    s_list = []
    for data_row in mat:
        manhattan_dist_dict = {}
        for i, c_row in enumerate(c_matrix):
            manhattan_dist_dict[i] = get_distance(data_row, c_row)
        closest_cluster = min(manhattan_dist_dict, key=manhattan_dist_dict.get)
        s_list.append(closest_cluster)
    return s_list

def get_centroids(mat, s_list, k):
    """
    Implements step 6 of the clustering algorithm, which updates the values 
    for each of the c_lists to be the median of the column
    The algorithm only takes into account the rows who are clustered around 
    each chosen cluster
    """
    c_matrix = []
    for k_ in range(k):
        c_list = []
        consideration_row = [mat[i] for i, x in enumerate(s_list) if x == k_]
        length_of_row = len(consideration_row[0])
        for col_number in range(length_of_row):
            c_list.append(get_median(consideration_row, col_number))
        c_matrix.append(c_list)
    return c_matrix

def run_tests():
    """
    Tests the get_groups() function by supplying it a predetermined range of 
    k values
    Uses Counter from the collections module to count the occurences of all
    clusters in the s_list and then print it to the screen
    """
    from collections import Counter
    FILENAME = "data.csv"
    matrix = load_from_csv(FILENAME)
    standardised_matrix = get_standardised_matrix(matrix)
    for k in range(2, 7):
        groups = get_groups(standardised_matrix, k)
        dict_groups = Counter(groups)
        print(f"\nNumber of Clusters: {k}")
        for key, value in sorted(dict_groups.items()):
            print(f"Cluster {key+1} has {value} entities")

if __name__ == "__main__":
    from timeit import default_timer
    start = default_timer()
    run_tests()
    end = default_timer()
    print(f"\nTime taken: {end-start}")

