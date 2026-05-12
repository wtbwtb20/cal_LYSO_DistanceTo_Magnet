import streamlit as st
import math
import numpy as np

def calculate_lyso_kinematics(p_electron, l_magnet, b_magnet, w_total):
    """
    核心物理计算层：将原来的零散脚本封装为纯函数，与 UI 完全解耦
    """
    # 1. 偏转半径 R
    r_deflection = 3.33 * p_electron / b_magnet
    
    # 🚨 防御性校验：防止定义域错误
    # 如果物理长度 L 大于 偏转半径 R，arcsin 会无解。
    if l_magnet > r_deflection:
        raise ValueError("磁铁物理长度大于偏转半径，电子将无法穿出磁场！")
        
    # 2. 偏转角度 theta
    theta_rad = np.arcsin(l_magnet / r_deflection)
    theta_deg = math.degrees(theta_rad)
    
    # 3. 磁铁内部偏转距离 n
    if theta_rad == 0:
        n_physical = 0.0
    else:
        tan_theta = math.tan(theta_rad)
        a = 1.0
        b = (2 * l_magnet) / tan_theta
        c = -(l_magnet ** 2)
        discriminant = b**2 - 4 * a * c
        
        n1 = (-b + math.sqrt(discriminant)) / (2 * a)
        n2 = (-b - math.sqrt(discriminant)) / (2 * a)
        n_physical = max(n1, n2)
        
    # 4. 暗箱距离 D
    w_out = w_total - n_physical
    d_out = w_out / math.tan(theta_rad)
    
    return r_deflection, theta_deg, n_physical, d_out

# ================= UI 表现层 =================

# 1. 页面基础配置 (设置网页标题、图标和布局格式)
st.set_page_config(page_title="LYSO 距离计算器", page_icon="🧲", layout="centered")

# 2. 主标题与说明
st.title("🧲 LYSO 暗箱距离自动计算工具")
st.markdown("基于电子动量、磁场强度与物理尺寸，实时推算探测器最佳放置位置。")
st.divider() # 绘制一条分割线

# 3. 布局：使用左右两列，左侧放输入表单，右侧放计算结果
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("📥 物理参数输入")
    # 创建交互式数字输入框，修改数值会自动触发整个页面的重新计算
    p_in = st.number_input("电子能量 P (默认 0.4)", value=0.40, step=0.01, format="%.3f")
    l_in = st.number_input("磁铁物理长度 L (米)", value=0.20, step=0.01, format="%.3f")
    b_in = st.number_input("磁场强度 B (特斯拉)", value=1.00, step=0.10, format="%.2f")
    w_in = st.number_input("LYSO中心距边缘 W (米)", value=0.20, step=0.01, format="%.3f")

with col_output:
    st.subheader("📤 实时计算结果")
    try:
        # 防御性校验：除数不能为0
        if b_in == 0:
            st.warning("⚠️ 磁场强度不能为 0")
        else:
            # 调用核心计算逻辑
            r_res, theta_res, n_res, d_res = calculate_lyso_kinematics(p_in, l_in, b_in, w_in)
            
            # 使用 Streamlit 的 metric 组件，展示效果类似数据看板的大卡片
            st.metric(label="偏转半径 (R)", value=f"{r_res:.4f} m")
            st.metric(label="偏转角度 (θ)", value=f"{theta_res:.4f} °")
            st.metric(label="磁铁内偏转距离 (n)", value=f"{n_res:.6f} m")
            
            # 使用醒目的颜色高亮最终我们需要的结果
            st.success(f"**✅ 暗箱应放置距离 (D)：{d_res:.4f} m**")
            
    except ValueError as ve:
        # 捕获我们在函数中抛出的物理不合理异常
        st.error(f"⚠️ 物理边界错误：{ve}")
    except Exception as e:
        # 兜底捕获其他未知数学异常
        st.error(f"❌ 计算异常：{e}")
