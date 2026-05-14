import math
from numpy import arcsin
import numpy
import pandas
import matplotlib
import matplotlib.pyplot as plt
import math
L_Magnet = 0.05 #磁铁的物理长度，即沿着电子前进方向的磁铁长度，假设为0.15m
P_electron = 0.4 #电子能量400MeV
B_Magnet = 0.4    #磁铁磁场强度
R_deflection = 3.33*P_electron/B_Magnet  #能量为P的电子在磁场强度为B中偏转半径
print(f"\033[33m第一个磁铁中偏转半径为：{R_deflection} 米，注意需要确保R>L\033[0m")
theta_rad = arcsin(L_Magnet/R_deflection) #电子从进入磁铁到飞出磁铁的偏转角度，飞出后沿直线运动
theta_Deg = math.degrees(theta_rad) 
print(f"\033[33m第一个磁铁中偏转角度为：{theta_Deg} 度\033[0m")
#下面计算电子在磁铁内部的偏转距离
def calculate_deflection_distance(L, theta_deg):
    """
    计算电子在磁铁内部的横向偏转距离 n
    :param L: 磁铁物理长度 (单位自定义，例如米或厘米)
    :param theta_deg: 偏转角度 (单位：度)
    :return: 偏转距离 n (单位与 L 相同)
    """
    # 将角度转换为弧度
    theta_rad = math.radians(theta_deg)
    
    # 防止 theta = 0 导致除以零的报错
    if theta_rad == 0:
        return 0.0
        
    tan_theta = math.tan(theta_rad)
    
    # 构造一元二次方程 a*n^2 + b*n + c = 0 的系数
    a = 1.0
    b = (2 * L) / tan_theta
    c = - (L ** 2)
    
    # 计算判别式 (b^2 - 4ac)
    discriminant = b**2 - 4 * a * c
    
    # 求解两个根
    n1 = (-b + math.sqrt(discriminant)) / (2 * a)
    n2 = (-b - math.sqrt(discriminant)) / (2 * a)
    
    # 物理现实中，偏转距离 n 是一个正数，所以我们取大于 0 的那个根
    n_physical = max(n1, n2)
    
    return n_physical
# === 测试代码 ===
L_input = L_Magnet  # 假设磁铁长度 20cm (0.2m)
theta_input = theta_Deg  # 假设偏转角 8.6 度

n_result = calculate_deflection_distance(L_input, theta_input)
print(f"第一个磁铁长度 L = {L_input} m, 偏转角 theta = {theta_input}°")
print(f"\033[33m电子在第一个磁铁内部的偏转距离 n = {n_result:.6f} 米，注意需要确保电子束中心在垂直电子束传播方向上距离C形口至少为：{n_result:.6f}米\033[0m")

##============================下面加第二块磁铁在后面=======================================
n_between_magnets = 0.1 #两块磁铁之间的距离单位为米
L_Magnet2 = 0.08 #第二块磁铁的长度
B_Magnet2 = 0.9 #第二块磁铁的磁场强度
R_deflection2 = 3.33*P_electron/B_Magnet2  #能量为P的电子在第二块磁铁中的偏转半径
print(f"\033[33m第二块磁铁的偏转半径为：{R_deflection2} 米，注意需要确保R_deflection2>L_Magnet2\033[0m")
n2 = n_between_magnets* math.tan(theta_rad) #电子在两块磁铁之间的横向偏转距离
print(f"\033[33m电子在两块磁铁之间的横向偏转距离 n2 = {n2:.6f} 米\033[0m")
theta2_rad = arcsin(math.sin(theta_rad)+L_Magnet2/R_deflection2) #电子出第二块磁铁的偏转角度，用微积分算的，详见Gemini
theta2_Deg = math.degrees(theta2_rad)
beita_rad = theta2_rad-theta_rad #第二块磁铁中偏转的圆心角
beita_Deg = math.degrees(beita_rad)
print(f"\033[33m第二块磁铁中偏转的圆心角 beita = {beita_Deg:.6f} 度\033[0m")
print(f"\033[33m从第二块磁铁出射与水平夹角角度为：{theta2_Deg:.6f} 度\033[0m")

#从第二块磁铁入射点到出射点的偏转距离
#$Y = R (\cos\theta_1 - \cos\theta_2)$
y_Offset_Magnet2 = R_deflection2 * (math.cos(theta_rad) - math.cos(theta2_rad))
print(f"\033[33m从第二块磁铁入射点到出射点的偏转距离:{y_Offset_Magnet2:.6f} 米\033[0m")

Total_Offset = n_result + n2 + y_Offset_Magnet2
print(f"\033[33m电子从第一块磁铁入射点(即gamma束流中心)到第二块磁铁出射点（即电子离开最后一块磁铁）的总偏转距离为：{Total_Offset:.6f} 米\033[0m")

Horizontal_Distance_out_Magnet2 = L_Magnet+n_between_magnets+L_Magnet2
print(f"\033[33m电子刚出第二块磁铁时在gamma传播方向上的位移为{Horizontal_Distance_out_Magnet2:.6f}米\033[0m")

#下面求解暗箱应该放在磁铁后面多远
W_total = 0.05  #这是暗箱中LYSO中心距离暗箱边缘的距离,包含磁铁内部偏转距离
W_out = W_total-Total_Offset  #减去总偏转的距离
D_out = W_out/math.tan(theta2_rad)
print(f"\033[35m第二块磁铁外边缘距离暗箱距离应该为：{D_out:.6f}米\033[0m")