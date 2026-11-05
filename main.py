# ------------------------------------------------------------------------------------------------------------

# TASK 1

# ------------------------------------------------------------------------------------------------------------

import random

def random_individual(length):
    output = []
    for x in range(0, length):
        output.append(random.randint(0, 1))
    return output
        
print(random_individual(5))

# ------------------------------------------------------------------------------------------------------------

def onemax_fitness(genome):
    return sum(genome) # Fitness is simply the count of 1s.

def deceptive_fitness(genome):
    u = sum(genome)       # Unitation (number of 1s)
    L = len(genome)       # Length of genome
    
    if L - u <= 2: # Near the global optimum
        return u
    else:          # Near a less good optimum
        return L - u - 1 
    
gene = random_individual(5)
print("Gene: " + str(gene))
print("onemax_fitness: " + str(onemax_fitness(gene)))
print("deceptive_fitness: " + str(deceptive_fitness(gene)))

# ------------------------------------------------------------------------------------------------------------

def random_population(pop, length):
    output = []
    for x in range(0, pop):
        output.append(random_individual(length))

    return output

print(random_population(5, 5))
population = random_population(5, 5)

# ------------------------------------------------------------------------------------------------------------

def eval_fitness():
    output = []
    for gene in population:
        output.append(onemax_fitness(gene))

    return output

print(eval_fitness())
fitness = eval_fitness()

# ------------------------------------------------------------------------------------------------------------

def tournament(pop_size, tour_size):
    random_gene = []

    for num in range(0, tour_size):
        random_gene.append(random.randint(0, pop_size -1))

    maximum = -999
    max_index = 0

    for index in range(0, len(random_gene)):
        if fitness[random_gene[index]] >= maximum:
            maximum = fitness[random_gene[index]]
            max_index = random_gene[index]

    return max_index

population = random_population(5, 4)
fitness = eval_fitness()
print("Population: " + str(population))
print("Fitness: " + str(fitness))
print(tournament(5, 5))

# ------------------------------------------------------------------------------------------------------------

def neg_tournament(pop_size, tour_size):
    random_gene = []
    for num in range(0, tour_size):
        random_gene.append(random.randint(0, pop_size-1))

    minimum = 999
    min_index = 0

    for index in range(0, len(random_gene)):
        if fitness[random_gene[index]] <= minimum:
            minimum = fitness[random_gene[index]]
            min_index = random_gene[index]

    return min_index

population = random_population(5, 5)
fitness = eval_fitness()
print("Population: " + str(population))
print("Fitness: " + str(fitness))
print(neg_tournament(5, 3))

# ------------------------------------------------------------------------------------------------------------

def mutate(index):
    global mutation_rate

    parent = population[index]
    offspring = []
    for bit in parent:
        if random.random() < mutation_rate:
            offspring.append(1 - bit)
        else:
            offspring.append(bit)
    return offspring

mutation_rate = 1/5
index = tournament(5, 2)
print("Parent:    " + str(population[index]))
print("Offspring: " + str(mutate(index)))

# ------------------------------------------------------------------------------------------------------------

def crossover(index1, index2):
    # select parents
    parent1 = population[index1]
    parent2 = population[index2]
    
    # select crossover point
    crossPoint = random.randint(1, len(parent1) -1)
    # print(crossPoint)
    
    # perform crossover
    offspring = parent1[:crossPoint]
    offspring += parent2[crossPoint:]
    
    return offspring

index1 = tournament(5, 2)
index2 = tournament(5, 2)

print("Parent 1 : " + str(population[index1]))
print("Parent 2 : " + str(population[index2]))
print("Offspring: " + str(crossover(index1, index2)))

# ------------------------------------------------------------------------------------------------------------

def check(N):
    for gene in range(0, len(population)):
        if onemax_fitness(population[gene]) == N:
            return gene + 1
    return 0

# ------------------------------------------------------------------------------------------------------------

