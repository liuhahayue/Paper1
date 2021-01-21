import os
import numpy as np
import matplotlib.pyplot as plt

# ===================================================================
#                            边界条件对比
# ===================================================================
# Step
# 改变当前工作路径
path = r"C:\Users\B201-18\Desktop\fluent_ly\Paper1\Case7_application\Case7_application_result"
os.chdir(path)

filename = 'lastcycle_bcresult.csv'
Case1_bcdatas = []
with open(filename, "r") as f:
    for line in f.readlines():
        line = line.strip('\n').split(',')
        Case1_bcdatas.append(line)

# list 2 numpy
Case1_bcdatas = np.array(Case1_bcdatas).astype(np.float)
rows = Case1_bcdatas.shape[0]

# 处理非周期计算结果
non_period = []
f = open("Vary_T.txt", "r")
for line in f.readlines():
    line = line.strip('\n').split('\t')
    non_period.append(line)
f.close()
non_period = np.array(non_period).astype(np.float)

# ===================================================================
#                            绘图
# ===================================================================
plt.figure(figsize=(45, 15))

# BC
x1 = np.linspace(0, rows, rows)
# step inletq
ax1 = plt.subplot(3, 1, 1)
ax1.plot(x1, Case1_bcdatas[:, 0], color="r", ls="-", label="Step")
ax1.set_title("Inlet flow wavefoam", fontsize=12, color='k')
ax1.set_ylabel("ml/s")
# ax1.set_xlabel("timestep")
ax1.legend()
# step outlet1p
ax2 = plt.subplot(3, 1, 2)
ax2.plot(x1, Case1_bcdatas[:, 1], color="r", ls="-", label="Step")
ax2.set_title("Outlet1 pressure wavefoam", fontsize=12, color='k')
ax2.set_ylabel("mmHg/s")
# ax2.set_xlabel("timestep")
ax2.legend()
# Vary time
ax3 = plt.subplot(3, 1, 3)
x3 = np.linspace(0, non_period.shape[0], non_period.shape[0])
ax3.plot(x3, non_period[:, 1], marker='o', mec='r', mfc='w', label="Step")
ax3.set_title("Vary Time", fontsize=12, color='k')
ax3.set_xlabel("timestep")
ax3.set_ylabel("s")
ax3.legend()

plt.show()
