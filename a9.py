import csv
import math

def sum_lists(list1, list2):
    sums_list = []
    for index in range(8):
        sums_list.append(list1[index] + list2[index])
    
    return sums_list

def make_averages(sums_list, count):
    averages_list = []
    
    for value in sums_list:
        avg_value = value / count
        averages_list.append(avg_value)
    
    return averages_list

def make_data_set(training_file_name):
    input_stream = open(training_file_name, "r")
    reader = csv.reader(input_stream)

    training_set_list = []
    id_count = 0 #attached to identify each tuple, incremented each loop
    for line_list in reader:
        #skip header
        if line_list[0] == "Pregnancies":
            continue

        outcome_str = line_list[8]
        if outcome_str == "0":
            outcome_str = "n" #diabetes negative
        else:
            outcome_str = "p" #diabetes positive

        #(id, outcome, 8 patient attributes)
        patient_tuple = (str(id_count),       outcome_str, \
                         int(line_list[0]),   int(line_list[1]), \
                         int(line_list[2]),   int(line_list[3]), \
                         int(line_list[4]),   float(line_list[5]), \
                         float(line_list[6]), int(line_list[7]))
        training_set_list.append(patient_tuple)

        id_count += 1
    
    return training_set_list

def train_classifier(training_set_list):
    negative_sums_list = [0] * 8 #diabetes negative
    positive_sums_list = [0] * 8 #diabetes positive
    positive_count     = 0
    negative_count     = 0
    
    for patient_tuple in training_set_list:
        if patient_tuple[1] == "n": #negative
            negative_sums_list = sum_lists(negative_sums_list, patient_tuple[2:])
            negative_count += 1
        else:                       #positive
            positive_sums_list = sum_lists(positive_sums_list, patient_tuple[2:])
            positive_count += 1

    negative_averages_list = make_averages(negative_sums_list, negative_count)
    positive_averages_list = make_averages(positive_sums_list, positive_count)

    classifier_list = make_averages(sum_lists(negative_averages_list, positive_averages_list), 2)

    return classifier_list

def train_classifier2(training_set_list):
    negative_sums_list = [0] * 8 #diabetes negative
    positive_sums_list = [0] * 8 #diabetes positive
    positive_count     = 0
    negative_count     = 0
    
    for patient_tuple in training_set_list:
        if patient_tuple[1] == "n": #negative
            for i in range(2, 10):
                negative_sums_list[i - 2] += patient_tuple[i]
            negative_count += 1
        else:                       #positive
            for i in range(2, 10):
                positive_sums_list[i - 2] += patient_tuple[i]
            positive_count += 1

    negative_averages_list = make_averages(negative_sums_list, negative_count)
    positive_averages_list = make_averages(positive_sums_list, positive_count)

    classifier_list = []
    for i in range (8):
        avg_value = (negative_averages_list[i] + positive_averages_list[i])/2
        classifier_list.append(avg_value)

    return classifier_list

def classify_test_set_list(test_set_list, classifier_list):
    result_list = []
    for patient_tuple in test_set_list:
        negative_count = 0
        positive_count = 0
        id_str, diagnosis_str = patient_tuple[:2]
        for index in range(8):
            if patient_tuple[index + 2] > classifier_list[index]:
                positive_count += 1
            else:
                negative_count += 1
        result_tuple = (id_str, negative_count, positive_count, diagnosis_str)
        result_list.append(result_tuple)
    
    return result_list

def report_results(result_list):
    total_count = 0
    inaccurate_count = 0
    for result_tuple in result_list:
        negative_count, positive_count, diagnosis_str = result_tuple[1:4]
        total_count += 1
        if   (negative_count > positive_count) and (diagnosis_str == 'p'):
            inaccurate_count += 1
        elif (negative_count < positive_count) and (diagnosis_str == 'n'): # 
            inaccurate_count += 1
    
    print(f"Of {total_count} patients, there were {inaccurate_count} inaccuracies")

def find_least_discriminative_feature(patient_tuple, classifier_list):
    '''
    given patient_tuple without id or diagnosis_str, returns attribute index
    closest to corresponding classifier_list attribute
    '''
    difference_list = []
    for i in patient_tuple:


