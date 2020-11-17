# old code
# just prints out the number of solutions
'''
coins = [1, 2, 5, 10, 20, 50, 100, 200]
goal = 200
solutions = [1] + ([0] * goal)
for coin in coins:
	for j in range(coin, goal + 1):
		solutions[j] += solutions[j - coin]

print(solutions[goal])

# https://blog.dreamshire.com/project-euler-31-solution/
# I think this code uses partitions from number theory
# I didn't go in-depth but it sounds interesting
'''