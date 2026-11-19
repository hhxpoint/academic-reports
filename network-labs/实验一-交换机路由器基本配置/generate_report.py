from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# 标题
doc.add_heading('实验一 交换机路由器的基本配置', level=0)

# 实验目的
doc.add_heading('一、实验目的', level=1)
doc.add_paragraph('1. 掌握以太网交换机和路由器的概念；')
doc.add_paragraph('2. 完成交换机和路由器的基本配置；')
doc.add_paragraph('3. 掌握交换机和路由器各种视图下的常用命令。')

# 实验环境
doc.add_heading('二、实验环境', level=1)
doc.add_paragraph('Cisco Packet Tracer 仿真软件')

# 实验原理
doc.add_heading('三、实验原理', level=1)
doc.add_paragraph('1. 交换机工作原理：')
doc.add_paragraph('以太网交换机工作在数据链路层，基于MAC地址进行数据帧的转发。交换机通过自学习算法建立MAC地址表，当收到数据帧时，检查源MAC地址并记录到MAC表中，然后根据目的MAC地址查找MAC表进行转发。如果目的MAC地址不在表中，则向除接收端口外的所有端口广播（泛洪）。')
doc.add_paragraph('2. 路由器工作原理：')
doc.add_paragraph('路由器工作在网络层，基于IP地址进行数据包的转发。路由器通过路由表决定数据包的转发路径，支持静态路由和动态路由协议。路由器的主要功能包括：连接不同网络、路径选择、数据包转发。')
doc.add_paragraph('3. 交换机与路由器的区别：')

# 添加对比表格
table = doc.add_table(rows=6, cols=3)
table.style = 'Table Grid'
headers = ['比较项目', '交换机', '路由器']
for i, h in enumerate(headers):
    table.rows[0].cells[i].text = h
data = [
    ['工作层次', '数据链路层（二层）', '网络层（三层）'],
    ['转发依据', 'MAC地址', 'IP地址'],
    ['主要功能', '局域网内数据帧转发', '不同网络间数据包路由'],
    ['广播处理', '转发广播帧', '隔离广播域'],
    ['端口数量', '较多（24/48口）', '较少（2-8口）'],
]
for i, row_data in enumerate(data):
    for j, cell_data in enumerate(row_data):
        table.rows[i+1].cells[j].text = cell_data

# 实验内容与步骤
doc.add_heading('四、实验内容与步骤', level=1)

doc.add_heading('（一）交换机基本配置', level=2)
doc.add_paragraph('1. 搭建网络拓扑')
doc.add_paragraph('在Cisco Packet Tracer中，选择1台2960交换机和3台PC机。使用直通线将PC机连接到交换机的FastEthernet端口。')
doc.add_paragraph('拓扑结构：')
doc.add_paragraph('  Switch0 (2960)')
doc.add_paragraph('  ├── Fa0/1 ── PC1 (192.168.1.1/24)')
doc.add_paragraph('  ├── Fa0/2 ── PC2 (192.168.1.2/24)')
doc.add_paragraph('  └── Fa0/3 ── PC3 (192.168.1.3/24)')
doc.add_paragraph('')
doc.add_paragraph('2. 配置PC机IP地址')
doc.add_paragraph('PC1: IP=192.168.1.1, 子网掩码=255.255.255.0')
doc.add_paragraph('PC2: IP=192.168.1.2, 子网掩码=255.255.255.0')
doc.add_paragraph('PC3: IP=192.168.1.3, 子网掩码=255.255.255.0')
doc.add_paragraph('')
doc.add_paragraph('3. 查看交换机端口信息')
doc.add_paragraph('通过Console口连接交换机，进入命令行模式，执行以下命令：')
doc.add_paragraph('Switch>enable')
doc.add_paragraph('Switch#show interfaces')
doc.add_paragraph('Switch#show ip interface brief')
doc.add_paragraph('')
doc.add_paragraph('4. 测试连通性')
doc.add_paragraph('在PC1的命令行中执行：')
doc.add_paragraph('C:\\>ping 192.168.1.2')
doc.add_paragraph('C:\\>ping 192.168.1.3')
doc.add_paragraph('')
doc.add_paragraph('5. 查看MAC地址表')
doc.add_paragraph('在交换机上执行：')
doc.add_paragraph('Switch#show mac-address-table')
doc.add_paragraph('')
doc.add_paragraph('6. 观察交换机自学习过程')
doc.add_paragraph('切换到仿真模式，使用PC1 ping PC2，观察ARP和ICMP数据包的转发过程。交换机首先收到PC1的数据帧，记录PC1的MAC地址到MAC表中，然后向其他端口泛洪。当PC2回复时，交换机记录PC2的MAC地址，之后就可以直接转发。')