# BINARY GENERATIONAL GA
N = 5
M = 5
mutation_rate = 1/N
crossover_rate = random.random()
population = random_population(M, N)
fitness = eval_fitness()
generation = 0

while not check(N):
    index = tournament(M, 2)
    offspring = None
    crossover_rate = random.random()

    if crossover_rate < 1/2:
        offspring = mutate(index)
        print("MUTATE")
    else:
        offspring = crossover(index, tournament(M, 2))
        print("CROSSOVER")

    population[neg_tournament(M, 2)] = offspring
    fitness = eval_fitness()
    generation += 1

    print("Generation: " + str(generation))
    print("Offspring: " + str(offspring))
    print("Fitness: " + str(fitness))
    print("Population: " + str(population))

print("Gene: " + str(population[check(N) - 1]))

# ------------------------------------------------------------------------------------------------------------

# TASK 2 

# ------------------------------------------------------------------------------------------------------------

def phenotype(gene): #BINARY
    output = 0
    bit = 1

    for num in range(0, len(gene)):
        output += gene[num] * bit
        bit *= 2

    return output


gene = random_individual(4)
print("Gene: " + str(gene))
print(phenotype(gene))

# ------------------------------------------------------------------------------------------------------------

def phenotype_weird(gene): #NON_POSITIONAL BINARY
    output = 0
    for num in gene:
        output += num
    return output

gene = random_individual(15)
print("Gene: " + str(gene))
print(phenotype_weird(gene))

# ------------------------------------------------------------------------------------------------------------

def eval_fitness_pheno(): # 15-MAX
    output = []
    for gene in population:
        output.append(phenotype(gene))
    
    return output


population = random_population(5, 4)
print("Population: " + str(population))
print("Phenotype: " + str(eval_fitness_pheno()))

# ------------------------------------------------------------------------------------------------------------

def soft_eval_fitness_pheno(fitness):
    sum = 0
    for num in fitness:
        sum += num
    
    return sum / len(fitness)

population = random_population(5, 4)
fitness = eval_fitness_pheno()
print("Population: " + str(population))
print("Fitness: " + str(fitness))
print("Soft Phenotype: " + str(soft_eval_fitness_pheno(fitness)))

# ------------------------------------------------------------------------------------------------------------

def check_pheno():
    for gene in range(0, len(population)):
        if phenotype(population[gene]) == 15:
            return gene + 1
    return 0 

# ------------------------------------------------------------------------------------------------------------

# TASK 3 

# ------------------------------------------------------------------------------------------------------------

# 15-MAX GA
N = 4
M = 5
mutation_rate = 1/N
crossover_rate = random.random()
population = random_population(M, N)
fitness = eval_fitness_pheno()
generation = 0

while not check_pheno():
    index = tournament(M, 3)
    offspring = None
    crossover_rate = random.random()

    if crossover_rate < 1/2:
        offspring = mutate(index)
        print("MUTATE")
    else:
        offspring = crossover(index, tournament(M, 3))
        print("CROSSOVER")

    population[neg_tournament(M, 3)] = offspring
    fitness = eval_fitness_pheno()
    generation += 1

    print("Generation: " + str(generation))
    print("Offspring: " + str(offspring))
    print("Fitness: " + str(fitness))
    print("Population: " + str(population))

print("Gene: " + str(population[check_pheno() - 1]))

# ------------------------------------------------------------------------------------------------------------

# SOFT 15-MAX GA
N = 4
M = 5
mutation_rate = 1/N
crossover_rate = random.random()
population = random_population(M, N)
fitness = eval_fitness_pheno()
generation = 0

while not soft_eval_fitness_pheno(fitness) == 15:
    index = tournament(M, 3)
    offspring = None
    crossover_rate = random.random()

    if crossover_rate < 1/2:
        offspring = mutate(index)
        print("MUTATE")
    else:
        offspring = crossover(index, tournament(M, 3))
        print("CROSSOVER")

    population[neg_tournament(M, 3)] = offspring
    fitness = eval_fitness_pheno()
    generation += 1

    print("Generation: " + str(generation))
    print("Offspring: " + str(offspring))
    print("Fitness: " + str(fitness))
    print("SOFT FITNESS: " + str(soft_eval_fitness_pheno(fitness)))
    print("Population: " + str(population))

