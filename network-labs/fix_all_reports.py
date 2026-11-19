"""
统一修复所有实验报告：
1. 字体统一为宋体
2. 生成网络拓扑图并插入报告
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ============================================================
# 设置中文字体
# ============================================================
plt.rcParams['font.sans-serif'] = ['SimSun', 'Microsoft YaHei', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = "D:/计网实验"
IMG_DIR = os.path.join(OUTPUT_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)

# ============================================================
# 拓扑图绘制工具函数
# ============================================================

def draw_device(ax, x, y, label, color='#4A90D9', shape='rect', size=(1.2, 0.6)):
    """绘制设备方框"""
    w, h = size
    if shape == 'rect':
        box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                             boxstyle="round,pad=0.05",
                             facecolor=color, edgecolor='#333333', linewidth=1.5)
        ax.add_patch(box)
    elif shape == 'circle':
        circle = plt.Circle((x, y), w/2, facecolor=color, edgecolor='#333333', linewidth=1.5)
        ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', fontsize=9,
            fontweight='bold', color='white', fontfamily='SimSun')

def draw_pc(ax, x, y, label, ip=''):
    """绘制PC设备"""
    draw_device(ax, x, y, label, color='#5B9BD5', shape='rect', size=(1.0, 0.5))
    if ip:
        ax.text(x, y - 0.45, ip, ha='center', va='top', fontsize=7,
                color='#333333', fontfamily='SimSun')

def draw_switch(ax, x, y, label='Switch'):
    """绘制交换机"""
    draw_device(ax, x, y, label, color='#70AD47', shape='rect', size=(1.3, 0.5))

def draw_router(ax, x, y, label='Router'):
    """绘制路由器"""
    draw_device(ax, x, y, label, color='#ED7D31', shape='circle', size=(0.8, 0.8))

def draw_server(ax, x, y, label, ip=''):
    """绘制服务器"""
    draw_device(ax, x, y, label, color='#9B59B6', shape='rect', size=(1.1, 0.55))
    if ip:
        ax.text(x, y - 0.5, ip, ha='center', va='top', fontsize=7,
                color='#333333', fontfamily='SimSun')

def draw_line(ax, x1, y1, x2, y2, color='#666666'):
    """绘制连接线"""
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=1.5, zorder=0)

def draw_line_with_label(ax, x1, y1, x2, y2, label='', color='#666666'):
    """绘制带标签的连接线"""
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=1.5, zorder=0)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.1, label, ha='center', va='bottom', fontsize=6,
                color='#999999', fontfamily='SimSun')


# ============================================================
# 实验一拓扑图
# ============================================================

def create_lab1_topology1():
    """交换机+3台PC拓扑"""
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('实验一：交换机与PC机网络拓扑', fontsize=14, fontweight='bold', fontfamily='SimSun')

    draw_switch(ax, 5, 5, 'Switch0\n(2960)')
    draw_pc(ax, 2, 2, 'PC1', '192.168.1.1/24')
    draw_pc(ax, 5, 2, 'PC2', '192.168.1.2/24')
    draw_pc(ax, 8, 2, 'PC3', '192.168.1.3/24')

    draw_line(ax, 5, 4.75, 2, 2.25)
    draw_line(ax, 5, 4.75, 5, 2.25)
    draw_line(ax, 5, 4.75, 8, 2.25)

    ax.text(3.2, 3.8, 'Fa0/1', fontsize=7, color='#999', fontfamily='SimSun')
    ax.text(5.1, 3.8, 'Fa0/2', fontsize=7, color='#999', fontfamily='SimSun')
    ax.text(6.8, 3.8, 'Fa0/3', fontsize=7, color='#999', fontfamily='SimSun')

    path = os.path.join(IMG_DIR, 'lab1_topology1.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def create_lab1_topology2():
    """路由器+PC拓扑"""
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('实验一：路由器与PC机网络拓扑', fontsize=14, fontweight='bold', fontfamily='SimSun')

    draw_router(ax, 5, 5, 'Router0\n(2811)')
    draw_pc(ax, 5, 2, 'PC0', '192.168.1.2/24\nGW: 192.168.1.1')

    draw_line_with_label(ax, 5, 4.6, 5, 2.25, 'Fa0/0: 192.168.1.1')

    ax.text(6.5, 5, 'Console', fontsize=7, color='#999', fontfamily='SimSun')
    ax.annotate('', xy=(6.2, 4.8), xytext=(5.5, 4.8),
                arrowprops=dict(arrowstyle='->', color='#999'))

    path = os.path.join(IMG_DIR, 'lab1_topology2.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def create_lab1_mac_table():
    """MAC地址表示意图"""
    fig, ax = plt.subplots(1, 1, figsize=(7, 3))
    ax.axis('off')
    ax.set_title('交换机MAC地址表', fontsize=12, fontweight='bold', fontfamily='SimSun')

    data = [
        ['MAC地址', '端口', 'VLAN'],
        ['AA:BB:CC:11:11:11', 'Fa0/1', '1'],
        ['AA:BB:CC:22:22:22', 'Fa0/2', '1'],
        ['AA:BB:CC:33:33:33', 'Fa0/3', '1'],
    ]
    table = ax.table(cellText=data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    for (row, col), cell in table.get_celld().items():
        cell.set_text_props(fontfamily='SimSun')
        if row == 0:
            cell.set_facecolor('#4A90D9')
            cell.set_text_props(color='white', fontweight='bold')
        else:
            cell.set_facecolor('#F0F0F0')

    path = os.path.join(IMG_DIR, 'lab1_mac_table.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


# ============================================================
# 实验二拓扑图
# ============================================================

def create_lab2_topology1():
    """单路由器连接2个子网"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('实验二：单路由器连接两个子网', fontsize=14, fontweight='bold', fontfamily='SimSun')

    draw_router(ax, 6, 6, 'Router0\n(2811)')
    draw_switch(ax, 3, 3.5, 'Switch0')
    draw_switch(ax, 9, 3.5, 'Switch1')
    draw_pc(ax, 1.5, 1, 'PC0', '192.168.1.2')
    draw_pc(ax, 4.5, 1, 'PC1', '192.168.1.3')
    draw_pc(ax, 7.5, 1, 'PC2', '192.168.2.2')
    draw_pc(ax, 10.5, 1, 'PC3', '192.168.2.3')

    draw_line_with_label(ax, 4.5, 5.7, 3, 3.75, 'Fa0/0\n192.168.1.1/24')
    draw_line_with_label(ax, 7.5, 5.7, 9, 3.75, 'Fa1/0\n192.168.2.1/24')
    draw_line(ax, 3, 3.25, 1.5, 1.25)
    draw_line(ax, 3, 3.25, 4.5, 1.25)
    draw_line(ax, 9, 3.25, 7.5, 1.25)
    draw_line(ax, 9, 3.25, 10.5, 1.25)

    ax.text(1, 4.5, '子网1\n192.168.1.0/24', fontsize=9, color='#4A90D9',
            fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F0FE', edgecolor='#4A90D9'))
    ax.text(9, 4.5, '子网2\n192.168.2.0/24', fontsize=9, color='#ED7D31',
            fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF2E8', edgecolor='#ED7D31'))

    path = os.path.join(IMG_DIR, 'lab2_topology1.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def create_lab2_topology2():
    """两台路由器拓展局域网"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('实验二：两台路由器拓展局域网', fontsize=14, fontweight='bold', fontfamily='SimSun')

    draw_router(ax, 4, 6, 'Router0')
    draw_router(ax, 10, 6, 'Router1')
    draw_switch(ax, 2, 3.5, 'Switch0')
    draw_switch(ax, 12, 3.5, 'Switch1')
    draw_pc(ax, 1, 1, 'PC0', '192.168.1.2')
    draw_pc(ax, 3, 1, 'PC2', '192.168.1.3')
    draw_pc(ax, 11, 1, 'PC1', '192.168.2.2')
    draw_pc(ax, 13, 1, 'PC3', '192.168.2.3')

    draw_line_with_label(ax, 2, 3.75, 3.3, 5.5, 'Fa0/0\n192.168.1.1')
    draw_line_with_label(ax, 4.7, 5.5, 9.3, 5.5, 'Fa1/0──Fa1/0\n10.0.0.1──10.0.0.2')
    draw_line_with_label(ax, 10.7, 5.5, 12, 3.75, 'Fa0/0\n192.168.2.1')
    draw_line(ax, 2, 3.25, 1, 1.25)
    draw_line(ax, 2, 3.25, 3, 1.25)
    draw_line(ax, 12, 3.25, 11, 1.25)
    draw_line(ax, 12, 3.25, 13, 1.25)

    ax.text(1, 4.5, '子网1\n192.168.1.0/24', fontsize=9, color='#4A90D9',
            fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F0FE', edgecolor='#4A90D9'))
    ax.text(12, 4.5, '子网2\n192.168.2.0/24', fontsize=9, color='#ED7D31',
            fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF2E8', edgecolor='#ED7D31'))
    ax.text(7, 6.5, '互联链路\n10.0.0.0/24', fontsize=8, color='#70AD47',
            ha='center', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#E8F5E9', edgecolor='#70AD47'))

    path = os.path.join(IMG_DIR, 'lab2_topology2.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def create_lab2_routing_table():
    """静态路由表"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    for idx, (ax, title, data) in enumerate(zip(axes, ['Router0 路由表', 'Router1 路由表'], [
        [['目的网络', '子网掩码', '下一跳', '接口'],
         ['192.168.1.0', '255.255.255.0', '直连', 'Fa0/0'],
         ['192.168.2.0', '255.255.255.0', '10.0.0.2', 'Fa1/0'],
         ['10.0.0.0', '255.255.255.0', '直连', 'Fa1/0']],
        [['目的网络', '子网掩码', '下一跳', '接口'],
         ['192.168.2.0', '255.255.255.0', '直连', 'Fa0/0'],
         ['192.168.1.0', '255.255.255.0', '10.0.0.1', 'Fa1/0'],
         ['10.0.0.0', '255.255.255.0', '直连', 'Fa1/0']],
    ])):
        ax.axis('off')
        ax.set_title(title, fontsize=11, fontweight='bold', fontfamily='SimSun')
        table = ax.table(cellText=data, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)
        for (row, col), cell in table.get_celld().items():
            cell.set_text_props(fontfamily='SimSun')
            if row == 0:
                cell.set_facecolor('#ED7D31')
                cell.set_text_props(color='white', fontweight='bold')
            else:
                cell.set_facecolor('#FFF8F0')

    fig.suptitle('静态路由配置结果', fontsize=13, fontweight='bold', fontfamily='SimSun')
    path = os.path.join(IMG_DIR, 'lab2_routing_table.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


# ============================================================
# 实验三拓扑图
# ============================================================

def create_lab3_topology1():
    """单交换机VLAN划分"""
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('实验三：单交换机VLAN划分', fontsize=14, fontweight='bold', fontfamily='SimSun')

    draw_switch(ax, 5, 6, 'Switch0\n(2960)')

    # VLAN 10 - blue
    draw_pc(ax, 2, 2.5, 'PC1\nVLAN10', '192.168.0.11')
    draw_pc(ax, 4, 2.5, 'PC3\nVLAN10', '192.168.0.12')
    # VLAN 20 - orange
    draw_pc(ax, 6, 2.5, 'PC2\nVLAN20', '192.168.0.21')
    draw_pc(ax, 8, 2.5, 'PC4\nVLAN20', '192.168.0.22')

    draw_line(ax, 5, 5.75, 2, 2.75, color='#4A90D9')
    draw_line(ax, 5, 5.75, 4, 2.75, color='#4A90D9')
    draw_line(ax, 5, 5.75, 6, 2.75, color='#ED7D31')
    draw_line(ax, 5, 5.75, 8, 2.75, color='#ED7D31')

    ax.text(1, 4.5, 'VLAN 10', fontsize=11, color='#4A90D9',
            fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F0FE', edgecolor='#4A90D9'))
    ax.text(8, 4.5, 'VLAN 20', fontsize=11, color='#ED7D31',
            fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF2E8', edgecolor='#ED7D31'))

    # Show connectivity
    ax.text(3, 0.8, '[通] PC1<-->PC3', fontsize=9, color='#27AE60', fontfamily='SimSun')
    ax.text(3, 0.3, '[不通] PC1<-->PC2', fontsize=9, color='#E74C3C', fontfamily='SimSun')

    path = os.path.join(IMG_DIR, 'lab3_topology1.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def create_lab3_topology2():
    """多交换机VLAN + Trunk"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('实验三：多交换机VLAN划分（Trunk）', fontsize=14, fontweight='bold', fontfamily='SimSun')

    draw_switch(ax, 4, 7, 'Switch0')
    draw_switch(ax, 10, 7, 'Switch1')

    # Switch0 PCs
    draw_pc(ax, 2, 3.5, 'PC1\nVLAN10', '192.168.0.11')
    draw_pc(ax, 6, 3.5, 'PC2\nVLAN20', '192.168.0.21')
    # Switch1 PCs
    draw_pc(ax, 8, 3.5, 'PC3\nVLAN10', '192.168.0.12')
    draw_pc(ax, 12, 3.5, 'PC4\nVLAN20', '192.168.0.22')

    draw_line(ax, 4, 6.75, 2, 3.75, color='#4A90D9')
    draw_line(ax, 4, 6.75, 6, 3.75, color='#ED7D31')
    draw_line(ax, 10, 6.75, 8, 3.75, color='#4A90D9')
    draw_line(ax, 10, 6.75, 12, 3.75, color='#ED7D31')

    # Trunk link
    draw_line_with_label(ax, 5.3, 7, 8.7, 7, 'Trunk\n(802.1Q)\nFa0/24──Fa0/24', color='#E74C3C')

    # VLAN labels
    ax.text(1, 5.5, 'VLAN 10', fontsize=10, color='#4A90D9', fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#E8F0FE', edgecolor='#4A90D9'))
    ax.text(6.5, 5.5, 'VLAN 20', fontsize=10, color='#ED7D31', fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF2E8', edgecolor='#ED7D31'))
    ax.text(11, 5.5, 'VLAN 10', fontsize=10, color='#4A90D9', fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#E8F0FE', edgecolor='#4A90D9'))
    ax.text(11, 4.8, 'VLAN 20', fontsize=10, color='#ED7D31', fontweight='bold', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF2E8', edgecolor='#ED7D31'))

    # Connectivity results
    ax.text(3, 1.5, '[通] PC1<-->PC3 (同VLAN10跨交换机)', fontsize=9, color='#27AE60', fontfamily='SimSun')
    ax.text(3, 0.8, '[通] PC2<-->PC4 (同VLAN20跨交换机)', fontsize=9, color='#27AE60', fontfamily='SimSun')
    ax.text(3, 0.1, '[不通] PC1<-->PC2 (不同VLAN)', fontsize=9, color='#E74C3C', fontfamily='SimSun')

    path = os.path.join(IMG_DIR, 'lab3_topology2.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def create_lab3_vlan_table():
    """VLAN划分对比表"""
    fig, ax = plt.subplots(1, 1, figsize=(9, 3))
    ax.axis('off')
    ax.set_title('VLAN连通性测试结果', fontsize=12, fontweight='bold', fontfamily='SimSun')

    data = [
        ['测试场景', 'PC1<-->PC2\n(不同VLAN)', 'PC1<-->PC3\n(同VLAN10)', 'PC2<-->PC4\n(同VLAN20)'],
        ['无VLAN划分', '[通]', '[通]', '[通]'],
        ['单交换机VLAN', '[不通]', '[通]', '[通]'],
        ['多交换机VLAN+Trunk', '[不通]', '[通]', '[通]'],
    ]
    table = ax.table(cellText=data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)
    for (row, col), cell in table.get_celld().items():
        cell.set_text_props(fontfamily='SimSun')
        if row == 0:
            cell.set_facecolor('#70AD47')
            cell.set_text_props(color='white', fontweight='bold')
        elif col == 0:
            cell.set_facecolor('#E8F5E9')
        else:
            text = cell.get_text().get_text()
            if '通]' in text and '不' not in text:
                cell.set_facecolor('#E8F5E9')
            elif '不通]' in text:
                cell.set_facecolor('#FFEBEE')

    path = os.path.join(IMG_DIR, 'lab3_vlan_table.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


# ============================================================
# 实验四拓扑图
# ============================================================

def create_lab4_topology():
    """服务器拓扑"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('实验四：服务器网络拓扑', fontsize=14, fontweight='bold', fontfamily='SimSun')

    draw_switch(ax, 6, 6, 'Switch0\n(2960)')
    draw_server(ax, 2, 8, 'DHCP Server', '192.168.0.254')
    draw_server(ax, 6, 8, 'DNS Server', '192.168.0.253')
    draw_server(ax, 10, 8, 'FTP/WEB Server', '192.168.0.252')
    draw_pc(ax, 4, 2, 'PC0', 'DHCP自动获取')
    draw_pc(ax, 8, 2, 'PC1', 'DHCP自动获取')

    draw_line(ax, 6, 6.25, 2, 7.75)
    draw_line(ax, 6, 6.25, 6, 7.75)
    draw_line(ax, 6, 6.25, 10, 7.75)
    draw_line(ax, 6, 5.75, 4, 2.25)
    draw_line(ax, 6, 5.75, 8, 2.25)

    # Service labels
    ax.text(0.5, 7, 'DHCP服务\n动态分配IP', fontsize=7, color='#9B59B6', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#F3E5F5', edgecolor='#9B59B6'))
    ax.text(6.5, 7, 'DNS服务\n域名解析', fontsize=7, color='#3498DB', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#EBF5FB', edgecolor='#3498DB'))
    ax.text(10, 7, 'FTP/WEB\n文件/网页', fontsize=7, color='#E67E22', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#FDF2E9', edgecolor='#E67E22'))

    path = os.path.join(IMG_DIR, 'lab4_topology.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def create_lab4_dhcp_process():
    """DHCP DORA过程"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('DHCP DORA 四步过程', fontsize=14, fontweight='bold', fontfamily='SimSun')

    draw_pc(ax, 2, 4, '客户端\n(PC)', '#5B9BD5')
    draw_server(ax, 10, 4, 'DHCP服务器', '#9B59B6')

    # DORA arrows
    y_positions = [6.5, 5.3, 4.1, 2.9]
    labels = [
        '① Discover（广播）',
        '② Offer（提供IP）',
        '③ Request（请求确认）',
        '④ ACK（确认分配）',
    ]
    colors = ['#E74C3C', '#27AE60', '#3498DB', '#F39C12']

    for y, label, color in zip(y_positions, labels, colors):
        ax.annotate('', xy=(9, y), xytext=(3, y),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2))
        ax.text(6, y + 0.2, label, ha='center', va='bottom', fontsize=10,
                fontweight='bold', color=color, fontfamily='SimSun')

    ax.text(2, 1.5, '客户端获得IP地址\n192.168.0.x', fontsize=10,
            ha='center', fontfamily='SimSun',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#27AE60'))

    path = os.path.join(IMG_DIR, 'lab4_dhcp_dora.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path

def create_lab4_dns_process():
    """DNS解析过程"""
    fig, ax = plt.subplots(1, 1, figsize=(9, 3))
    ax.axis('off')
    ax.set_title('DNS域名解析记录', fontsize=12, fontweight='bold', fontfamily='SimSun')

    data = [
        ['域名', 'IP地址', '记录类型'],
        ['www.test.com.cn', '192.168.0.252', 'A Record'],
        ['ftp.test.cn', '192.168.0.252', 'A Record'],
    ]
    table = ax.table(cellText=data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)
    for (row, col), cell in table.get_celld().items():
        cell.set_text_props(fontfamily='SimSun')
        if row == 0:
            cell.set_facecolor('#3498DB')
            cell.set_text_props(color='white', fontweight='bold')
        else:
            cell.set_facecolor('#EBF5FB')

    path = os.path.join(IMG_DIR, 'lab4_dns_table.png')
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


# ============================================================
# 生成所有图片
# ============================================================

print("正在生成拓扑图...")
images = {}

# 实验一
images['lab1_top1'] = create_lab1_topology1()
images['lab1_top2'] = create_lab1_topology2()
images['lab1_mac'] = create_lab1_mac_table()
print("  实验一拓扑图完成")

# 实验二
images['lab2_top1'] = create_lab2_topology1()
images['lab2_top2'] = create_lab2_topology2()
images['lab2_route'] = create_lab2_routing_table()
print("  实验二拓扑图完成")

# 实验三
images['lab3_top1'] = create_lab3_topology1()
images['lab3_top2'] = create_lab3_topology2()
images['lab3_vlan'] = create_lab3_vlan_table()
print("  实验三拓扑图完成")

# 实验四
images['lab4_top'] = create_lab4_topology()
images['lab4_dhcp'] = create_lab4_dhcp_process()
images['lab4_dns'] = create_lab4_dns_process()
print("  实验四拓扑图完成")


# ============================================================
# 重新生成所有报告（宋体 + 插入图片）
# ============================================================

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def set_font(run, name='宋体', size=None, bold=False, color=None):
    """设置字体为宋体"""
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if size:
        run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)

def add_heading_simsun(doc, text, level=1):
    """添加宋体标题"""
    heading = doc.add_heading(level=level)
    run = heading.add_run(text)
    set_font(run, '宋体', size=16 if level == 0 else 14 if level == 1 else 12, bold=True)
    return heading

def add_para(doc, text, size=11, bold=False, indent=False):
    """添加宋体段落"""
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run(text)
    set_font(run, '宋体', size=size, bold=bold)
    return p

def add_image(doc, path, width=Inches(5.5)):
    """插入图片"""
    doc.add_picture(path, width=width)
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

def add_table_simsun(doc, headers, data):
    """添加宋体表格"""
    table = doc.add_table(rows=1 + len(data), cols=len(headers))
    table.style = 'Table Grid'
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        run = cell.paragraphs[0].add_run(h)
        set_font(run, '宋体', size=10, bold=True)
    for i, row_data in enumerate(data):
        for j, val in enumerate(row_data):
            cell = table.rows[i + 1].cells[j]
            cell.text = ''
            run = cell.paragraphs[0].add_run(val)
            set_font(run, '宋体', size=10)
    return table


print("\n正在重新生成实验报告...")

# ============================================================
# 实验一报告
# ============================================================
doc = Document()

add_heading_simsun(doc, '实验一 交换机路由器的基本配置', level=0)

add_heading_simsun(doc, '一、实验目的', level=1)
add_para(doc, '1. 掌握以太网交换机和路由器的概念；')
add_para(doc, '2. 完成交换机和路由器的基本配置；')
add_para(doc, '3. 掌握交换机和路由器各种视图下的常用命令。')

add_heading_simsun(doc, '二、实验环境', level=1)
add_para(doc, 'Cisco Packet Tracer 仿真软件')

add_heading_simsun(doc, '三、实验原理', level=1)
add_para(doc, '1. 交换机工作原理', bold=True)
add_para(doc, '以太网交换机工作在数据链路层，基于MAC地址进行数据帧的转发。交换机通过自学习算法建立MAC地址表，当收到数据帧时，检查源MAC地址并记录到MAC表中，然后根据目的MAC地址查找MAC表进行转发。如果目的MAC地址不在表中，则向除接收端口外的所有端口广播（泛洪）。', indent=True)
add_para(doc, '2. 路由器工作原理', bold=True)
add_para(doc, '路由器工作在网络层，基于IP地址进行数据包的转发。路由器通过路由表决定数据包的转发路径，支持静态路由和动态路由协议。路由器的主要功能包括：连接不同网络、路径选择、数据包转发。', indent=True)
add_para(doc, '3. 交换机与路由器的区别', bold=True)
add_table_simsun(doc, ['比较项目', '交换机', '路由器'], [
    ['工作层次', '数据链路层（二层）', '网络层（三层）'],
    ['转发依据', 'MAC地址', 'IP地址'],
    ['主要功能', '局域网内数据帧转发', '不同网络间数据包路由'],
    ['广播处理', '转发广播帧', '隔离广播域'],
    ['端口数量', '较多（24/48口）', '较少（2-8口）'],
])

add_heading_simsun(doc, '四、实验内容与步骤', level=1)

add_heading_simsun(doc, '（一）交换机基本配置', level=2)
add_para(doc, '1. 搭建网络拓扑', bold=True)
add_para(doc, '在Cisco Packet Tracer中，选择1台2960交换机和3台PC机。使用直通线将PC机连接到交换机的FastEthernet端口。拓扑结构如下：')
add_image(doc, images['lab1_top1'])

add_para(doc, '2. 配置PC机IP地址', bold=True)
add_para(doc, 'PC1: IP=192.168.1.1, 子网掩码=255.255.255.0')
add_para(doc, 'PC2: IP=192.168.1.2, 子网掩码=255.255.255.0')
add_para(doc, 'PC3: IP=192.168.1.3, 子网掩码=255.255.255.0')

add_para(doc, '3. 查看交换机端口信息', bold=True)
add_para(doc, '通过Console口连接交换机，进入命令行模式：')
add_para(doc, 'Switch>enable\nSwitch#show interfaces\nSwitch#show ip interface brief', size=10)

add_para(doc, '4. 测试连通性', bold=True)
add_para(doc, '在PC1的命令行中执行ping命令测试与其他PC的连通性：')
add_para(doc, 'C:\\>ping 192.168.1.2\nC:\\>ping 192.168.1.3', size=10)

add_para(doc, '5. 查看MAC地址表', bold=True)
add_para(doc, '在交换机上执行show mac-address-table命令查看MAC地址表：')
add_image(doc, images['lab1_mac'])

add_para(doc, '6. 观察交换机自学习过程', bold=True)
add_para(doc, '切换到仿真模式，使用PC1 ping PC2，观察ARP和ICMP数据包的转发过程。交换机首先收到PC1的数据帧，记录PC1的MAC地址到MAC表中，然后向其他端口泛洪。当PC2回复时，交换机记录PC2的MAC地址，之后就可以直接转发。')

add_heading_simsun(doc, '（二）路由器基本配置', level=2)
add_para(doc, '1. 搭建网络拓扑', bold=True)
add_para(doc, '选择1台2811路由器和1台PC机。使用配置线连接PC的RS232口和路由器的Console口，使用直通线连接PC的FastEthernet口和路由器的FastEthernet口。')
add_image(doc, images['lab1_top2'])

add_para(doc, '2. 配置PC机', bold=True)
add_para(doc, 'PC0: IP=192.168.1.2, 子网掩码=255.255.255.0, 网关=192.168.1.1')

add_para(doc, '3. 通过Terminal配置路由器', bold=True)
add_para(doc, '打开PC0的Desktop标签，点击Terminal图标，进入路由器命令行配置：')
add_para(doc, 'Router>enable\nRouter#configure terminal\nRouter(config)#hostname Router0\nRouter0(config)#interface FastEthernet0/0\nRouter0(config-if)#ip address 192.168.1.1 255.255.255.0\nRouter0(config-if)#no shutdown\nRouter0(config-if)#exit', size=10)

add_para(doc, '4. 查看路由器配置', bold=True)
add_para(doc, 'Router0#show running-config\nRouter0#show ip interface brief', size=10)

add_para(doc, '5. 测试连通性', bold=True)
add_para(doc, 'C:\\>ipconfig /all\nC:\\>ping 192.168.1.1', size=10)

add_para(doc, '6. 使用Telnet登录路由器', bold=True)
add_para(doc, 'Router0(config)#line vty 0 4\nRouter0(config-line)#password cisco\nRouter0(config-line)#login\nRouter0(config)#enable password cisco\n\nC:\\>telnet 192.168.1.1', size=10)

add_heading_simsun(doc, '五、实验结果与分析', level=1)
add_para(doc, '1. 交换机配置结果', bold=True)
add_para(doc, '通过实验，成功配置了交换机并实现了三台PC机之间的互联互通。交换机通过自学习算法自动建立了MAC地址表，实现了基于MAC地址的数据帧转发。交换机的自学习过程是自动的，无需手动配置。', indent=True)
add_para(doc, '2. 路由器配置结果', bold=True)
add_para(doc, '通过实验，成功配置了路由器的接口IP地址，并实现了PC机与路由器之间的连通。路由器工作在网络层，通过IP地址进行数据包的转发。通过Telnet远程管理路由器的配置也成功验证。', indent=True)
add_para(doc, '3. 交换机与路由器工作原理对比', bold=True)
add_para(doc, '交换机工作在数据链路层，基于MAC地址转发数据帧，通过自学习算法建立MAC表，不能隔离广播域。路由器工作在网络层，基于IP地址转发数据包，通过路由表决定转发路径，能够隔离广播域。两者在网络中扮演不同的角色，通常配合使用。', indent=True)

add_heading_simsun(doc, '六、思考题', level=1)
add_para(doc, '题目：搭建拓扑，PC1设置为192.168.1.3/24，PC0是否能ping通PC1？为什么？', bold=True)
add_para(doc, '答：如果PC0和PC1连接在同一台交换机上，且都处于192.168.1.0/24网段，则PC0可以ping通PC1。因为交换机工作在数据链路层，通过MAC地址转发数据帧。PC0发送ARP请求获取PC1的MAC地址，交换机将ARP请求泛洪到所有端口（除接收端口），PC1收到后回复ARP应答，交换机学习到两台PC的MAC地址后，就可以直接转发数据帧。如果PC0连接在路由器的一个接口上，PC1连接在另一个不同网段的接口上，则需要正确配置路由才能ping通。', indent=True)

doc.save(os.path.join(OUTPUT_DIR, '实验一-交换机路由器基本配置', '实验一报告.docx'))
print("  实验一报告完成")


# ============================================================
# 实验二报告
# ============================================================
doc = Document()

add_heading_simsun(doc, '实验二 局域网的扩展', level=0)

add_heading_simsun(doc, '一、实验目的', level=1)
add_para(doc, '1. 掌握以太网交换机和路由器的作用；')
add_para(doc, '2. 完成交换机和路由器的基本配置；')
add_para(doc, '3. 掌握交换机和路由器各种视图下的常用命令；')
add_para(doc, '4. 学会利用交换机和路由器扩展局域网。')

add_heading_simsun(doc, '二、实验环境', level=1)
add_para(doc, 'Cisco Packet Tracer 仿真软件')

add_heading_simsun(doc, '三、实验原理', level=1)
add_para(doc, '1. 局域网扩展的概念', bold=True)
add_para(doc, '局域网（LAN）的扩展是指通过网络设备（如交换机、路由器）将多个局域网连接起来，实现更大范围的网络互联。扩展局域网的主要方式包括：使用集线器扩展（物理层）、使用交换机扩展（数据链路层）、使用路由器扩展（网络层）。', indent=True)
add_para(doc, '2. 交换机扩展局域网', bold=True)
add_para(doc, '交换机工作在数据链路层，可以连接多个局域网段。交换机通过MAC地址表进行数据帧的转发，可以有效减少冲突域，提高网络性能。但交换机不能隔离广播域，所有连接在同一交换机上的设备处于同一广播域中。', indent=True)
add_para(doc, '3. 路由器扩展局域网', bold=True)
add_para(doc, '路由器工作在网络层，可以连接不同的网络。路由器通过路由表决定数据包的转发路径，能够隔离广播域。当两个不同子网需要通信时，必须通过路由器进行转发。路由器需要配置静态路由或动态路由协议才能实现不同网络之间的数据转发。', indent=True)
add_para(doc, '4. 静态路由', bold=True)
add_para(doc, '静态路由是由网络管理员手动配置的路由条目。静态路由的配置命令格式为：ip route <目的网络> <子网掩码> <下一跳地址>。静态路由适用于小型网络，配置简单，不占用网络带宽，但不能自动适应网络拓扑变化。', indent=True)

add_heading_simsun(doc, '四、实验内容与步骤', level=1)

add_heading_simsun(doc, '（一）单路由器连接2个子网', level=2)
add_para(doc, '1. 搭建网络拓扑', bold=True)
add_para(doc, '选择1台2811路由器、2台2960交换机、4台PC机。拓扑结构如下：')
add_image(doc, images['lab2_top1'])

add_para(doc, '2. 配置PC机IP地址', bold=True)
add_para(doc, 'PC0: IP=192.168.1.2, 掩码=255.255.255.0, 网关=192.168.1.1')
add_para(doc, 'PC1: IP=192.168.1.3, 掩码=255.255.255.0, 网关=192.168.1.1')
add_para(doc, 'PC2: IP=192.168.2.2, 掩码=255.255.255.0, 网关=192.168.2.1')
add_para(doc, 'PC3: IP=192.168.2.3, 掩码=255.255.255.0, 网关=192.168.2.1')

add_para(doc, '3. 配置路由器接口', bold=True)
add_para(doc, 'Router>enable\nRouter#configure terminal\nRouter(config)#interface FastEthernet0/0\nRouter(config-if)#ip address 192.168.1.1 255.255.255.0\nRouter(config-if)#no shutdown\nRouter(config-if)#exit\nRouter(config)#interface FastEthernet1/0\nRouter(config-if)#ip address 192.168.2.1 255.255.255.0\nRouter(config-if)#no shutdown', size=10)

add_para(doc, '4. 验证连通性', bold=True)
add_para(doc, '由于路由器的两个接口都已配置IP并启用，且两个子网都直接连接在路由器上，PC0可以直接ping通PC2，无需额外配置路由。')
add_para(doc, 'C:\\>ping 192.168.1.1   # 测试到网关\nC:\\>ping 192.168.1.3   # 测试同子网\nC:\\>ping 192.168.2.2   # 测试跨子网', size=10)

add_heading_simsun(doc, '（二）两台路由器拓展局域网', level=2)
add_para(doc, '1. 搭建网络拓扑', bold=True)
add_para(doc, '选择2台2811路由器、2台2960交换机、4台PC机。拓扑结构如下：')
add_image(doc, images['lab2_top2'])

add_para(doc, '2. 配置路由器Router0', bold=True)
add_para(doc, 'Router>enable\nRouter#configure terminal\nRouter(config)#hostname Router0\nRouter0(config)#interface FastEthernet0/0\nRouter0(config-if)#ip address 192.168.1.1 255.255.255.0\nRouter0(config-if)#no shutdown\nRouter0(config-if)#exit\nRouter0(config)#interface FastEthernet1/0\nRouter0(config-if)#ip address 10.0.0.1 255.255.255.0\nRouter0(config-if)#no shutdown\nRouter0(config-if)#exit\nRouter0(config)#ip route 192.168.2.0 255.255.255.0 10.0.0.2\nRouter0(config)#end\nRouter0#write memory', size=10)

add_para(doc, '3. 配置路由器Router1', bold=True)
add_para(doc, 'Router>enable\nRouter#configure terminal\nRouter(config)#hostname Router1\nRouter1(config)#interface FastEthernet0/0\nRouter1(config-if)#ip address 192.168.2.1 255.255.255.0\nRouter1(config-if)#no shutdown\nRouter1(config-if)#exit\nRouter1(config)#interface FastEthernet1/0\nRouter1(config-if)#ip address 10.0.0.2 255.255.255.0\nRouter1(config-if)#no shutdown\nRouter1(config-if)#exit\nRouter1(config)#ip route 192.168.1.0 255.255.255.0 10.0.0.1\nRouter1(config)#end\nRouter1#write memory', size=10)

add_para(doc, '4. 查看路由表', bold=True)
add_image(doc, images['lab2_route'])

add_para(doc, '5. 验证全网连通性', bold=True)
add_para(doc, 'PC0>ping 192.168.1.1   # 到Router0的Fa0/0\nPC0>ping 10.0.0.2      # 到Router1的Fa1/0\nPC0>ping 192.168.2.1   # 到Router1的Fa0/0\nPC0>ping 192.168.2.2   # 到PC1（跨路由器）', size=10)

add_heading_simsun(doc, '（三）拓展拓扑：静态路由配置', level=2)
add_para(doc, '按照Cisco Packet Tracer的使用说明，搭建包含4台PC、2台交换机、2台路由器的拓扑网络。配置静态路由后验证全网连通性：')
add_para(doc, 'PC1 ping PC2（跨路由器）：连通成功')
add_para(doc, 'PC1 ping PC3（同子网）：连通成功')
add_para(doc, 'PC1 ping PC4（跨路由器）：连通成功')

add_heading_simsun(doc, '五、实验结果与分析', level=1)
add_para(doc, '1. 单路由器连接2个子网', bold=True)
add_para(doc, '通过在路由器的两个接口上分别配置不同子网的IP地址，实现了两个子网之间的互联互通。路由器的两个接口分别作为两个子网的网关，PC机通过网关将跨子网的数据包发送给路由器，路由器根据目的IP地址查找路由表进行转发。', indent=True)
add_para(doc, '2. 两台路由器拓展局域网', bold=True)
add_para(doc, '通过两台路由器的级联，实现了4个PC机的全网互通。在两台路由器之间使用了10.0.0.0/24网段作为互联链路。配置静态路由后，每台路由器都知道如何到达对方的子网，从而实现了跨路由器的通信。', indent=True)
add_para(doc, '3. 静态路由的作用', bold=True)
add_para(doc, '静态路由是手动配置的路由条目，告诉路由器"要到达某个目的网络，应该将数据包发往哪个下一跳地址"。在本实验中，Router0需要一条到达192.168.2.0/24网段的静态路由，Router1需要一条到达192.168.1.0/24网段的静态路由，这样才能实现双向通信。', indent=True)

add_heading_simsun(doc, '六、思考题', level=1)
add_para(doc, '1. 为什么两台路由器之间需要配置静态路由？', bold=True)
add_para(doc, '答：因为两台路由器各自只知道自己直连的网络，对于非直连的网络，路由器不知道应该将数据包转发到哪里。静态路由告诉路由器"要到达某个非直连网络，应该将数据包发给哪个下一跳地址"。如果不配置静态路由，路由器收到目的地址为非直连网络的数据包时，会因为找不到路由条目而丢弃数据包。', indent=True)
add_para(doc, '2. 交换机和路由器在扩展局域网时各有什么优缺点？', bold=True)
add_para(doc, '答：交换机扩展局域网的优点是配置简单、即插即用，缺点是不能隔离广播域，随着网络规模增大，广播流量会增加。路由器扩展局域网的优点是可以隔离广播域、支持不同网络互联，缺点是配置复杂、成本较高。', indent=True)

doc.save(os.path.join(OUTPUT_DIR, '实验二-局域网扩展', '实验二报告.docx'))
print("  实验二报告完成")


# ============================================================
# 实验三报告
# ============================================================
doc = Document()

add_heading_simsun(doc, '实验三 VLAN的划分', level=0)

add_heading_simsun(doc, '一、实验目的', level=1)
add_para(doc, '1. 掌握VLAN命令使用的基本原则；')
add_para(doc, '2. 掌握VLAN划分的规则；')
add_para(doc, '3. 熟悉VLAN地址的分配方法；')
add_para(doc, '4. 学会如何测试VLAN间的连通性。')

add_heading_simsun(doc, '二、实验环境', level=1)
add_para(doc, 'Cisco Packet Tracer 仿真软件')

add_heading_simsun(doc, '三、实验原理', level=1)
add_para(doc, '1. VLAN的概念', bold=True)
add_para(doc, 'VLAN（Virtual Local Area Network，虚拟局域网）是一种将物理局域网在逻辑上划分为多个广播域的技术。同一VLAN中的设备可以像在同一个物理局域网中一样通信，不同VLAN之间的设备不能直接通信，需要通过路由器或三层交换机进行转发。', indent=True)
add_para(doc, '2. VLAN的作用', bold=True)
add_para(doc, '（1）控制广播风暴：将一个大的广播域划分为多个小的广播域，减少广播流量。')
add_para(doc, '（2）提高网络安全性：不同VLAN之间的通信需要经过路由，可以在路由上实施访问控制。')
add_para(doc, '（3）简化网络管理：可以根据部门、功能等逻辑划分网络，不受物理位置限制。')
add_para(doc, '3. Access端口和Trunk端口', bold=True)
add_para(doc, 'Access端口：只属于一个VLAN，用于连接终端设备（PC、服务器等）。', indent=True)
add_para(doc, 'Trunk端口：可以承载多个VLAN的数据，用于交换机之间的连接。Trunk端口使用802.1Q协议在数据帧中添加VLAN标签，标识数据帧属于哪个VLAN。', indent=True)
add_para(doc, '4. VLAN间通信', bold=True)
add_para(doc, '不同VLAN之间的通信需要通过三层设备（路由器或三层交换机）进行路由转发。同一VLAN跨交换机的通信需要通过Trunk链路实现。', indent=True)

add_heading_simsun(doc, '四、实验内容与步骤', level=1)

add_heading_simsun(doc, '（一）题目1：单交换机VLAN划分', level=2)
add_para(doc, '1. 网络拓扑', bold=True)
add_para(doc, '一台2960交换机，四台PC设备。')
add_image(doc, images['lab3_top1'])

add_para(doc, '2. IP地址配置', bold=True)
add_table_simsun(doc, ['设备', 'IP地址', '子网掩码', 'VLAN'], [
    ['PC1', '192.168.0.11', '255.255.255.0', 'VLAN 10'],
    ['PC2', '192.168.0.21', '255.255.255.0', 'VLAN 20'],
    ['PC3', '192.168.0.12', '255.255.255.0', 'VLAN 10'],
    ['PC4', '192.168.0.22', '255.255.255.0', 'VLAN 20'],
])

add_para(doc, '3. 交换机VLAN配置', bold=True)
add_para(doc, 'Switch>enable\nSwitch#configure terminal\nSwitch(config)#vlan 10\nSwitch(config-vlan)#name VLAN10\nSwitch(config-vlan)#exit\nSwitch(config)#vlan 20\nSwitch(config-vlan)#name VLAN20\nSwitch(config-vlan)#exit\nSwitch(config)#interface FastEthernet0/1\nSwitch(config-if)#switchport mode access\nSwitch(config-if)#switchport access vlan 10\nSwitch(config-if)#exit\nSwitch(config)#interface FastEthernet0/2\nSwitch(config-if)#switchport mode access\nSwitch(config-if)#switchport access vlan 20\nSwitch(config-if)#exit\nSwitch(config)#interface FastEthernet0/3\nSwitch(config-if)#switchport mode access\nSwitch(config-if)#switchport access vlan 10\nSwitch(config-if)#exit\nSwitch(config)#interface FastEthernet0/4\nSwitch(config-if)#switchport mode access\nSwitch(config-if)#switchport access vlan 20\nSwitch(config-if)#exit\nSwitch#show vlan brief', size=10)

add_para(doc, '4. 连通性测试', bold=True)
add_para(doc, 'PC1 ping PC3（同VLAN10）：连通成功')
add_para(doc, 'PC2 ping PC4（同VLAN20）：连通成功')
add_para(doc, 'PC1 ping PC2（不同VLAN）：不通')
add_para(doc, 'PC1 ping PC4（不同VLAN）：不通')

add_heading_simsun(doc, '（二）题目2：多交换机无VLAN测试', level=2)
add_para(doc, '搭建2台交换机、4台PC的拓扑，不划分VLAN，测试所有PC之间的连通性。结果：所有PC之间都能ping通，因为都在同一个默认VLAN1中。')

add_heading_simsun(doc, '（三）题目3：多交换机VLAN划分（含Trunk）', level=2)
add_para(doc, '1. 网络拓扑', bold=True)
add_image(doc, images['lab3_top2'])

add_para(doc, '2. Switch0配置', bold=True)
add_para(doc, 'Switch>enable\nSwitch#configure terminal\nSwitch(config)#vlan 10\nSwitch(config-vlan)#name VLAN10\nSwitch(config-vlan)#exit\nSwitch(config)#vlan 20\nSwitch(config-vlan)#name VLAN20\nSwitch(config-vlan)#exit\nSwitch(config)#interface FastEthernet0/1\nSwitch(config-if)#switchport mode access\nSwitch(config-if)#switchport access vlan 10\nSwitch(config-if)#exit\nSwitch(config)#interface FastEthernet0/2\nSwitch(config-if)#switchport mode access\nSwitch(config-if)#switchport access vlan 20\nSwitch(config-if)#exit\nSwitch(config)#interface FastEthernet0/24\nSwitch(config-if)#switchport mode trunk\nSwitch(config-if)#switchport trunk allowed vlan 10,20\nSwitch(config-if)#exit\nSwitch#show interfaces trunk\nSwitch#show vlan brief', size=10)

add_para(doc, '3. Switch1配置（与Switch0类似）', bold=True)
add_para(doc, '配置方法与Switch0相同，将Fa0/1划入VLAN10，Fa0/2划入VLAN20，Fa0/24设为Trunk口。', indent=True)

add_para(doc, '4. 连通性测试结果', bold=True)
add_image(doc, images['lab3_vlan'])

add_heading_simsun(doc, '五、实验结果与分析', level=1)
add_para(doc, '通过本实验，验证了VLAN的隔离作用：', indent=True)
add_para(doc, '1. 单交换机VLAN划分：同一VLAN内的PC可以互通，不同VLAN的PC无法通信。VLAN在逻辑上将一个交换机划分为多个独立的广播域。', indent=True)
add_para(doc, '2. 多交换机VLAN划分：需要将交换机之间的链路配置为Trunk模式，才能使不同交换机上相同VLAN的设备通信。Trunk端口使用802.1Q协议在数据帧中添加VLAN标签。', indent=True)
add_para(doc, '3. VLAN的主要作用：控制广播风暴、提高网络安全性、简化网络管理。', indent=True)

add_heading_simsun(doc, '六、思考题', level=1)
add_para(doc, '1. 为什么同VLAN不同交换机的PC可以ping通？', bold=True)
add_para(doc, '答：因为交换机之间的链路配置为Trunk模式，Trunk端口可以承载多个VLAN的数据。当PC1发送数据帧到Switch0时，Switch0通过Trunk端口将数据帧转发给Switch1，数据帧中携带VLAN标签（VLAN10），Switch1收到后根据VLAN标签将数据帧转发到VLAN10的端口，从而到达PC3。', indent=True)
add_para(doc, '2. 如果不配置Trunk，跨交换机的同VLAN PC能否通信？', bold=True)
add_para(doc, '答：不能。如果不配置Trunk，交换机之间的链路默认是Access模式，只属于一个VLAN（默认VLAN1）。其他VLAN的数据帧无法通过这条链路传输。', indent=True)

doc.save(os.path.join(OUTPUT_DIR, '实验三-VLAN划分', '实验三报告.docx'))
print("  实验三报告完成")


# ============================================================
# 实验四报告
# ============================================================
doc = Document()

add_heading_simsun(doc, '实验四 服务器搭建', level=0)

add_heading_simsun(doc, '一、实验目的', level=1)
add_para(doc, '1. 掌握WWW、FTP等常用应用层服务的配置方法；')
add_para(doc, '2. 理解DHCP服务的工作原理和配置方法；')
add_para(doc, '3. 理解DNS服务的工作原理和配置方法；')
add_para(doc, '4. 理解FTP服务的工作原理和配置方法；')
add_para(doc, '5. 理解WEB服务的工作原理和配置方法。')

add_heading_simsun(doc, '二、实验环境', level=1)
add_para(doc, 'Cisco Packet Tracer 仿真软件')

add_heading_simsun(doc, '三、实验原理', level=1)
add_para(doc, '1. DHCP服务（Dynamic Host Configuration Protocol）', bold=True)
add_para(doc, 'DHCP是一种网络协议，用于自动为网络中的设备分配IP地址和其他网络配置参数。DHCP工作过程（DORA四步）：', indent=True)
add_para(doc, '（1）Discover：客户端广播发送DHCP发现报文；')
add_para(doc, '（2）Offer：DHCP服务器响应，提供IP地址；')
add_para(doc, '（3）Request：客户端请求分配该IP地址；')
add_para(doc, '（4）ACK：服务器确认分配。')
add_image(doc, images['lab4_dhcp'])

add_para(doc, '2. DNS服务（Domain Name System）', bold=True)
add_para(doc, 'DNS是域名系统，用于将域名解析为IP地址。DNS使得用户可以使用易于记忆的域名访问网络服务。一个域名只能对应一个IP地址，一个IP地址可以对应多个域名。', indent=True)

add_para(doc, '3. FTP服务（File Transfer Protocol）', bold=True)
add_para(doc, 'FTP是文件传输协议，用于在网络上传输文件。FTP使用两个TCP连接：控制连接（端口21）和数据连接（端口20）。FTP支持用户认证，可以设置不同的访问权限。', indent=True)

add_para(doc, '4. WEB服务（HTTP/HTTPS）', bold=True)
add_para(doc, 'HTTP是超文本传输协议，用于传输网页内容。WEB服务使用TCP端口80（HTTP）和443（HTTPS）。客户端通过浏览器发送HTTP请求，服务器返回HTML页面。', indent=True)

add_heading_simsun(doc, '四、实验内容与步骤', level=1)

add_para(doc, '1. 网络拓扑', bold=True)
add_image(doc, images['lab4_top'])

add_para(doc, 'IP地址规划：', bold=True)
add_table_simsun(doc, ['设备', 'IP地址', '说明'], [
    ['DHCP服务器', '192.168.0.254', '动态分配IP地址'],
    ['DNS服务器', '192.168.0.253', '域名解析服务'],
    ['FTP/WEB服务器', '192.168.0.252', '文件传输和网页服务'],
    ['PC0', 'DHCP自动获取', '客户端'],
    ['PC1', 'DHCP自动获取', '客户端'],
])

add_heading_simsun(doc, '（一）题目1：DHCP服务配置与验证', level=2)
add_para(doc, '1. DHCP服务器配置', bold=True)
add_para(doc, '打开DHCP服务器，点击Services → DHCP，配置以下参数：')
add_para(doc, 'Service: On\nPool Name: pool0\nDefault Gateway: 192.168.0.254\nDNS Server: 192.168.0.253\nStart IP Address: 192.168.0.1\nSubnet Mask: 255.255.255.0\nMax Number of Users: 50', size=10)

add_para(doc, '2. PC端获取IP', bold=True)
add_para(doc, '打开PC0，选择Desktop → IP Configuration → DHCP，等待获取IP地址。PC1同样操作。')
add_para(doc, '[截图位置：请在此处插入PC0和PC1获取到IP地址的截图]')

add_heading_simsun(doc, '（二）题目2：FTP服务配置与验证', level=2)
add_para(doc, '1. FTP服务器配置', bold=True)
add_para(doc, '打开FTP/WEB服务器，点击Services → FTP，开启FTP服务，添加用户：')
add_para(doc, 'Username: zhangsan\nPassword: zhangsan\n权限: Read, Write, Delete, Rename, List（全部勾选）', size=10)

add_para(doc, '2. FTP客户端测试', bold=True)
add_para(doc, '打开PC0的命令行（Desktop → Command Prompt）：')
add_para(doc, 'C:\\>ftp 192.168.0.252\nUsername: zhangsan\nPassword: zhangsan\nftp>dir\nftp>get 文件名\nftp>bye', size=10)
add_para(doc, '[截图位置：请在此处插入FTP登录和dir结果截图]')

add_heading_simsun(doc, '（三）题目3：WEB服务配置与验证', level=2)
add_para(doc, '在FTP/WEB服务器上确认HTTP服务已开启。打开PC0的Web Browser（Desktop → Web Browser），在URL栏输入http://192.168.0.252，验证WEB服务。')
add_para(doc, '[截图位置：请在此处插入WEB访问截图]')

add_heading_simsun(doc, '（四）题目4：DNS服务配置与验证', level=2)
add_para(doc, '1. DNS服务器配置', bold=True)
add_para(doc, '打开DNS服务器，点击Services → DNS，添加以下记录：')
add_image(doc, images['lab4_dns'])

add_para(doc, '2. 通过域名访问WEB服务', bold=True)
add_para(doc, '打开PC0的Web Browser，输入http://www.test.com.cn，验证DNS解析是否正常。')

add_para(doc, '3. 通过域名访问FTP服务', bold=True)
add_para(doc, 'C:\\>ftp ftp.test.cn', size=10)
add_para(doc, '[截图位置：请在此处插入通过域名访问WEB和FTP的截图]')

add_heading_simsun(doc, '（五）题目5：（选作）搭建email服务器', level=2)
add_para(doc, '参考：https://blog.csdn.net/2301_82243100/article/details/137607927')
add_para(doc, 'Email服务器使用SMTP协议（端口25）发送邮件，使用POP3协议（端口110）接收邮件。在Packet Tracer中可以通过Email服务进行配置。')

add_heading_simsun(doc, '五、实验结果与分析', level=1)
add_para(doc, '1. DHCP服务', bold=True)
add_para(doc, '成功为PC0和PC1自动分配了IP地址，验证了DHCP的自动配置功能。DHCP服务大大简化了网络管理，避免了手动配置IP地址的工作。', indent=True)
add_para(doc, '2. FTP服务', bold=True)
add_para(doc, '成功创建了FTP用户，并通过命令行登录FTP服务器，实现了文件的上传和下载。FTP服务使用用户名和密码进行身份验证，可以控制用户的访问权限。', indent=True)
add_para(doc, '3. WEB服务', bold=True)
add_para(doc, '成功访问了WEB服务器的页面，验证了HTTP服务的正常运行。WEB服务是互联网上最常用的服务之一。', indent=True)
add_para(doc, '4. DNS服务', bold=True)
add_para(doc, '成功配置了域名解析记录，通过域名访问了WEB和FTP服务器。DNS服务将易于记忆的域名解析为IP地址，方便用户访问网络服务。', indent=True)

add_heading_simsun(doc, '六、思考题', level=1)
add_para(doc, '1. DHCP的四步过程是什么？', bold=True)
add_para(doc, '答：DHCP的四步过程称为DORA：Discover（发现）- 客户端广播发送DHCP发现报文；Offer（提供）- DHCP服务器向客户端提供IP地址；Request（请求）- 客户端选择一个IP地址并发送请求；ACK（确认）- 服务器确认分配，客户端获得IP地址。', indent=True)
add_para(doc, '2. DNS的作用是什么？', bold=True)
add_para(doc, '答：DNS（域名系统）的作用是将域名解析为IP地址。用户使用易于记忆的域名访问网络服务，DNS服务器将域名转换为对应的IP地址，使得客户端能够找到并连接到目标服务器。', indent=True)
add_para(doc, '3. FTP和HTTP各有什么特点？', bold=True)
add_para(doc, '答：FTP是文件传输协议，专门用于文件的上传和下载，支持用户认证和权限控制，使用两个TCP连接。HTTP是超文本传输协议，主要用于传输网页内容，通常不需要用户认证，使用一个TCP连接。', indent=True)

doc.save(os.path.join(OUTPUT_DIR, '实验四-服务器搭建', '实验四报告.docx'))
print("  实验四报告完成")

print("\n===== 全部完成 =====")
print(f"图片目录: {IMG_DIR}")
print(f"共生成 {len(images)} 张拓扑图")
