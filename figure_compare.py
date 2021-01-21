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
# non_period = []
# f = open("Vary_T.txt","r")
# for line in f.readlines():
#     line = line.strip('\n').split('\t')
#     non_period.append(line)
# f.close()
# non_period = np.array(non_period).astype(np.float)

# Cycle
# path = r"C:\Users\B201-18\Desktop\fluent_ly\Paper1\Case6_cycle_serial"
# os.chdir(path)

# filename = 'lastcycle_bcresult.csv'
# Case2_bcdatas = []
# with open(filename, "r") as f:
    # for line in f.readlines():
        # line = line.strip('\n').split(',')
        # Case2_bcdatas.append(line)

# list 2 numpy
# Case2_bcdatas = np.array(Case2_bcdatas).astype(np.float)
# cycle_inletq = Case2_bcdatas[:,0]*1000/1.06
# cycle_outlet1q = Case2_bcdatas[:,1]*-1*1000/1.06
# cycle_inletp = Case2_bcdatas[:,1]/133.28
# cycle_outlet2p = Case2_bcdatas[:,-1]/133.28
# Case2_bcdatas = np.column_stack((cycle_inletq,cycle_outlet1q,cycle_outlet2p))
# Case2_bcdatas = np.column_stack((cycle_inletq,cycle_inletp))

# ===================================================================
#                            收敛时间及残差对比
# ===================================================================
# Case1_error = [1,0.024574,0.010828,0.003213]
# Case2_error = [1,0.039642,0.036783,0.039167]
# Case_timex = ["Step","Cycle"]
# Case_timey = [395,892]

# ===================================================================
#                            绘图
# ===================================================================
plt.figure(figsize=(30, 15))

# BC
x1 = np.linspace(0, rows, rows)
ax1 = plt.subplot(3, 1, 1)
ax1.plot(x1, Case1_bcdatas[:, 0], color="r", ls="-", label="Step")        # step inletq
# ax1.plot(x1,Case2_bcdatas[:,0],color="b",ls = ":",label="Cycle")      #cycle inletq
ax1.set_title("Inlet compare", fontsize=12, color='k')
ax1.set_ylabel("ml/s")
ax1.set_xlabel("timestep")
ax1.legend()

ax2 = plt.subplot(3, 1, 2)
ax2.plot(x1, Case1_bcdatas[:, 1], color="r", ls="-", label="Step")        # step outlet1p
# ax2.plot(x1,Case2_bcdatas[:,1],color="b",ls = ":", label="Cycle")     #cycle outlet1p
ax2.set_title("Outlet1 compare", fontsize=12, color='k')
ax2.set_ylabel("mmHg/s")
ax2.set_xlabel("timestep")
ax2.legend()

# Error
# ax3 = plt.subplot(3, 1, 3)
# x3 = np.linspace(0,non_period.shape[0],non_period.shape[0])
# x3 = np.linspace(0,len(Case1_error),len(Case1_error))
# ax3.plot(x3,non_period[:,1],marker='o', mec='r', mfc='w',label="Step")
# ax3.plot(x3,Case1_error,marker='o', mec='r', mfc='w',label="Step")
# x3 = np.linspace(0,len(Case2_error),len(Case2_error))
# ax3.plot(x3,Case2_error,marker='*', ms=10,label="Cycle")
# ax3.set_title("Vary Time", fontsize=12, color='k')
# ax3.legend()

# Time
# ax4 = plt.subplot(2,2,4)
# ax4.bar(x = Case_timex, height=Case_timey)
# ax4.set_title("Time compare",fontsize=12,color='k')
# 保存图片
# plt.savefig('Case5_compare.jpg')
plt.show()
