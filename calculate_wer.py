#!/usr/bin/env python
import numpy
import argparse

    #Calculation of WER with Levenshtein distance.

def dis_matrix(original_words,transcribed_words):


    # initialisation

    substitution = []
    insertion = []
    deletion = []
    original_words_len = len(original_words)
    transcribed_words_len = len(transcribed_words)

    distance_matrix = numpy.zeros((original_words_len+1)*(transcribed_words_len+1), dtype=numpy.uint8)
    distance_matrix = distance_matrix.reshape((original_words_len+1, transcribed_words_len+1))

    for i in range(original_words_len+1):
        for j in range(transcribed_words_len+1):
            if i == 0:
                distance_matrix[0][j] = j
            elif j == 0:
                distance_matrix[i][0] = i


    # computation
    for x in range(1, original_words_len+1):
        for y in range(1, transcribed_words_len+1):
            if original_words[x-1] == transcribed_words[y-1]:
                distance_matrix[x][y] = distance_matrix[x-1][y-1]
            else:
                substitution = distance_matrix[x-1][y-1] + 1
                insertion    = distance_matrix[x][y-1] + 1
                deletion     = distance_matrix[x-1][y] + 1
                distance_matrix[x][y] = min(substitution, insertion, deletion)
    return distance_matrix
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Calculate Word error rate ")
    parser.add_argument('path1', type=str, help=' Original txt path.')
    parser.add_argument('path2', type=str, help=' Transcribed txt path.')
    args = parser.parse_args()

    original_file = open(args.path1)
    transcribed_file = open(args.path2)

    r1 = original_file.read()
    r2 = transcribed_file.read()
    r1 = r1.lower()
    r2 = r2.lower()
    sign = ".? ""-,"
    for char in sign:
        r1 = r1.replace(char, " ")
        r2 = r2.replace(char, " ")
    r1  = r1.replace("\n"," ")
    r2 = r2.replace("\n"," ")

    original_words = r1.split()
    transcribed_words = r2.split()




    distance_matrix = dis_matrix(original_words,transcribed_words)
    print("Shape of the matrix ")
    print(distance_matrix.shape)
    x = distance_matrix.shape[0]-1
    y = distance_matrix.shape[1]-1

    substitute = 0
    delete = 0
    insert = 0


    while(True):
        if(x == 0 or y==0):
            break

        if (original_words[x - 1] == transcribed_words[y - 1]):
            x = x-1
            y = y-1
        elif(distance_matrix[x][y]==distance_matrix[x-1][y-1]+1):
            #print("substitute: " + str2[j - 1] + " in string2 to " + str1[i - 1] + " in string1");

            substitute += 1
            x = x-1
            y = y-1
        elif (distance_matrix[x][y] == distance_matrix[x][y - 1] + 1):
            delete += 1

            y = y-1
        elif (distance_matrix[x][y] == distance_matrix[x - 1][y] + 1):
            x = x-1
            insert += 1

    print("Number of substitute: %d "% substitute)
    print("Number of delete : %d" % delete)
    print("Number of insert: %d" % insert)
    word_error_rate = ((substitute+delete+insert)/len(original_words))*100

    print("The word error rate : %d %s"%(word_error_rate,"%"))