print("FINAL POPULATION: " + str(population))

# ------------------------------------------------------------------------------------------------------------

# TASK 5

# ------------------------------------------------------------------------------------------------------------

# Simulator of program execution (GP interpreter) 
# program = sequence of integers 
# x = input variable 
def execute(program, x): 
 
    # A place where to get arguments for operations and  
    # for storing their results 
    stack = []  
 
    # If l = [1,2,3], l.pop() removes 3 from the list and returns it 
    # but if l = [], l.pop() gives an error 
    # Fixing the problem for stack by defining our own pop() 
    def pop(): 
        if not stack: 
            return 0 
        return stack.pop() 
 
    # Main execution loop 
    for instr in program: 
        if instr == 0:   # NOP 
            pass 
        elif instr == 1: # X 
            stack.append(x) 
        elif instr == 2: # + 
            stack.append(pop() + pop()) 
        elif instr == 3: # - 
            stack.append(pop() - pop()) 
        elif instr == 4: # * 
            stack.append(pop() * pop()) 
        elif instr == 5: # 1  
            stack.append(1) 
        elif instr == 6: # -1  
            stack.append(-1) 
        else:            # 0 
            stack.append(0) 
 
    # Returning the very last result appended to stack 
    return pop()

print(execute([5, 1, 2], 3))

# ------------------------------------------------------------------------------------------------------------

# TASK 6

# ------------------------------------------------------------------------------------------------------------

def to_bytes(gene, no_inst, byte_size):
    output = []

    for num in range(0, no_inst):
        # print(num)
        output.append(gene[num * byte_size : (num * byte_size) + byte_size])

    return output

gene = random_individual(5 * 3)
print(gene)
print(to_bytes(gene, 5, 3))

# ------------------------------------------------------------------------------------------------------------

def to_program(no_inst, byte_size):

    program = []

    for gene in population:
        program.append(to_bytes(gene, no_inst, byte_size))

    return program

population = random_population(5, 5 *3)
print("Population: " + str(population))
print(to_program(5, 3))

# ------------------------------------------------------------------------------------------------------------

def program_phenotype(program):
    output = []

    for gene in program:

        instruction = []

        for num in gene:
            instruction.append(phenotype(num))

        output.append(instruction)

    return output

population = random_population(5, 5 *3)
program = to_program(5, 3)
print("Population: " + str(population))
print(program_phenotype(program))

# ------------------------------------------------------------------------------------------------------------

def execute_program(instruction, program_input):
    output = []

    for inst in instruction:
        output.append(execute(inst, program_input))

    return output

population = random_population(5, 5*3)
program = to_program(5, 3)
instructions = program_phenotype(program)

print("Population: " + str(population))
print("Instructions: " + str(instructions))
print(execute_program(instructions, -1))

# ------------------------------------------------------------------------------------------------------------

def best(fitness, input_variable):
    bool = input_variable + 1

    best_num = fitness[0]
    best_index = 0

    for index in range(0, len(fitness)):

        if not bool: # -1
            if fitness[index] <= best_num:
                best_num = fitness[index]
                best_index = index
        else: # 1
            if fitness[index] >= best_num:
                best_num = fitness[index]
                best_index = index
    
    return best_index

input_variable = -1
population = random_population(5, 5*3)
program = to_program(5, 3)
instructions = program_phenotype(program)
fitness = execute_program(instructions, input_variable)

print("Fitness: " + str(fitness))
print(best(fitness, input_variable))

# ------------------------------------------------------------------------------------------------------------

