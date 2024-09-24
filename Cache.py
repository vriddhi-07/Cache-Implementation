import math
import matplotlib.pyplot as plt

# Function to initialize the cache
def initialize_cache(cache_size_kb, block_size_bytes, associativity):

    cache_size = cache_size_kb * 1024            # Convert cache size from KB to bytes
    num_blocks = cache_size // block_size_bytes  # calculating the no. of blocks in the cache
    num_sets = num_blocks // associativity       # calculating the no. of sets in the cache

    # Initialize cache with sets and ways
    cache = []

    for i in range(num_sets):
        
        set_list = []    # set list has all the blocks of one particular set

        for j in range(associativity):  # Iterating over each way of the current set
            
            line = {'tag': None, 'valid': 0, 'lru': 0}   # Creating a dictionary with the default values of each block
            set_list.append(line)
        
        cache.append(set_list)    # Adding the current set to the cache
    
    return cache, num_sets, associativity


# Function to calculate the index and tag from the address
def get_index_and_tag(address, block_size, num_sets):

    block_offset_bits = int(math.log2(block_size))    # no. of bits in block offset
    index_bits = int(math.log2(num_sets))             # no. of bits in index
    tag_bits = 32 - index_bits - block_offset_bits    # no. of bits in tag

    address = '0' * (32 - len(address)) + address              # making the address 32 bits
    tag = int(address[0:tag_bits], 2)                          # getting tag from binary address and converting it to decimal 
    index = int(address[tag_bits:tag_bits+index_bits], 2)      # getting index from binary address and converting it to decimal
    
    return index, tag


# Function to access cache and return true for hit, false for miss
def access_cache(address, cache, block_size, num_sets, associativity):

    index, tag = get_index_and_tag(address, block_size, num_sets)      #getting index and tag
    set_cache = cache[index]         # getting the list of blocks for the set with the corresponding index

    for i in range(associativity):   # Iterating through all the blocks of the set
        
        if set_cache[i]['valid'] == 1 and set_cache[i]['tag'] == tag:   # checking if the valid bit of the block is set and there's a tag match
            
            update_lru(cache, index, i, associativity)     # update the lru count of the set
            return True  # cache hit so return true

    replace_lru(index, tag, cache, associativity)   # Cache miss, replace the data in the least recently used block with the new data
    return False  # cache miss so return false


# Function to update the LRU count in a set
def update_lru(cache, index, accessed_way, associativity):

    set_cache = cache[index]     # getting the set whose lru counts have to be updated
    set_cache[accessed_way]['lru'] = associativity - 1    # updating the lru count of the most recently accessed block

    for i in range(associativity):   #Iterating through the set to update the lru counts of the other blocks

        if i!=accessed_way and set_cache[i]['lru']!=0:    # if the lru is not already 0
            set_cache[i]['lru'] -= 1                      # decrement the lru count by 1


# Function to replace the LRU block in case of a cache miss
def replace_lru(index, tag, cache, associativity):

    set_cache = cache[index]

    for i in range(associativity):    #Iterating through each block of the set

        if set_cache[i]['lru'] == 0:    # if it's the least recently used block

            set_cache[i]['tag'] = tag    # replace the tag
            set_cache[i]['valid'] = 1    # change the valid bit to 1
            accessed_way = i             # index of the block being replaced in set_cache
            break

    update_lru(cache, index, accessed_way, associativity)   # Update the LRU count for the set


# Function to convert hexadecimal string to binary string
def hex_to_bin(hex_string):

    n = int(hex_string, 16) 
    binary_str = '' 
    while n > 0: 
        binary_str = str(n % 2) + binary_str 
        n = n >> 1   
    return binary_str 


# Function to simulate the cache for a trace file
def simulate_cache(cache_size_kb, block_size_bytes, associativity, trace_file):

    cache, num_sets, assoc = initialize_cache(cache_size_kb, block_size_bytes, associativity)    # initialise the cache
    total_accesses = 0
    hits = 0

    # Read the trace file and process each address
    with open(trace_file, 'r') as file:

        for line in file:

            parts = line.strip().split()    # getting a list of all the words in a line
            address = hex_to_bin(parts[1])  # Converting the hex memory address to binary
            total_accesses += 1

            if access_cache(address, cache, block_size_bytes, num_sets, assoc):   # if it's a cache hit
                hits += 1       # increment the no. of hits

    hit_rate = hits / total_accesses     # Calculating hit rate
    miss_rate = 1 - hit_rate             # Calculating miss rate
    return hit_rate, miss_rate

