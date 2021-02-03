import random

candidate_literals = ("a", "~a", "b", "~b", "c", "~c", "d", "~d") # a,b,c,d and their negation

total_no_of_testcases = int(input()) # user input

n = 4
k = 5

testcases = []
for i in range(total_no_of_testcases):
    test = ""
    for j in range(k):
        first_index = random.randint(1,8) % 8
        second_index = random.randint(1,8) % 8
        while(abs(second_index - first_index) <= 1):
            second_index = random.randint(1,8) % 8
        third_index = random.randint(1,8) % 8
        while(abs(second_index - third_index) <= 1 or abs(third_index - first_index) <= 1) :
            third_index = random.randint(1,8) % 8

        test = ''.join([test,"("])
        test = ''.join([test,candidate_literals[first_index]])
        test = ''.join([test,"v"])
        test = ''.join([test,candidate_literals[second_index]])
        test = ''.join([test,"v"])
        test = ''.join([test,candidate_literals[third_index]])
        test = ''.join([test,")"])
        test = ''.join([test,"^"])
    testcases.append(test)



for i in testcases:
    print(i[:len(i)-1])
