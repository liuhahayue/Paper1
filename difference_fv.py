import os
import numpy as np

# ===================================================================
#                            读取 FieldView 结果文件
# ===================================================================
# 改变路径
path = r"C:\Users\B201-18\Desktop\Fluent2FV\python\Paper1_Result_FV\Case5"
os.chdir(path)
fvname = "Case5_cycle_step"
fv_stepname = "Case5_step"
fv_cyclename = "Case6_cycle"

# Step
filenames = fv_stepname+"_ASCII_fieldview_results.fv"
stepDatas = []
with open(filenames, "r") as f:
    for line in f.readlines()[19:]:
        line = line.strip('\n')
        stepDatas.append(line)

# list 2 numpy
stepDatas = np.array(stepDatas).astype(np.float)

# Cycle
filenames = fv_cyclename+"_ASCII_fieldview_results.fv"
cycleDatas = []
with open(filenames, "r") as f:
    for line in f.readlines()[19:]:
        line = line.strip('\n')
        cycleDatas.append(line)

# list 2 numpy
cycleDatas = np.array(cycleDatas).astype(np.float)

# Calculate difference
# Difference_step2cycle = cycleDatas - stepDatas        # 二者的差异单纯做减法
Difference_step2cycle = np.abs(cycleDatas - stepDatas)  # 二者的差异取绝对值
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
