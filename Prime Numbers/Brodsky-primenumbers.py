#sabrodsky -- prime numbers code

import math

#recursive function to make sure user inputs either "determine" or "list"
def question1(user_in):
    if(user_in == "determine"):
        x = 0
    elif(user_in == "list"):
        m = input("Do you want my method or the sieve of eratosthenes? (me/eratosthenes): ")
        if(m == "me"):
            x = 1
        elif(m == "eratosthenes"):
            x = 2
        else:
            print("That is not an answer!")
            x = question1("list")
    else:
        print("That is not an answer!")
        x = question1(input("Do you want to determine if a number is prime or list out prime numbers? (determine/list): "))
    return x

#checking if the number is prime
def is_prime(funct, num):
    #if user wants to determine if a specific number is prime (will print out factors of num)
    if(funct == "determine"):
        factors = [1, num]
        #need to run through everything to get all the factors of num
        for x in range(2, int(math.sqrt(num)) + 1):
            if num%x == 0:
                factors.append(x)
                if(x != int(num/x)):
                    factors.append(int(num/x))
        return factors
    
    #if user wants to list all primes in specific range
    elif(funct == "list"):
        if(num%2 == 0):
            return False
        #needs to run up until sqrt before the factors reverse (ex. 2 * 4 --> 4 * 2)
        for x in range(3, int(math.sqrt(num)) + 2, 2):
            if num%x == 0:
                return False
        return True

#function that lists out all primes in a range set by user
def list_primes(low, high):
    primes = []
    
    #uses the is_prime function to make life easier :)
    for x in range(low, high):
        if(is_prime("list", x)):
            primes.append(x)
    return primes

#runs through a list of numbers, removing multiples while keeping primes
def sieve_of_eratosthenes(primes, tracker = 3, remove_num = []):
    #checks all numbers in list for divisibility by the tracker
    for x in range(len(primes)):
        if(primes[x]%tracker == 0 and primes[x] != tracker):
            #adds composite numbers to a different list {doesn't remove from original number list}
            remove_num.append(primes[x])
    #removing the composite numbers (based on tracker) from original number list
    for x in range(len(remove_num)):
        primes.pop(primes.index(remove_num[x]))
    print("Number list: (void: " + str(tracker) + ") " + str(primes))
    remove_num = []
    #adds an end to the recursive function or else it would go on for forever
    while(tracker < math.sqrt(primes[-1])):
        return sieve_of_eratosthenes(primes, tracker + 2, remove_num)
    else:
        #returns the original number list with all composite numbers removed
        return primes

def main():
    #determine or list
    answer1 = question1(input("Do you want to determine if a number is prime or list out prime numbers? (determine/list): "))

    #determine number
    if(answer1 == 0):
        factors = sorted(is_prime("determine", int(input("Enter a number: "))))
        #makes sure that the number is actually prime
        if(len(factors) > 2):
            print("Number Type: Composite")
        else:
            print("Number Type: Prime")
        print("Its factors are " + str(factors))

    #listing primes (my method)
    elif(answer1 == 1):
        user_range_low = int(input("Enter the least number of the range: "))
        user_range_high = int(input("Enter the greatest number of the range: "))
        print("Primes: " + str(list_primes(user_range_low, user_range_high)))

    #listing primes (sieve of eratosthenes
    elif(answer1 == 2):
        user_range_low = int(input("Enter the least number of the range: "))
        user_range_high = int(input("Enter the greatest number of the range: "))
        numbers = []
        remove_num = []
        
        #makes a list ranging for user's low and high
        for x in range(user_range_low, user_range_high + 1):
            numbers.append(x)
        print("Number list: " + str(numbers))

        #removes any even numbers
        for x in range(len(numbers)):
            if(numbers[x]%2 == 0):
                remove_num.append(numbers[x])
        for x in range(len(remove_num)):
            numbers.pop(remove_num.index(remove_num[x]))
        print("Number list (void: 2) " + str(numbers))

        #starts the recursive function
        print("Primes: " + str(sieve_of_eratosthenes(numbers)))
main()