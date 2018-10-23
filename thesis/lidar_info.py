import pandas as pd
import matplotlib.pyplot as plt
import glob
import os



filepath = r'C:\Users\oyeda\Desktop\msc\thesis\lidar_text_info\*.txt'

dirname=os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(dirname, 'lidar_text_info/*.txt')
list_of_files = glob.glob(filename) 
print(list_of_files)




# for file_name in list_of_files:
#   FI = open(file_name, 'r')
#   FO = open(file_name.replace('txt', 'out'), 'w') 
#   for line in FI:
#     FO.write(line)

#   FI.close()
#   FO.close()
 