doc.add_paragraph('')
doc.add_paragraph('[截图位置：请在此处插入Packet Tracer仿真截图]')
doc.add_paragraph('')

doc.add_heading('（二）路由器基本配置', level=2)
doc.add_paragraph('1. 搭建网络拓扑')
doc.add_paragraph('选择1台2811路由器和1台PC机。使用配置线连接PC的RS232口和路由器的Console口，使用直通线连接PC的FastEthernet口和路由器的FastEthernet口。')
doc.add_paragraph('')
doc.add_paragraph('2. 配置PC机')
doc.add_paragraph('PC0: IP=192.168.1.2, 子网掩码=255.255.255.0, 网关=192.168.1.1')
doc.add_paragraph('')
doc.add_paragraph('3. 通过Terminal配置路由器')
doc.add_paragraph('打开PC0的Desktop标签，点击Terminal图标，进入路由器命令行：')
doc.add_paragraph('Router>enable')
doc.add_paragraph('Router#configure terminal')
doc.add_paragraph('Router(config)#hostname Router0')
doc.add_paragraph('Router0(config)#interface FastEthernet0/0')
doc.add_paragraph('Router0(config-if)#ip address 192.168.1.1 255.255.255.0')
doc.add_paragraph('Router0(config-if)#no shutdown')
doc.add_paragraph('Router0(config-if)#exit')
doc.add_paragraph('')
doc.add_paragraph('4. 查看路由器配置')
doc.add_paragraph('Router0#show running-config')
doc.add_paragraph('Router0#show ip interface brief')
doc.add_paragraph('')
doc.add_paragraph('5. 测试连通性')
doc.add_paragraph('在PC0的命令行中执行：')
doc.add_paragraph('C:\\>ipconfig /all')
doc.add_paragraph('C:\\>ping 192.168.1.1')
doc.add_paragraph('')
doc.add_paragraph('6. 使用Telnet登录路由器')
doc.add_paragraph('Router0(config)#line vty 0 4')
doc.add_paragraph('Router0(config-line)#password cisco')
doc.add_paragraph('Router0(config-line)#login')
doc.add_paragraph('Router0(config-line)#exit')
doc.add_paragraph('Router0(config)#enable password cisco')
doc.add_paragraph('')
doc.add_paragraph('从PC0通过Telnet登录：')
doc.add_paragraph('C:\\>telnet 192.168.1.1')

doc.add_paragraph('')
doc.add_paragraph('[截图位置：请在此处插入路由器配置截图]')

# 实验结果与分析
doc.add_heading('五、实验结果与分析', level=1)
doc.add_paragraph('1. 交换机配置结果')
doc.add_paragraph('通过实验，成功配置了交换机并实现了三台PC机之间的互联互通。交换机通过自学习算法自动建立了MAC地址表，实现了基于MAC地址的数据帧转发。')
doc.add_paragraph('')
doc.add_paragraph('2. 路由器配置结果')
doc.add_paragraph('通过实验，成功配置了路由器的接口IP地址，并实现了PC机与路由器之间的连通。路由器工作在网络层，通过IP地址进行数据包的转发。')
doc.add_paragraph('')
doc.add_paragraph('3. 交换机与路由器工作原理对比')
doc.add_paragraph('交换机：工作在数据链路层，基于MAC地址转发数据帧，通过自学习算法建立MAC表，不能隔离广播域。')
doc.add_paragraph('路由器：工作在网络层，基于IP地址转发数据包，通过路由表决定转发路径，能够隔离广播域。')

# 思考题
doc.add_heading('六、思考题', level=1)
doc.add_paragraph('题目：搭建拓扑，PC1设置为192.168.1.3/24，PC0是否能ping通PC1？为什么？')
doc.add_paragraph('')
doc.add_paragraph('答：如果PC0和PC1连接在同一台交换机上，且都处于192.168.1.0/24网段，则PC0可以ping通PC1。因为交换机工作在数据链路层，通过MAC地址转发数据帧。PC0发送ARP请求获取PC1的MAC地址，交换机将ARP请求泛洪到所有端口（除接收端口），PC1收到后回复ARP应答，交换机学习到两台PC的MAC地址后，就可以直接转发数据帧。')
doc.add_paragraph('')
doc.add_paragraph('如果PC0连接在路由器的一个接口上，PC1连接在另一个不同网段的接口上，则需要正确配置路由才能ping通。')

doc.save('D:/计网实验/实验一-交换机路由器基本配置/实验一报告.docx')
print('报告已成功生成: D:/计网实验/实验一-交换机路由器基本配置/实验一报告.docx')
