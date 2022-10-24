import pandas as pd

import time
start_time = time.time()

# ###############
# Global Variable
# ###############
x_axis_count = 100
y_axis_count = 100
x_counter = 0
y_counter = 0
nbr_of_record_per_cell = 10000
number_range_config_file = 'BP_Numbers.txt'
matrix_file_name = 'matrix_data.txt'
label_matrix_file_name = 'matrix_label.txt'
system_in_scope = 'MSS'

# ######################################################
# Looping thru data frame rows containing Number ranges
# ######################################################
df_nbr_range = pd.read_csv(('./DATA/{}').format(number_range_config_file), sep='\t', header=None)
df_nbr_range = df_nbr_range.reset_index()  # make sure indexes pair with number of rows
v_start_nbr = 0
v_end_nbr = 0
df_nbr_range.columns = ['index', 'system', 'nbr_object', 'from_nbr', 'to_nbr']

# #########################################################
# Function which tells if the numbers are inside or outside
# the defined list of number range.
# #########################################################
def determine_inside_outside_nbr_range(start_nbr_range: int,
                                       end_nbr_range: int,
                                       actual_number: int):
    r = range(start_nbr_range, end_nbr_range)
    if actual_number in r:
        print("Inside the range")
        return 1
    else:
        print("Outside the range")
        return 0

# #########################################################
# Version 2
# Function which tells if the numbers are inside or outside
# the defined list of number range.
# #########################################################
def determine_inside_outside_nbr_range_v2(start_nbr_range: int,
                                          end_nbr_range: int,
                                          actual_start_nbr: int,
                                          actual_end_nbr):
    x = range(start_nbr_range, end_nbr_range)
    y = range(actual_start_nbr, actual_end_nbr)
    xs = set(x)
    return bool(xs.intersection(y))

# #########################################################
# Version 3
# Function which tells if the numbers are inside or outside
# the defined list of number range.
# #########################################################
def determine_inside_outside_nbr_range_v3(a: int, b: int, x: int, y: int):
    # Initialize the variable
    is_overlap = False
    if b <= x:
        is_overlap = False
        return is_overlap
    elif a >= y:
        is_overlap = False
        return is_overlap
    elif (a >= x and a < y):
        is_overlap = True
        return is_overlap
    elif a <= x and b > x and b >= y:
        is_overlap = True
        return is_overlap
    elif a >= x and a < y and b >= y:
        is_overlap = True
        return is_overlap
    elif (a <= x and b > x and b <= y):
        is_overlap = True
        return is_overlap
    else:
        return is_overlap

# ###########################################################################################
# Version - 4
# In this version we will loop through all the configured number range and evaluate against
# the 2 input values (start & end number) set and see if it falls into any of the range.
# If it finds one instance where it falls then just come out of the loop and return as match
# found. The program needs to be very efficient otherwise it will slow down the entire program.
# ###########################################################################################
def determine_inside_outside_nbr_range_v4(x: int, y: int):
    # Initialize the variable
    is_overlap = False

    for index, row in df_nbr_range.iterrows():
        if row['system'] == ('{}').format(system_in_scope):
            v_start_nbr = row['from_nbr']
            v_end_nbr = row['to_nbr']
            if (v_end_nbr <= x):
                is_overlap = False
                continue
            elif (v_start_nbr >= y):
                is_overlap = False
                continue
            elif (v_start_nbr >= x and v_start_nbr < y):
                is_overlap = True
                break
            elif (v_start_nbr <= x and v_end_nbr > x and v_end_nbr >= y):
                is_overlap = True
                break
            elif (v_start_nbr >= x and v_start_nbr < y and v_end_nbr >= y):
                is_overlap = True
                break
            elif (v_start_nbr <= x and v_end_nbr > x and v_end_nbr <= y):
                is_overlap = True
                break
            else:
                is_overlap = False

    return is_overlap, index, row['system'], row['nbr_object']

# #########################################################
# Function which tells which block it's in based on
# counter. Block size is maintained in static variable
# #########################################################
def determine_start_number_range(running_cell_number: int):
    return running_cell_number * nbr_of_record_per_cell

with open(('./DATA/{}-{}').format(system_in_scope, matrix_file_name), 'w') as f1, open(('./DATA/{}-{}').format(system_in_scope, label_matrix_file_name), 'w') as f2:
    for i in range(x_axis_count):
        for j in range(y_axis_count):
            y_counter += 1
            block_size = determine_start_number_range(y_counter)
            begin_block_nbr = block_size - nbr_of_record_per_cell
            end_block_nbr = block_size - 1
            is_there_overlap, myindex, mySystem, myNbrObject = determine_inside_outside_nbr_range_v4(begin_block_nbr, end_block_nbr)

            if (j < (y_axis_count - 1) and is_there_overlap):
                f1.write(("{}, ").format(myindex))
                f2.write(str(mySystem) + " : " + str(myNbrObject) + " : " + str(begin_block_nbr) + " - " + str(end_block_nbr) + ",")
                continue
            elif ((j < (y_axis_count - 1) and not is_there_overlap)):
                f1.write("0, ")
                f2.write("Range available : " + str(begin_block_nbr) + " - " + str(end_block_nbr) + ",")
                # f2.write(str(mySystem) + " : " + str(myNbrObject) + " : " + str(begin_block_nbr) + " - " + str(end_block_nbr) + ",")
                continue
            elif ((j >= (y_axis_count - 1) and is_there_overlap)):
                f1.write(("{}\n").format(myindex))
                f2.write(str(mySystem) + " : " + str(myNbrObject) + " : " + str(begin_block_nbr) + " - " + str(end_block_nbr) + "\n")
                continue
            elif ((j >= (y_axis_count - 1) and not is_there_overlap)):
                f1.write("0\n")
                f2.write("Range available : " + str(begin_block_nbr) + " - " + str(end_block_nbr) + "\n")
                # f2.write(str(mySystem) + " : " + str(myNbrObject) + " : " + str(begin_block_nbr) + " - " + str(end_block_nbr) + "\n")
                continue
            else:
                f1.write(("{}").format(myindex))
                f2.write(str(mySystem) + " : " + str(myNbrObject) + " : " + str(begin_block_nbr) + " - " + str(end_block_nbr))
                continue

print("Job Completed --- %s seconds ---" % (time.time() - start_time))