# Function to plot the cumulative graph
def plot_results_all(trace_files, x_values, miss_rates, x_label, title):

    plt.figure()

    for trace, miss_rate in miss_rates.items():
        plt.plot(x_values, miss_rate, label = f'Trace File: {trace_files[trace]}')

    plt.xlabel(x_label)

    if(x!="4"): 
        plt.ylabel('Miss Rate') #graph should plot miss rate for the other problems

    else:
        plt.ylabel('Hit Rate') #graph to plot hit rate for problem 4

    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()
        
# Function to plot the graph
def plot_results(trace_file, x_values, miss_rates, x_label, title):

    plt.figure()

    for trace, miss_rate in miss_rates.items():
        plt.plot(x_values, miss_rate, label = f'Trace File: {trace_file}')

    plt.xlabel(x_label)

    if(x!="4"): 
        plt.ylabel('Miss Rate') #graph should plot miss rate for the other problems

    else:
        plt.ylabel('Hit Rate') #graph to plot hit rate for problem 4

    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()
        
# ----------------------------------------Functions for each experiment-----------------------------------------------------------------

# Function for part (a)
def cache_simulation_for_1024(trace_files, cache_size, block_size, associativity):

    for trace_file in trace_files:

        hit_rate, miss_rate = simulate_cache(cache_size, block_size, associativity, trace_file)
        print(f"Trace File: {trace_file}, Hit Rate {1-miss_rate:.4f}, Miss Rate: {miss_rate:.4f}")

# Function to display seperate results for each trace file in part (b)
def varying_cache_size(trace_files, cache_sizes, block_size, associativity):

    for trace_file in trace_files: # iterating through each trace file

        for cache_size in cache_sizes: # iterating through diff cache sizes

            hit_rate, miss_rate = simulate_cache(cache_size, block_size, associativity, trace_file)
            miss_rates_cache_size[cache_size] = miss_rate
            print(f"Trace File: {trace_file}, Cache Size: {cache_size}KB, Hit Rate {1-miss_rate:.4f}, Miss Rate: {miss_rate:.4f}")

        plot_results(trace_file, cache_sizes, {'Trace': list(miss_rates_cache_size.values())}, 'Cache Size (KB)', 'Miss Rate vs Cache Size')

# Function to display seperate results for each trace file in part (c)
def varying_block_size(trace_files, cache_size, block_sizes, associativity):

    for trace_file in trace_files:  # iterating through each trace file

        for block_size in block_sizes: # iterating through diff block sizes

            hit_rate, miss_rate = simulate_cache(cache_size, block_size, associativity, trace_file)
            miss_rates_block_size[block_size] = miss_rate
            print(f"Trace File: {trace_file}, Block Size: {block_size} bytes, Hit Rate {1-miss_rate:.4f}, Miss Rate: {miss_rate:.4f}")

        plot_results(trace_file, block_sizes, {'Trace': list(miss_rates_block_size.values())}, 'Block Size (Bytes)', 'Miss Rate vs Block Size')

# Function to display seperate results for each trace file in part (d)
def varying_associativity(trace_files, cache_size, block_size, associativities):

    for trace_file in trace_files:  # iterating through each trace file

        for associativity in associativities: #  iterating through diff associativities

            hit_rate, miss_rate = simulate_cache(cache_size, block_size, associativity, trace_file)
            miss_rates_associativity[associativity] = miss_rate
            hit_rates_associativity[associativity] = hit_rate
            print(f"Trace File: {trace_file}, Associativity: {associativity}-way,Hit Rate {1-miss_rate:.4f}, Miss Rate: {miss_rate:.4f}")

        plot_results(trace_file, associativities, {'Trace': list(hit_rates_associativity.values())}, 'Associativity (ways)', 'Hit Rate vs Associativity')

# Fuction to display cumulative result for all trace files in part (b)
def varying_cache_size_all(miss_rates_cache_size,cache_sizes,block_size, associativity):

    for trace in range(0, 5):   # iterating through each trace file

        miss_rates_cache_size[trace] = []
        for cache_size in cache_sizes:   # iterating through diff cache sizes

            hit_rate, miss_rate = simulate_cache(cache_size, block_size, associativity, f'{trace_files[trace]}')  # Block size = 4 bytes, associativity = 4-way
            miss_rates_cache_size[trace].append(miss_rate)

        print(f"Trace file: {trace_files[trace]}", f"Hit rate: {hit_rate:.4f}", f"Miss rate: {miss_rate:.4f}")

    plot_results_all(trace_files, cache_sizes, miss_rates_cache_size, 'Cache Size (KB)', 'Miss Rate vs Cache Size')