def generate_offspring(crossover_rate, index, input_variable, tournament_size):
    offspring = None

    if crossover_rate < 5/8:
        offspring = mutate(index)
        # print("MUTATE")
    else:
        # print("CROSSOVER")

        bool = input_variable + 1

        if not bool: # -1
            offspring = crossover(index, neg_tournament(M, tournament_size))
        else: # 1
            offspring = crossover(index, tournament(M, tournament_size))
        
    return offspring

# ------------------------------------------------------------------------------------------------------------

# PROBLEM 1 

def problem_1(input_variable):

    best_fitness = 0
    best_gene = None
    best_instruction = None

    best_of_best = []

    for gen in range(0, generation_limit):
        offspring = None
        crossover_rate = random.random()

        bool = input_variable + 1

        if not bool: # -1
            index = neg_tournament(M, T)
            offspring = generate_offspring(crossover_rate, index, input_variable, T)
            population[tournament(M, T)] = offspring
        else: # 1
            index = tournament(M, T)
            offspring = generate_offspring(crossover_rate, index, input_variable, T)
            population[neg_tournament(M, T)] = offspring

        program = to_program(no_inst, byte_size)
        instructions = program_phenotype(program)
        fitness = execute_program(instructions, input_variable)


        # STORE BEST VALUES FOUND SO FAR
        best_index = best(fitness, input_variable)

        if not bool and fitness[best_index] < best_fitness: # -1
            best_fitness = fitness[best_index]
            best_gene = population[best_index]
            best_instruction = instructions[best_index]
        if bool and fitness[best_index] > best_fitness: # 1
            best_fitness = fitness[best_index]
            best_gene = population[best_index]
            best_instruction = instructions[best_index]

        
        best_of_best.append(best_fitness)
        # print("======= Generation: " + str(gen) + " ==========")
        # print("Offspring: " + str(offspring))
        # print("Fitness: " + str(fitness))
        # print("Population: " + str(population))
        # print("Instructions: " + str(instructions))
    
    # print("============== BEST VALUES FOUND: ==============")
    # print("Best Fitness: " + str(best_fitness))
    # print("Best Gene: " + str(best_gene))
    # print("Best Instructions: " + str(best_instruction))

    return best_of_best

byte_size = 3 # Bits
no_inst = 20 # No of Instructions

N = no_inst * byte_size  # Gene Length
M = 5 # Population Size
T = 4 # Tournament Size

mutation_rate = 3/N
crossover_rate = random.random()
population = random_population(M, N)
program = to_program(no_inst, byte_size)
instructions = program_phenotype(program)
fitness = execute_program(instructions, 1)
generation_limit = 10000

problem_1(1)
problem_1(-1)

# ------------------------------------------------------------------------------------------------------------

best_instruction = [[1, 6, 3, 1, 3, 2, 5, 5, 2, 4, 5, 6, 1, 3, 2, 4, 5, 5, 2, 4]]
print("Length: " + str(len(best_instruction[0])))
print("Result: " + str(execute_program(best_instruction, 1)))

# ------------------------------------------------------------------------------------------------------------

# TASK 7

# ------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt

inputs = [1, -1]

iterations = 15

byte_size = 3 # Bits
no_inst = 0 # No of Instructions

change = [5, 10, 20]
titles = ["No. Instructions: 5", "No. Instructions: 10", "No. Instructions: 20"]

generation_limit = 50

stats = []

for input_index in range(0, len(inputs)):

    per_input = []

    for inst_index in range(0, len(change)):

        no_inst = change[inst_index]
        program_output = []


        print("Input Variable: " + str(inputs[input_index]))
        print("No. Of Instructions: " + str(no_inst))

        for iteration in range(0, iterations):

            N = no_inst * byte_size  # Gene Length
            M = 50 # Population Size
            T = 100 # Tournament Size

            mutation_rate = 10/N
            crossover_rate = random.random()
            population = random_population(M, N)
            program = to_program(no_inst, byte_size)
            instructions = program_phenotype(program)
            fitness = execute_program(instructions, inputs[input_index])
            
            results = problem_1(inputs[input_index])

            plt.subplot(3, 5, iteration+1)
            plt.plot(results)

            program_output.append(results[len(results)-1])

        per_input.append(program_output)
            
        # plt.subplot(2, 1, 2)

        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.show()

    stats.append(per_input)