print("Reading in training data...")
training_file_name = "diabetes_sample_training.csv"
training_set_list = make_data_set(training_file_name)
print("Done reading training data.\n")

print(training_set_list)

print("Training classifier...")
classifier_list = train_classifier(training_set_list)
print("Done training classifier.\n")

for value in classifier_list:
    print("{:.3f}".format(value), end=" | ")


print("Reading in test data...")
test_file_name = "diabetes_sample_testing.csv"
test_set_list = make_data_set(test_file_name)
print("Done reading test data.\n")


print(f"test set list: \n")
for patient_tuple in test_set_list:
    print("\n")
    for value in patient_tuple[2:]:
        print("{:.3f}".format(value), end=" | ")

print("Classifying records...")
result_list = classify_test_set_list(test_set_list, classifier_list)
print("Done classifying.\n")

print(f"result list: \n")
for result_tuple in result_list:
    print(result_tuple, end="")
    if result_tuple[1] > result_tuple[2]:
        print("negative")
    else:
        print("positive")


report_results(result_list)

print("Program finished.")





'''
def find_least_discriminative_feature2(patient_tuple, classifier_list):
    '''
    #given patient_tuple without id or diagnosis_str, returns attribute index
    #closest to corresponding classifier_list attribute
'''
    difference_list = []
    for i in range(8):
        difference = abs(patient_tuple[i] - classifier_list[i])
        difference_list.append(difference)
    
    min_difference = min(difference_list)

    min_index = 0
    for i in range(8):
        if difference_list[i] == min_difference:
            min_index = i 
    
    print(min_index)

    return min_index



print("\nAverages list:")
for value in attribute_avgs_list:
    print("{:.3f}".format(value), end=" | ")

def get_attribute_avgs_list(training_set_list):
    
    finds the average value for each attribute in training set data. Discards
    missing values (where values = 0 that are not the pregnancy attribute)
    
    #initializing lists
    attribute_sums_list  = [0] * 8
    attribute_count_list = [0] * 8
    attribute_avgs_list  = [0] * 8

    #get sum of each attribute and number of valid values per attribute
    #iterate through each attribute
    for index in range(8):
        #for each patient_tuple
        for patient_tuple in training_set_list:
            #if patient_tuple has a missing value, skip that attribute value
            #[index + 2] is because patient_tuple's attributes are shifted by 2
            if index in [1, 2, 3, 4, 5, 6, 7] and patient_tuple[index + 2] == 0: 
                continue
            #else
            #add attribute value to sum (patient_tuple's attributes are shifted by 2)
            attribute_sums_list[index]  += patient_tuple[index+2] 
            attribute_count_list[index] += 1 #increment count                     
    
    #get attribute_avgs_list
    for index in range(8):
        attribute_avgs_list[index] = attribute_sums_list[index]/attribute_count_list[index]

    return attribute_avgs_list

def fill_empty_values(data_set_list, attribute_avgs_list):
    
    for each patient_tuple with data that contains a missing value, the
    average value for that attribute amongst all patients is put in its place
    
    for index1 in range(len(data_set_list)):
        patient_tuple = data_set_list[index]
        if index in [1, 2, 3, 4, 5, 6, 7] and patient_tuple[index + 2] == 0:









print("training_set_list:")
for patient_tuple in training_set_list:
    print(patient_tuple)




print("\n\nmin index: ", min_index)

print("\nnegative_avg_list")
for value in neg_avgs_list:
    print("{:.3f}".format(value), end=" | ")

print("\n\npositive_avg_list")
for value in pos_avgs_list:
    print("{:.3f}".format(value), end=" | ")
print("\n")

print("\n\nclassifier_list")
for value in classifier_list:
    print("{:.3f}".format(value), end=" | ")

print(f"\n\n\ntest set list: ", end="")
for patient_tuple in testing_set_list:
    print("\n")
    for value in patient_tuple[2:]:
        print("{:.3f}".format(value), end=" | ")

print(f"\n\nresult list: \n")
for result_tuple in result_list:
    print(result_tuple, end="")
    if result_tuple[1] > result_tuple[2]:
        print("negative")
    else:
        print("positive")
'''