# Fuction to display cumulative result for all trace files in part (c)
def varying_block_size_all(miss_rates_block_size, cache_size, block_sizes, associativity):

    for trace in range(0, 5):    # iterating through each trace file

        miss_rates_block_size[trace] = []
        for block_size in block_sizes:  # iterating through diff block sizes

            hit_rate, miss_rate = simulate_cache(cache_size, block_size, associativity, f'{trace_files[trace]}') 
            miss_rates_block_size[trace].append(miss_rate)

        print(f"Trace file: {trace_files[trace]}", f"Hit rate: {hit_rate:.4f}",f"Miss rate: {miss_rate:.4f}")

    plot_results_all(trace_files, block_sizes, miss_rates_block_size, 'Block Size (Bytes)', 'Miss Rate vs Block Size')

# Fuction to display cumulative result for all trace files in part (d)

def varying_associativity_all(trace_files, cache_size, block_size, associativities):

    for trace in range(0, 5):       # iterating through each trace file

        miss_rates_associativity[trace] = []
        hit_rates_associativity[trace] = []
        for associativity in associativities:   # iterating through diff associativities

            hit_rate, miss_rate = simulate_cache(cache_size, block_size, associativity, f'{trace_files[trace]}') 
            miss_rates_associativity[trace].append(miss_rate)
            hit_rates_associativity[trace].append(hit_rate)

        print(f"Trace file: {trace_files[trace]}",f"Hit rate: {hit_rate:.4f}",f"Miss rate: {miss_rate:.4f}")

    plot_results_all(trace_files, associativities, hit_rates_associativity, 'Associativity (ways)', 'Hit Rate vs Associativity')

# -----------------------------------------------------------main-------------------------------------------------------------------------

# List of trace files
trace_files = ['gcc.trace', 'gzip.trace', 'mcf.trace', 'swim.trace', 'twolf.trace']  # Add all your trace files here

x = input("Enter which program you want to run:\n"
          "1. 4-way set associative cache of size 1024KiB\n"
          "2. Varying cache sizes\n"
          "3. Varying block size\n"
          "4. Varying associativity\n"
          "Choose an option (1/2/3/4): ")

# Part (a)
if x == '1':
    cache_size = 1024
    block_size = 4    # 4 bytes 
    associativity = 4
    cache_simulation_for_1024(trace_files, cache_size, block_size, associativity)


if(x!="1"):
    y=input('''Enter your preference:\n1. Plot the graphs seperately for each input file\n2. Plot the graph of all the input files together\n''')

# Part (b)
# plot miss rate and cache size

if x == '2':
    cache_sizes = [128, 256, 512, 1024, 2048, 4096] #list of cache sizes
    miss_rates_cache_size = {}
    block_size = 4    # 4 bytes 
    associativity = 4

    if(y=="1"): #individual graph
        varying_cache_size(trace_files, cache_sizes, block_size, associativity)

    elif(y=="2"): #cumulative graph
        varying_cache_size_all(miss_rates_cache_size,cache_sizes,block_size, associativity)

    
# Part (c)
# plot miss rate vs block size

elif x == '3':

    block_sizes = [1, 2, 4, 8, 16, 32, 64, 128] #list of block sizes
    miss_rates_block_size = {}
    cache_size = 1024    # 1024KB
    associativity = 4

    if(y=="1"): #individual graph
        varying_block_size(trace_files, cache_size, block_sizes, associativity)

    elif(y=="2"): #cumulative graph
        varying_block_size_all(miss_rates_block_size, cache_size, block_sizes, associativity)

# Part (d)
# plot variation of hit rates vs associativity

elif x == '4':

    associativities = [1, 2, 4, 8, 16, 32, 64]  #list of associativities
    miss_rates_associativity = {}
    hit_rates_associativity = {}
    cache_size = 1024    # 1024KB
    block_size = 4

    if(y=="1"): #individual graph
        varying_associativity(trace_files, cache_size, block_size, associativities)

    elif(y=="2"): #cumulative graph
        varying_associativity_all(trace_files, cache_size, block_size, associativities)




            