# ------------------------------------------------------------------------------------------------------------

# print(stats)
for input_index in range(0, len(stats)): # SCATTER GRAPH
    x = []
    y = []
    for instr in range(0, len(stats[input_index])):
        for num in stats[input_index][instr]:
            x.append(change[instr])
            y.append(num)

    plt.scatter(x, y)
    plt.xlabel("No. Instructions")
    plt.ylabel("Fitness")
    plt.show()

# ------------------------------------------------------------------------------------------------------------

import math

# https://www.google.com/search?q=how+to+calculate+standard+deviation&rlz=1C1CHBF_en-GBGB879GB879&oq=how+to+calculate+stand&gs_lcrp=EgZjaHJvbWUqCggAEAAYsQMYgAQyCggAEAAYsQMYgAQyBwgBEAAYgAQyBggCEEUYOTIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDM4NzdqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
def standard_deviation(data):
    mean = 0
    for num in data:
        mean += num
    mean = mean / len(data)

    divations = data[:]
    for div in range(0, len(divations)):
        divations[div] = (divations[div] - mean) ** 2

    sum = 0
    for div in divations:
        sum += div

    varience = sum / (len(divations) -1)

    return math.sqrt(varience)

for input_index in range(0, len(stats)):
    for instr in range(0, len(stats[input_index])):
        print("Input: " + str(inputs[input_index]))
        print("No. of Instructions: " + str(change[instr]))
        print(stats[input_index][instr])
        print("Standard Deviation: " + str(standard_deviation(stats[input_index][instr])))

# ------------------------------------------------------------------------------------------------------------

# TASK 6 PROBLEM 2

# ------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt

x = [-1, -.9, -.8, -.7, -.6, -.5, -.4, -.3, -.2, -.1, 0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1]
print(len(x))

y = []

for num in x:
    y.append(2 * num**5 + 4 * num**4 + 6 * num**3 + 8 * num**2 + 10 * num + 1)

plt.plot(x, y)
plt.show()

# ------------------------------------------------------------------------------------------------------------

def polynomial_fitness(program_output, input_index):
    target = y[input_index]

    output = []

    for out in program_output:
        # Calc to how close it is
        if out > target:
            output.append(out - target)
        else:
            output.append(target - out)

    return output

input_index = 0

population = random_population(5, 5*3)
program = to_program(5, 3)
instructions = program_phenotype(program)
program_output = execute_program(instructions, x[input_index])
fitness = polynomial_fitness(program_output, input_index)


print("Input variable: " + str(x[input_index]))
print("Expected value: " + str(y[input_index]))
print("Population: " + str(population))
print("Output: " + str(program_output))
print("Fitness: " + str(fitness))

# ------------------------------------------------------------------------------------------------------------

# Problem 2

