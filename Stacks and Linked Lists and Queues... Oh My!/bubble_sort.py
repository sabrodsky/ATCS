import random

def gen_list(length, mode='s'): #essentially a list.shuffle() function...
    if mode == 's':
        empty_list = []
        num_list = [num for num in range(1, length+1)] # sequential numbers

        for x in range(length):
            index = random.randint(0, len(num_list)-1)
            empty_list.append(num_list[index])
            num_list.pop(index)
  
    else:
        empty_list = [random.randint(1, 500) for num in range(length)] # random numbers

    return empty_list

def sort(data):
    for x in range(1, len(data)):
        if data[x-1] > data[x]:
            return False
    return True

def bubble(data):
    count = 0
    while sort(data) == False:
        for x in range(1, len(data)):
            if data[x-1] > data[x]:
                greater = data[x-1]
                data[x-1] = data[x]
                data[x] = greater
        count += 1
        # print("iteration {}: ".format(count), data)
    return data

random_list = gen_list(100, mode='s')
print('start: ', random_list)

random_list = bubble(random_list)
print('end: ', random_list)