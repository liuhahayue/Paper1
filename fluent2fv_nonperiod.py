import os
import pandas as pd
import numpy as np

# ===================================================================
#                     删除文件夹中不需要的结果文件
# ===================================================================
# 改变当前工作路径
path = r"C:\Users\B201-18\Desktop\fluent_ly\Paper1\Case7_application\Case7_application_result"
os.chdir(path)
result_0d = 'CalData.txt'       # 3d 边界条件结果
resultStr = 'Case5_step-'       # 不同的case需要修改结果文件的前缀 此处应该将所有的统一！！！
fvname = 'Case7_step_cycle'     # fieldview 格式输出文件名
geom_filename = 'geom.csv'      # 几何文件
mesh_style = 1                  # 网格类型 struct : mesh_style = 1 || unstruct mesh_style = 0
step = 1                        # 判断程序处理 step = 1 || cycle = 0
# 获取第一个循环周期的序号 与 计算结果
dt = 0.0004
T = 0.8
rm_total_step = (int)(T/dt)

# 获取结果文件的序号
resultData = []
with open(result_0d, "r") as f:
    if(step == 1):
        # Step 读取计算结果
        for line in f.readlines():
            # 将每一行的换行符 剪切掉 数据以 \t 分开
            line = line.strip('\n').split('\t')
            resultData.append(line)
    else:
        # Cycle 读取计算结果
        for line in f.readlines()[3:]:
            line = line.strip('\n').split(' ')
            resultData.append(line)

# list 2 numpy
resultData = np.array(resultData)
lastcycle_bcresult = resultData[(rm_total_step-1):-1, 1:].astype(np.float)
lastcycle_filenumber = resultData[(rm_total_step-1):-1, 0]

# 3D 边界条件 与 计算结果输出
np.savetxt('lastcycle_bcresult.csv', lastcycle_bcresult, delimiter=',')

# 获取最后一个循环周期的结果文件名称
lastCycle_filenames = []
for caseNumber in lastcycle_filenumber:
    if(len(caseNumber) < 4):
        caseNumber = str(0)+caseNumber

    lastCycle_filenames.append(resultStr+caseNumber)                        # str

# 更新 total step
total_step = len(lastCycle_filenames)

# 将不符合要求的文件删除
files = os.listdir(path)
for f in files:
    if (resultStr in f) and (f not in lastCycle_filenames):
        os.remove(f)

# ===================================================================
#                         读取结果文件
# ===================================================================
# 提取壁面剪切应力信息
wallShear_df = pd.DataFrame()
wallShearX_df = pd.DataFrame()
wallShearY_df = pd.DataFrame()
wallShearZ_df = pd.DataFrame()
coordinateXYZ_df = pd.DataFrame()
maxWallShear_info = pd.DataFrame()
maxWallShear = []

for i in range(total_step):
    print("The"+str(i)+"th file\n")
    # 文件为空格符为分割时
    df = pd.read_csv(lastCycle_filenames[i], delim_whitespace=True, dtype=str)
    # 提取计算结果面网格节点坐标
    if i == 0:
        coordinateXYZ_df = df.iloc[:, 1:4]

    # 利用apply将数据类型转换作用到整个dataframe中
    df = df.apply(pd.to_numeric, errors='ignore')
    # 将壁面剪应力的信息写入 wallShear_df
    wallShear_df[i] = df[df.columns[4]]
    wallShearX_df[i] = df[df.columns[5]]
    wallShearY_df[i] = df[df.columns[6]]
    wallShearZ_df[i] = df[df.columns[7]]

    # 寻找到最大壁面剪应力的行索引
    # maxWallShear_index = df['wall-shear'].idxmax()
    maxWallShear_index = df[df.columns[4]].idxmax()
    # 将最大剪应力的行信息写入 maxWallShear_info
    maxWallShear_info = maxWallShear_info.append(df[maxWallShear_index:maxWallShear_index+1])
    # 保存每一列最大的壁面剪应力
    maxWallShear.append(df.loc[maxWallShear_index, 'wall-shear'])  # loc 时 需要用行与列索引的名字

# 保存最大壁面剪应力文件
np.savetxt('maxWallShear.csv', np.array(maxWallShear), delimiter=',')

# ===================================================================
#                         计算壁面相关参数
# ===================================================================
# 将 dataframe 转换为 numpy
xyz_arr = coordinateXYZ_df.values.astype(np.float)
wss_arr = wallShear_df.values
wssx_arr = wallShearX_df.values
wssy_arr = wallShearY_df.values
wssz_arr = wallShearZ_df.values