def problem_2():

    global crossover_rate, population, program, instructions, program_output, fitness, best_fitness, best_outcome, best_instruction
    
    best_of_best = []

    for input_index in range(0, len(x)):

        input_variable = x[input_index]

        crossover_rate = random.random()
        population = random_population(M, N)
        program = to_program(no_inst, byte_size)
        instructions = program_phenotype(program)
        program_output = execute_program(instructions, input_variable)
        fitness = polynomial_fitness(program_output, input_index)

        best_fitness = 999
        best_outcome = None
        best_instruction = None

        for gen in range(0, generation_limit):
            offspring = None
            crossover_rate = random.random()

            index = neg_tournament(M, T)

            if crossover_rate < 1/2:
                offspring = mutate(index)
            else:
                offspring = crossover(index, neg_tournament(M, T))

            population[tournament(M, T)] = offspring
            program = to_program(no_inst, byte_size)
            instructions = program_phenotype(program)
            program_output = execute_program(instructions, input_variable)
            fitness = polynomial_fitness(program_output, input_index)


            # STORE BEST VALUES FOUND SO FAR
            best_index = best(fitness, -1) # -1 for best lowest score

            if fitness[best_index] < best_fitness:
                best_fitness = fitness[best_index]
                best_outcome = program_output[best_index]
                best_instruction = instructions[best_index]
                

            

            # print("======= Generation: " + str(gen) + " ==========")
            # print("Population: " + str(population))
            # print("Instructions: " + str(instructions))
            # print("Output: " + str(program_output))
            # print("Fitness: " + str(fitness))

        

        best_of_best.append(best_outcome)
        # print("============== BEST VALUES FOUND: ==============")
        # print("Exected Value: " + str(y[input_index]))
        # print("Best Outcome: " + str(best_outcome))
        # print("Fitness: " + str(best_fitness))
        # print("Best Instructions: " + str(best_instruction))

    # print(y)
    # print(best_of_best)
    return best_of_best

byte_size = 3 # Bits
no_inst = 21 # No of Instructions

N = no_inst * byte_size  # Gene Length
M = 100 # Population Size
T = 50 # Tournament Size

mutation_rate = 5/N
generation_limit = 50

crossover_rate = random.random()
population = random_population(M, N)
program = to_program(no_inst, byte_size)
instructions = program_phenotype(program)
program_output = execute_program(instructions, x[0])
fitness = polynomial_fitness(program_output, 0)

best_fitness = 999
best_outcome = None
best_instruction = None

problem_2()

# ------------------------------------------------------------------------------------------------------------

# TASK 7

# ------------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt

iterations = 15

byte_size = 3 # Bits
no_inst = 21 # No of Instructions

generation_limit = 50

stats = []

for iteration in range(0, iterations):

    N = no_inst * byte_size  # Gene Length
    M = 100 # Population Size
    T = 50 # Tournament Size

    crossover_rate = random.random()
    population = random_population(M, N)
    program = to_program(no_inst, byte_size)
    instructions = program_phenotype(program)
    program_output = execute_program(instructions, x[0])
    fitness = polynomial_fitness(program_output, 0)

    best_fitness = 999
    best_outcome = None
    best_instruction = None
    
    results = problem_2()

    stats.append(results)

    plt.subplot(3, 5, iteration+1)

    plt.plot(x, y, color="tab:blue")
    plt.plot(x, results, color="tab:red")

plt.xlabel("Input Variable")
plt.ylabel("Fitness")
plt.show()

# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/shared_axis_demo.html

# ------------------------------------------------------------------------------------------------------------

x_axis = []
y_axis = []

for perm in stats:
    for num in range(0, len(perm)):
        y_axis.append(perm[num])
        x_axis.append(x[num])

plt.scatter(x_axis, y_axis)
plt.xlabel("Input Variable")
plt.ylabel("Program Output")
plt.show()

# ------------------------------------------------------------------------------------------------------------

sorted_stats = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

def mean(data):
    sum = 0
    for num in data:
        sum += num
    return sum/len(data)

for perm in stats:
    for num in range(0, len(perm)):
        sorted_stats[num].append(perm[num])

difference = []

for x_input in range(0, len(x)):
    print("==== Input Variable: " + str(x[x_input]) + " ====")
    print("Expected Output: " + str(y[x_input]))
    print("Mean Output: " + str(mean(sorted_stats[x_input])))
    print("Standard Deviation: " + str(standard_deviation(sorted_stats[x_input])))
    diff = y[x_input] - mean(sorted_stats[x_input])
    print("Difference between mean & expected: " + str(diff))
    difference.append(diff)
    print("")

# ------------------------------------------------------------------------------------------------------------

plt.bar(x, difference)
plt.show()