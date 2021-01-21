import os
import numpy as np

# ===================================================================
#                            读取 FieldView 结果文件
# ===================================================================
# 改变路径
path = r"C:\Users\B201-18\Desktop\fluent_ly\Paper1\Case1_step\Result"
os.chdir(path)
fvname = "Case1_cycle_step"

# Step
filenames = "Case1_step_ASCII_fieldview_results.fv"
stepDatas = []
with open(filenames, "r") as f:
    for line in f.readlines()[19:]:
        line = line.strip('\n')
        stepDatas.append(line)

# list 2 numpy
stepDatas = np.array(stepDatas).astype(np.float)
# print(stepDatas.shape)

# 改变路径
path = r"C:\Users\B201-18\Desktop\fluent_ly\Paper1\Case2_cycle\Case1_cycle_result"
os.chdir(path)
# Cycle
filenames = "Case1_cycle_ASCII_fieldview_results.fv"
cycleDatas = []
with open(filenames, "r") as f:
    for line in f.readlines()[19:]:
        line = line.strip('\n')
        cycleDatas.append(line)

# list 2 numpy
cycleDatas = np.array(cycleDatas).astype(np.float)
# print(cycleDatas.shape)

# Calculate difference
Difference_step2cycle = cycleDatas - stepDatas
node_number = Difference_step2cycle.shape[0]/4

# ==================================================================
#                         生成 .fv 文件（ASCII）
# ==================================================================
output_filename = fvname + '_Difference_ASCII_fieldview_results.fv'
with open(output_filename, "w") as file:
    file.write('FIELDVIEW_Results 3 0\n')
    file.write('Constants\n0.002000\n0.000000\n0.000000\n0.000000\n')
    file.write('Grids\n1\n')
    file.write('Variable Names\n4\n')  # 4 variables
    file.write('TAWSS\n')
    file.write('MWSS\n')
    file.write('OSI\n')
    file.write('RRT\n')
    file.write('Boundary Variable Names\n0\n')
    file.write('Nodes\n')
    file.write(str(node_number)+'\n')
    file.write('Variables\n')

    for i in range(Difference_step2cycle.shape[0]):
        file.write(str(Difference_step2cycle[i])+'\n')
