# -*- coding: utf-8 -*-
"""生成实验三VLAN划分实验报告"""

import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn


def set_cell_text(cell, text, bold=False, alignment=WD_ALIGN_PARAGRAPH.CENTER):
    """设置单元格文本和格式"""
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = alignment
    run = p.add_run(text)
    run.font.size = Pt(10.5)
    run.bold = bold
    run.font.name = "宋体"
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')


def add_heading_styled(doc, text, level=1):
    """添加标题"""
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        run.font.name = "黑体"
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    return heading


def add_paragraph_styled(doc, text, bold=False, indent=False, font_size=12):
    """添加段落"""
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Cm(0.74)
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    run.bold = bold
    run.font.name = "宋体"
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    return p


def add_code_block(doc, text):
    """添加代码块（用等宽字体，灰色背景模拟）"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.name = "Consolas"
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    return p


def add_screenshot_placeholder(doc, desc):
    """添加截图占位符"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"[截图位置：请在此处插入{desc}截图]")
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
    run.font.name = "宋体"
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    return p


def create_report():
    doc = Document()

    # 设置默认字体
    style = doc.styles['Normal']
    font = style.font
    font.name = '宋体'
    font.size = Pt(12)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # ========== 标题 ==========
    title = doc.add_heading("", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("实验三 VLAN的划分")
    run.font.size = Pt(22)
    run.font.name = "黑体"
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    # ========== 一、实验目的 ==========
    add_heading_styled(doc, "一、实验目的", level=1)
    purposes = [
        "掌握VLAN命令使用的基本原则",
        "掌握VLAN划分的规则",
        "熟悉VLAN地址的分配方法",
        "学会如何测试VLAN间的连通性"
    ]
    for i, p_text in enumerate(purposes, 1):
        p = doc.add_paragraph()
        run = p.add_run(f"{i}. {p_text}")
        run.font.size = Pt(12)
        run.font.name = "宋体"
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # ========== 二、实验环境 ==========
    add_heading_styled(doc, "二、实验环境", level=1)
    add_paragraph_styled(doc, "Cisco Packet Tracer 仿真软件")

    # ========== 三、实验原理 ==========
    add_heading_styled(doc, "三、实验原理", level=1)

    # 1. VLAN的概念
    add_heading_styled(doc, "1. VLAN的概念", level=2)
    add_paragraph_styled(doc,
        "VLAN（Virtual Local Area Network，虚拟局域网）是一种将物理局域网在逻辑上划分为多个广播域的技术。"
        "同一VLAN中的设备可以像在同一个物理局域网中一样通信，不同VLAN之间的设备不能直接通信，需要通过路由器或三层交换机进行转发。",
        indent=True)

    # 2. VLAN的作用
    add_heading_styled(doc, "2. VLAN的作用", level=2)
    add_paragraph_styled(doc, "（1）控制广播风暴：将一个大的广播域划分为多个小的广播域，减少广播流量。广播报文只在同一VLAN内转发，不会扩散到其他VLAN，从而有效控制广播风暴的产生。", indent=True)
    add_paragraph_styled(doc, "（2）提高网络安全性：不同VLAN之间的通信需要经过路由，可以在路由上实施访问控制策略（如ACL），从而提高网络的安全性。", indent=True)
    add_paragraph_styled(doc, "（3）简化网络管理：可以根据部门、功能等逻辑划分网络，不受物理位置限制。当用户物理位置发生变化时，只需修改VLAN配置，无需重新布线。", indent=True)

    # 3. VLAN的类型
    add_heading_styled(doc, "3. VLAN的类型", level=2)
    add_paragraph_styled(doc, "（1）基于端口的VLAN：将交换机的端口分配到不同的VLAN中，这是最常用也是最简单的VLAN划分方式。本实验采用的就是基于端口的VLAN划分方法。", indent=True)
    add_paragraph_styled(doc, "（2）基于MAC地址的VLAN：根据设备的MAC地址来划分VLAN，同一MAC地址的设备无论连接到哪个端口都属于同一个VLAN。", indent=True)
    add_paragraph_styled(doc, "（3）基于网络层的VLAN：根据网络层协议类型或IP地址来划分VLAN。", indent=True)

    # 4. Access端口和Trunk端口
    add_heading_styled(doc, "4. Access端口和Trunk端口", level=2)
    add_paragraph_styled(doc,
        "Access端口：只属于一个VLAN，用于连接终端设备（PC、服务器等）。Access端口在发送数据时会去掉VLAN标签，"
        "在接收数据时会给数据帧打上该端口所属VLAN的标签。",
        indent=True)
    add_paragraph_styled(doc,
        "Trunk端口：可以承载多个VLAN的数据，用于交换机之间的连接。Trunk端口使用802.1Q协议在数据帧中添加VLAN标签，"
        "标识数据帧属于哪个VLAN。当Trunk端口收到不带标签的数据帧时，会将其划分到默认VLAN（通常是VLAN1）中。",
        indent=True)

    # 5. VLAN间通信
    add_heading_styled(doc, "5. VLAN间通信", level=2)
    add_paragraph_styled(doc,
        "不同VLAN之间的通信需要通过三层设备（路由器或三层交换机）进行路由转发。"
        "这是因为VLAN在数据链路层实现了广播域的隔离，不同VLAN之间的通信需要在网络层进行路由。"
        "常用的VLAN间路由方法有：单臂路由（Router-on-a-Stick）和三层交换机路由。",
        indent=True)

    # ========== 四、实验内容与步骤 ==========
    add_heading_styled(doc, "四、实验内容与步骤", level=1)

    # ---------- 题目1 ----------
    add_heading_styled(doc, "题目1：单交换机VLAN划分", level=2)

    add_heading_styled(doc, "1. 网络拓扑搭建", level=3)
    add_paragraph_styled(doc,
        "在Cisco Packet Tracer中搭建网络拓扑：1台2960交换机（Switch0），4台PC（PC1、PC2、PC3、PC4）。"
        "将PC1连接到Fa0/1端口，PC2连接到Fa0/2端口，PC3连接到Fa0/3端口，PC4连接到Fa0/4端口。",
        indent=True)
    add_screenshot_placeholder(doc, "单交换机VLAN拓扑")

    add_heading_styled(doc, "2. 配置PC的IP地址", level=3)
    add_paragraph_styled(doc, "按照下表配置各PC的IP地址和子网掩码：", indent=True)

    # IP地址表格
    table = doc.add_table(rows=5, cols=3)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["设备", "IP地址", "子网掩码"]
    for i, h in enumerate(headers):
        set_cell_text(table.rows[0].cells[i], h, bold=True)
    data = [
        ("PC1", "192.168.0.11", "255.255.255.0"),
        ("PC2", "192.168.0.21", "255.255.255.0"),
        ("PC3", "192.168.0.12", "255.255.255.0"),
        ("PC4", "192.168.0.22", "255.255.255.0"),
    ]
    for r, (dev, ip, mask) in enumerate(data, 1):
        set_cell_text(table.rows[r].cells[0], dev)
        set_cell_text(table.rows[r].cells[1], ip)
        set_cell_text(table.rows[r].cells[2], mask)

    add_screenshot_placeholder(doc, "PC1的IP地址配置")

    add_heading_styled(doc, "3. 创建VLAN并分配端口", level=3)
    add_paragraph_styled(doc,
        "在交换机上创建VLAN10和VLAN20，将Fa0/1和Fa0/3分配到VLAN10，Fa0/2和Fa0/4分配到VLAN20。"
        "具体配置命令如下：",
        indent=True)

    commands1 = """Switch>enable
Switch#configure terminal
Switch(config)#vlan 10
Switch(config-vlan)#name VLAN10
Switch(config-vlan)#exit
Switch(config)#vlan 20
Switch(config-vlan)#name VLAN20
Switch(config-vlan)#exit
Switch(config)#interface FastEthernet0/1
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 10
Switch(config-if)#exit
Switch(config)#interface FastEthernet0/2
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 20
Switch(config-if)#exit
Switch(config)#interface FastEthernet0/3
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 10
Switch(config-if)#exit
Switch(config)#interface FastEthernet0/4
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 20
Switch(config-if)#exit
Switch(config)#end
Switch#write memory"""

    add_code_block(doc, commands1)

    add_heading_styled(doc, "4. 查看VLAN配置", level=3)
    add_paragraph_styled(doc, "使用show vlan brief命令查看VLAN配置结果：", indent=True)

    vlan_output = """Switch#show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/5, Fa0/6, Fa0/7, Fa0/8
                                                Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                Fa0/13, Fa0/14, Fa0/15, Fa0/16
                                                Fa0/17, Fa0/18, Fa0/19, Fa0/20
                                                Fa0/21, Fa0/22, Fa0/23, Fa0/24
                                                Gig0/1, Gig0/2
10   VLAN10                           active    Fa0/1, Fa0/3
20   VLAN20                           active    Fa0/2, Fa0/4"""

    add_code_block(doc, vlan_output)
    add_screenshot_placeholder(doc, "show vlan brief命令输出")

    add_heading_styled(doc, "5. 连通性测试", level=3)
    add_paragraph_styled(doc, "使用ping命令测试各PC之间的连通性：", indent=True)

    add_paragraph_styled(doc, "（1）PC1 ping PC3（同VLAN10）：", indent=True)
    add_paragraph_styled(doc, "结果：ping通。PC1和PC3都属于VLAN10，在同一个广播域内，可以正常通信。", indent=True)
    add_screenshot_placeholder(doc, "PC1 ping PC3结果")

    add_paragraph_styled(doc, "（2）PC2 ping PC4（同VLAN20）：", indent=True)
    add_paragraph_styled(doc, "结果：ping通。PC2和PC4都属于VLAN20，在同一个广播域内，可以正常通信。", indent=True)
    add_screenshot_placeholder(doc, "PC2 ping PC4结果")

    add_paragraph_styled(doc, "（3）PC1 ping PC2（不同VLAN）：", indent=True)
    add_paragraph_styled(doc, "结果：ping不通。PC1属于VLAN10，PC2属于VLAN20，不同VLAN之间无法直接通信。", indent=True)
    add_screenshot_placeholder(doc, "PC1 ping PC2结果")

    add_paragraph_styled(doc, "（4）PC1 ping PC4（不同VLAN）：", indent=True)
    add_paragraph_styled(doc, "结果：ping不通。PC1属于VLAN10，PC4属于VLAN20，不同VLAN之间无法直接通信。", indent=True)
    add_screenshot_placeholder(doc, "PC1 ping PC4结果")

    add_heading_styled(doc, "6. 结果分析", level=3)
    add_paragraph_styled(doc,
        "从测试结果可以看出，同一VLAN内的PC（PC1与PC3、PC2与PC4）可以互相ping通，"
        "而不同VLAN之间的PC（PC1与PC2、PC1与PC4）无法ping通。这说明VLAN的作用是隔离广播域，"
        "不同VLAN之间的设备无法直接通信。交换机通过VLAN标签来区分不同VLAN的数据帧，"
        "同一VLAN的数据帧可以在交换机内部正常转发，不同VLAN的数据帧则被丢弃。",
        indent=True)

    # ---------- 题目2 ----------
    add_heading_styled(doc, "题目2：多交换机无VLAN连通性测试", level=2)

    add_heading_styled(doc, "1. 网络拓扑搭建", level=3)
    add_paragraph_styled(doc,
        "在Cisco Packet Tracer中搭建网络拓扑：2台2960交换机（Switch0和Switch1），4台PC（PC1、PC2、PC3、PC4）。"
        "Switch0的Fa0/1连接PC1，Fa0/2连接PC2，Fa0/24连接Switch1的Fa0/24。"
        "Switch1的Fa0/1连接PC3，Fa0/2连接PC4。",
        indent=True)
    add_screenshot_placeholder(doc, "多交换机无VLAN拓扑")

    add_heading_styled(doc, "2. 配置PC的IP地址", level=3)
    add_paragraph_styled(doc, "IP地址配置同题目1，所有PC配置相同的网段地址（192.168.0.0/24）。", indent=True)

    add_heading_styled(doc, "3. 连通性测试", level=3)
    add_paragraph_styled(doc,
        "不做任何VLAN配置，直接测试所有PC之间的连通性。由于所有端口默认属于VLAN1，"
        "两台交换机之间通过默认VLAN1进行数据转发，所有PC处于同一个广播域中。",
        indent=True)

    add_paragraph_styled(doc, "测试结果：", indent=True)
    add_paragraph_styled(doc, "（1）PC1 ping PC3：ping通", indent=True)
    add_paragraph_styled(doc, "（2）PC2 ping PC4：ping通", indent=True)
    add_paragraph_styled(doc, "（3）PC1 ping PC2：ping通", indent=True)
    add_paragraph_styled(doc, "（4）PC1 ping PC4：ping通", indent=True)
    add_screenshot_placeholder(doc, "多交换机无VLAN连通性测试结果")

    add_heading_styled(doc, "4. 结果分析", level=3)
    add_paragraph_styled(doc,
        "在不划分VLAN的情况下，所有PC之间都能ping通。这是因为所有交换机端口默认属于VLAN1，"
        "两台交换机之间的链路也默认通过VLAN1进行数据转发，所有PC处于同一个广播域中，因此可以互相通信。",
        indent=True)

    # ---------- 题目3 ----------
    add_heading_styled(doc, "题目3：多交换机VLAN划分（含Trunk配置）", level=2)

    add_heading_styled(doc, "1. 网络拓扑搭建", level=3)
    add_paragraph_styled(doc,
        "在题目2的基础上，进行VLAN划分。保持原有的网络拓扑不变，2台2960交换机通过Fa0/24端口互联，"
        "4台PC的连接方式不变。",
        indent=True)
    add_screenshot_placeholder(doc, "多交换机VLAN拓扑")

    add_heading_styled(doc, "2. 规划VLAN分配", level=3)
    add_paragraph_styled(doc, "按照下表进行VLAN分配：", indent=True)

    table2 = doc.add_table(rows=5, cols=4)
    table2.style = 'Table Grid'
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers2 = ["设备", "连接交换机", "端口", "所属VLAN"]
    for i, h in enumerate(headers2):
        set_cell_text(table2.rows[0].cells[i], h, bold=True)
    data2 = [
        ("PC1", "Switch0", "Fa0/1", "VLAN10"),
        ("PC2", "Switch0", "Fa0/2", "VLAN20"),
        ("PC3", "Switch1", "Fa0/1", "VLAN10"),
        ("PC4", "Switch1", "Fa0/2", "VLAN20"),
    ]
    for r, row_data in enumerate(data2, 1):
        for c, val in enumerate(row_data):
            set_cell_text(table2.rows[r].cells[c], val)

    add_heading_styled(doc, "3. 配置Switch0", level=3)
    add_paragraph_styled(doc, "在Switch0上创建VLAN，分配端口，并配置Trunk口：", indent=True)

    cmd_switch0 = """Switch0>enable
Switch0#configure terminal
Switch0(config)#vlan 10
Switch0(config-vlan)#name VLAN10
Switch0(config-vlan)#exit
Switch0(config)#vlan 20
Switch0(config-vlan)#name VLAN20
Switch0(config-vlan)#exit
Switch0(config)#interface FastEthernet0/1
Switch0(config-if)#switchport mode access
Switch0(config-if)#switchport access vlan 10
Switch0(config-if)#exit
Switch0(config)#interface FastEthernet0/2
Switch0(config-if)#switchport mode access
Switch0(config-if)#switchport access vlan 20
Switch0(config-if)#exit
Switch0(config)#interface FastEthernet0/24
Switch0(config-if)#switchport mode trunk
Switch0(config-if)#switchport trunk allowed vlan 10,20
Switch0(config-if)#exit
Switch0(config)#end
Switch0#write memory"""

    add_code_block(doc, cmd_switch0)

    add_heading_styled(doc, "4. 配置Switch1", level=3)
    add_paragraph_styled(doc, "在Switch1上创建VLAN，分配端口，并配置Trunk口：", indent=True)

    cmd_switch1 = """Switch1>enable
Switch1#configure terminal
Switch1(config)#vlan 10
Switch1(config-vlan)#name VLAN10
Switch1(config-vlan)#exit
Switch1(config)#vlan 20
Switch1(config-vlan)#name VLAN20
Switch1(config-vlan)#exit
Switch1(config)#interface FastEthernet0/1
Switch1(config-if)#switchport mode access
Switch1(config-if)#switchport access vlan 10
Switch1(config-if)#exit
Switch1(config)#interface FastEthernet0/2
Switch1(config-if)#switchport mode access
Switch1(config-if)#switchport access vlan 20
Switch1(config-if)#exit
Switch1(config)#interface FastEthernet0/24
Switch1(config-if)#switchport mode trunk
Switch1(config-if)#switchport trunk allowed vlan 10,20
Switch1(config-if)#exit
Switch1(config)#end
Switch1#write memory"""

    add_code_block(doc, cmd_switch1)

    add_heading_styled(doc, "5. 查看配置结果", level=3)
    add_paragraph_styled(doc, "使用show vlan brief和show interfaces trunk命令查看配置结果：", indent=True)

    add_paragraph_styled(doc, "Switch0的VLAN信息：", bold=True)
    vlan_out0 = """Switch0#show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/3, Fa0/4, Fa0/5, ...
10   VLAN10                           active    Fa0/1
20   VLAN20                           active    Fa0/2"""
    add_code_block(doc, vlan_out0)

    add_paragraph_styled(doc, "Switch0的Trunk信息：", bold=True)
    trunk_out = """Switch0#show interfaces trunk

Port        Mode         Encapsulation  Status        Native vlan
Fa0/24      on           802.1q         trunking      1

Port        Vlans allowed on trunk
Fa0/24      10,20

Port        Vlans allowed and active in management domain
Fa0/24      10,20

Port        Vlans in spanning tree forwarding state and not pruned
Fa0/24      10,20"""
    add_code_block(doc, trunk_out)
    add_screenshot_placeholder(doc, "Switch0的VLAN和Trunk配置信息")

    add_paragraph_styled(doc, "Switch1的VLAN信息：", bold=True)
    vlan_out1 = """Switch1#show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/3, Fa0/4, Fa0/5, ...
10   VLAN10                           active    Fa0/1
20   VLAN20                           active    Fa0/2"""
    add_code_block(doc, vlan_out1)
    add_screenshot_placeholder(doc, "Switch1的VLAN和Trunk配置信息")

    add_heading_styled(doc, "6. Trunk的作用说明", level=3)
    add_paragraph_styled(doc,
        "Trunk端口可以承载多个VLAN的数据，使得不同交换机上相同VLAN的设备可以通信。"
        "在本实验中，Switch0和Switch1之间的Fa0/24端口配置为Trunk模式，并允许VLAN10和VLAN20的数据通过。"
        "当PC1（VLAN10）发送数据帧到PC3（VLAN10，连接在Switch1上）时，"
        "数据帧经过Switch0的Fa0/1端口进入Switch0，Switch0在转发数据帧到Fa0/24（Trunk端口）时，"
        "会在数据帧中添加VLAN标签（802.1Q封装），标识该数据帧属于VLAN10。"
        "Switch1从Fa0/24端口收到带标签的数据帧后，根据VLAN标签将数据帧转发到VLAN10的端口Fa0/1，从而到达PC3。",
        indent=True)

    add_heading_styled(doc, "7. 连通性测试", level=3)
    add_paragraph_styled(doc, "使用ping命令测试各PC之间的连通性：", indent=True)

    add_paragraph_styled(doc, "（1）PC1 ping PC3（同VLAN10，跨交换机）：", indent=True)
    add_paragraph_styled(doc, "结果：ping通。PC1和PC3都属于VLAN10，虽然连接在不同交换机上，但通过Trunk链路可以通信。", indent=True)
    add_screenshot_placeholder(doc, "PC1 ping PC3结果")

    add_paragraph_styled(doc, "（2）PC2 ping PC4（同VLAN20，跨交换机）：", indent=True)
    add_paragraph_styled(doc, "结果：ping通。PC2和PC4都属于VLAN20，通过Trunk链路可以通信。", indent=True)
    add_screenshot_placeholder(doc, "PC2 ping PC4结果")

    add_paragraph_styled(doc, "（3）PC1 ping PC2（不同VLAN）：", indent=True)
    add_paragraph_styled(doc, "结果：ping不通。PC1属于VLAN10，PC2属于VLAN20，不同VLAN之间无法直接通信。", indent=True)
    add_screenshot_placeholder(doc, "PC1 ping PC2结果")

    add_paragraph_styled(doc, "（4）PC1 ping PC4（不同VLAN）：", indent=True)
    add_paragraph_styled(doc, "结果：ping不通。PC1属于VLAN10，PC4属于VLAN20，不同VLAN之间无法直接通信。", indent=True)
    add_screenshot_placeholder(doc, "PC1 ping PC4结果")

    add_heading_styled(doc, "8. 结果分析", level=3)
    add_paragraph_styled(doc,
        "从测试结果可以看出，在多交换机环境下，通过配置Trunk端口，同一VLAN内不同交换机上的PC可以互相ping通"
        "（PC1与PC3、PC2与PC4），而不同VLAN之间的PC无法ping通（PC1与PC2、PC1与PC4）。"
        "这说明Trunk端口能够承载多个VLAN的数据，使得跨交换机的同VLAN通信成为可能。"
        "同时，VLAN的隔离特性在多交换机环境下同样有效。",
        indent=True)

    # ========== 五、实验结果与分析 ==========
    add_heading_styled(doc, "五、实验结果与分析", level=1)

    add_heading_styled(doc, "1. 实验结果汇总", level=2)
    add_paragraph_styled(doc, "三个实验的测试结果对比如下表所示：", indent=True)

    table3 = doc.add_table(rows=6, cols=4)
    table3.style = 'Table Grid'
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    h3 = ["测试项目", "无VLAN（多交换机）", "有VLAN（单交换机）", "有VLAN（多交换机+Trunk）"]
    for i, h in enumerate(h3):
        set_cell_text(table3.rows[0].cells[i], h, bold=True)
    results = [
        ("PC1-PC3（同VLAN）", "通", "通", "通"),
        ("PC2-PC4（同VLAN）", "通", "通", "通"),
        ("PC1-PC2（不同VLAN）", "通", "不通", "不通"),
        ("PC1-PC4（不同VLAN）", "通", "不通", "不通"),
        ("PC2-PC3（不同VLAN）", "通", "不通", "不通"),
    ]
    for r, (test, v1, v2, v3) in enumerate(results, 1):
        set_cell_text(table3.rows[r].cells[0], test)
        set_cell_text(table3.rows[r].cells[1], v1)
        set_cell_text(table3.rows[r].cells[2], v2)
        set_cell_text(table3.rows[r].cells[3], v3)

    add_heading_styled(doc, "2. 结果分析", level=2)
    add_paragraph_styled(doc,
        "（1）在不划分VLAN的情况下，所有PC处于同一个广播域中，可以互相通信。这是交换机的默认行为，"
        "所有端口都属于VLAN1。",
        indent=True)
    add_paragraph_styled(doc,
        "（2）在单交换机划分VLAN后，同一VLAN内的PC可以通信，不同VLAN之间的PC无法通信。"
        "这说明VLAN有效地隔离了广播域，不同VLAN之间的数据帧被交换机丢弃。",
        indent=True)
    add_paragraph_styled(doc,
        "（3）在多交换机环境下，通过配置Trunk端口，同一VLAN内不同交换机上的PC可以通信。"
        "Trunk端口使用802.1Q协议在数据帧中添加VLAN标签，使得交换机能够识别数据帧所属的VLAN，"
        "从而实现跨交换机的VLAN通信。",
        indent=True)
    add_paragraph_styled(doc,
        "（4）VLAN的核心作用是隔离广播域。广播报文只在同一VLAN内转发，不会扩散到其他VLAN，"
        "这不仅减少了网络中的广播流量，还提高了网络的安全性。"
        "在实际网络中，通常会根据部门、功能等因素将网络划分为多个VLAN。",
        indent=True)

    # ========== 六、思考题 ==========
    add_heading_styled(doc, "六、思考题", level=1)

    add_heading_styled(doc, "思考题1：为什么同VLAN不同交换机的PC可以ping通？", level=2)
    add_paragraph_styled(doc,
        "答：因为交换机之间的链路配置为Trunk模式，Trunk端口可以承载多个VLAN的数据。"
        "当PC1发送数据帧到Switch0时，数据帧从Fa0/1（Access端口，属于VLAN10）进入Switch0，"
        "Switch0查找MAC地址表后发现目的地址在Fa0/24端口方向，于是将数据帧从Fa0/24（Trunk端口）转发。"
        "在转发过程中，Switch0会在数据帧中添加VLAN标签（802.1Q封装），标识该数据帧属于VLAN10。"
        "Switch1从Fa0/24端口收到带标签的数据帧后，读取VLAN标签发现该数据帧属于VLAN10，"
        "于是将数据帧转发到VLAN10的端口Fa0/1，从而到达PC3。",
        indent=True)
    add_screenshot_placeholder(doc, "Trunk数据帧转发示意图")

    add_heading_styled(doc, "思考题2：如果不配置Trunk，跨交换机的同VLAN PC能否通信？", level=2)
    add_paragraph_styled(doc,
        "答：不能。如果不配置Trunk，交换机之间的链路默认是Access模式，只属于一个VLAN（默认VLAN1）。"
        "Access端口在转发数据时会去掉VLAN标签，只转发属于该端口所属VLAN的数据帧。"
        "因此，当PC1（VLAN10）发送数据帧到Switch0的Fa0/1端口后，Switch0需要将数据帧从Fa0/24端口转发给Switch1，"
        "但Fa0/24是Access端口且属于VLAN1，无法转发VLAN10的数据帧。"
        "即使Switch0将数据帧从Fa0/24转发出去，Switch1收到数据帧后也会将其归入VLAN1，"
        "而PC3连接的Fa0/1端口属于VLAN10，因此数据帧无法到达PC3。",
        indent=True)

    # 保存文档
    output_path = r"D:\计网实验\实验三-VLAN划分\实验三报告.docx"
    doc.save(output_path)
    print(f"报告已生成: {output_path}")


if __name__ == "__main__":
    create_report()
