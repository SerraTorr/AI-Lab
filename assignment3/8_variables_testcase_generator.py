import random

# candidate_literals = ("a", "~a", "b", "~b", "c", "~c", "d", "~d", "e", "~e", "f", "~f", "g", "~g") # a,b,c,d,e,f,g and their negation
candidate_literals = ("a", "b", "c", "d", "e", "f", "g")
total_no_of_testcases = int(input()) # user input

n = 4
k = 5

testcases = []
for i in range(total_no_of_testcases):
    test = ""
    for j in range(k):
        # first_index = random.randint(1,2) % 2
        # second_index = random.randint(1,8) % 8
        # while(abs(second_index - first_index) <= 1):
        #     second_index = random.randint(1,8) % 8
        # third_index = random.randint(1,8) % 8
        # while(abs(second_index - third_index) <= 1 or abs(third_index - first_index) <= 1) :
        #     third_index = random.randint(1,8) % 8
        test = ''.join([test,"("])
        for i in range(4):
            # number = random.randint(1,14) % 14
            number = random.randint(1,14) % 7
            test = ''.join([test,candidate_literals[number]])
            if i == 3:
                continue
            test = ''.join([test,"v"])

        test = ''.join([test,")"])
        test = ''.join([test,"^"])
    testcases.append(test)


for i in testcases:
    print(i[:len(i)-1])