# 计算 TAWSS
wss_Trnavg = wss_arr.mean(axis=1)                       # 以列取平均值

# 计算 MWSS
wssx_Trnavg = wssx_arr.mean(axis=1)
wssy_Trnavg = wssy_arr.mean(axis=1)
wssz_Trnavg = wssz_arr.mean(axis=1)
MWSS = np.sqrt(np.square(wssx_Trnavg)+np.square(wssy_Trnavg)+np.square(wssz_Trnavg))

# 计算 OSI
OSI = 0.5*(1-MWSS/wss_Trnavg)

# 计算 RRT
RRT = 1/((1.000001 - 2*OSI)*wss_Trnavg)

# 将计算结果数组合并
temp2 = np.column_stack((xyz_arr, wss_Trnavg, MWSS, OSI, RRT))
# numpy 矩阵分别以 x,y,z 三个方向由小到大排序
sort_temp2 = temp2[np.lexsort(temp2[:, ::-1].T)]

# ===================================================================
#                         读取几何文件
# ===================================================================
# 提取面网格节点坐标信息
f = open(geom_filename, "r")
geom = []
for line in f.readlines()[6:]:
    line = line.strip('\n').split(',')
    if(line[0] == ''):
        break
    geom.append(line)
f.close()

# 3d 面网格节点坐标
iloc_geom = np.array(geom)[:, 1:]

# list 2 numpy
geom = np.array(geom).astype(np.float)
coordinate_geom = geom[:, 1:]
node_geom = geom[:, 0]
node_number = node_geom.shape[0]

# 提取面网格连接信息
f = open(geom_filename, "r")
face_xyz = []
for line in f.readlines()[(6+node_number+2):]:
    line = line.strip('\n').split(',')
    if(line[0] == ''):
        break
    face_xyz.append(line)
f.close()

# list 2 numpy
face_xyz = np.array(face_xyz).astype(np.int) + 1    # face connection
face_number = face_xyz.shape[0]

# 合并两个不同维度的矩阵
temp = np.column_stack((coordinate_geom, node_geom))
# numpy 矩阵分别以 x,y,z 三个方向由小到大排序
sort_temp = temp[np.lexsort(temp[:, ::-1].T)]
# sort flag 结果文件按照此标记进行排序
sort_flag = sort_temp[:, -1]                         # 几何坐标系 与 计算结果坐标系 匹配

# ==================================================================
#                         生成 .fv 文件（ASCII）
# ==================================================================
# 利用 sort flag 重新对计算结果重新排序
sort_temp2 = np.column_stack((sort_flag, sort_temp2))
sorted_datas = sort_temp2[np.lexsort(sort_temp2[:, ::-1].T)]
# 3D 壁面计算结果输出
np.savetxt('lastcycle_wallresult_cycle.csv', sorted_datas, delimiter=',')

# write the "xxx_ASCII_fieldview_results.fv" file
output_filename = fvname + '_ASCII_fieldview_results.fv'
lastcycle_result = sorted_datas[:, 4:]
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

    for j in range(lastcycle_result.shape[1]):
        for i in range(lastcycle_result.shape[0]):
            file.write(str(lastcycle_result[i, j])+'\n')

# write the "xxx_ASCII_fieldview_grids.fv" file
output_filename2 = fvname + '_ASCII_fieldview_grids.fv'
with open(output_filename2, "w") as file1:
    file1.write('FIELDVIEW_Grids 3 0\n')
    file1.write('Grids\n1\n')
    file1.write('Boundary Table\n1\n')
    file1.write('1 0 1 Wall\n')
    file1.write('Nodes\n')
    file1.write(str(node_number)+'\n')

    for i in range(node_number):
        file1.write(iloc_geom[i, 0]+' '+iloc_geom[i, 1]+' '+iloc_geom[i, 2]+'\n')

    file1.write('Boundary Faces\n')
    file1.write(str(face_number)+'\n')
    for i in range(face_number):
        if mesh_style == 1:
            file1.write('1 4 '+str(face_xyz[i, 0])+' '+str(face_xyz[i, 1])+' '+str(face_xyz[i, 2])+' '+str(face_xyz[i, 3])+'\n')
        else:
            file1.write('1 3 '+str(face_xyz[i, 0])+' '+str(face_xyz[i, 1])+' '+str(face_xyz[i, 2])+'\n')

    file1.write('Elements\n')                       # there has to be an element
    file1.write('1 1 2 10 11 4\n')                  # randomly give one
