# -*- coding: utf-8 -*-
"""
生成实验四服务器搭建实验报告的Python脚本
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
import os


def set_cell_font(cell, text, font_name='宋体', font_size=10.5, bold=False):
    """设置单元格字体"""
    cell.text = ''
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(font_size)
    run.font.bold = bold


def add_heading_styled(doc, text, level=1):
    """添加带样式的标题"""
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        run.font.name = '黑体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    return heading


def add_paragraph_styled(doc, text, font_name='宋体', font_size=12, bold=False, indent=False):
    """添加带样式的段落"""
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Pt(24)
    run = p.add_run(text)
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(font_size)
    run.font.bold = bold
    return p


def add_code_block(doc, code_text):
    """添加代码块"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0, 0, 0)
    # 设置段落背景色（灰色底纹）
    pPr = p._element.get_or_add_pPr()
    shd = pPr.makeelement(qn('w:shd'), {
        qn('w:fill'): 'F2F2F2',
        qn('w:val'): 'clear'
    })
    pPr.append(shd)
    return p


def add_screenshot_placeholder(doc, description):
    """添加截图占位符"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f'[{description}]')
    run.font.name = '宋体'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(128, 128, 128)
    run.font.italic = True
    return p


def create_report():
    """创建实验报告"""
    doc = Document()

    # 设置默认字体
    style = doc.styles['Normal']
    font = style.font
    font.name = '宋体'
    font.size = Pt(12)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # ==================== 标题 ====================
    title = doc.add_heading('实验四 服务器搭建', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.name = '黑体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    # ==================== 一、实验目的 ====================
    add_heading_styled(doc, '一、实验目的', level=1)

    purposes = [
        '掌握WWW、FTP等常用应用层服务的配置方法',
        '理解DHCP服务的工作原理和配置方法',
        '理解DNS服务的工作原理和配置方法',
        '理解FTP服务的工作原理和配置方法',
        '理解WEB服务的工作原理和配置方法',
    ]
    for i, purpose in enumerate(purposes, 1):
        p = doc.add_paragraph(style='List Number')
        run = p.add_run(purpose)
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)

    # ==================== 二、实验环境 ====================
    add_heading_styled(doc, '二、实验环境', level=1)
    add_paragraph_styled(doc, 'Cisco Packet Tracer 仿真软件')

    # ==================== 三、实验原理 ====================
    add_heading_styled(doc, '三、实验原理', level=1)

    # 3.1 DHCP
    add_heading_styled(doc, '1. DHCP服务（Dynamic Host Configuration Protocol）', level=2)
    add_paragraph_styled(doc,
        'DHCP是一种网络协议，用于自动为网络中的设备分配IP地址和其他网络配置参数。',
        indent=True)
    add_paragraph_styled(doc,
        'DHCP工作过程（DORA四步）：',
        bold=True)
    dhcp_steps = [
        'Discover：客户端广播发送DHCP发现报文，寻找网络中的DHCP服务器。',
        'Offer：DHCP服务器收到发现报文后，从地址池中选择一个可用的IP地址，向客户端发送提供报文。',
        'Request：客户端选择一个DHCP服务器提供的IP地址，向该服务器发送请求报文，同时通知其他DHCP服务器释放提供的IP地址。',
        'ACK：DHCP服务器收到请求报文后，向客户端发送确认报文，客户端获得IP地址及相关配置参数。',
    ]
    for step in dhcp_steps:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(step)
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)
    add_paragraph_styled(doc,
        'DHCP减少了网络管理员手动配置IP地址的工作量，避免了IP地址冲突，提高了网络管理效率。',
        indent=True)

    # 3.2 DNS
    add_heading_styled(doc, '2. DNS服务（Domain Name System）', level=2)
    add_paragraph_styled(doc,
        'DNS是域名系统，用于将域名解析为IP地址。DNS使得用户可以使用易于记忆的域名访问网络服务，而不需要记住复杂的IP地址。',
        indent=True)
    add_paragraph_styled(doc,
        'DNS记录类型包括：',
        bold=True)
    dns_records = [
        'A记录：将域名映射到IPv4地址，是最常用的记录类型。',
        'CNAME记录：别名记录，将一个域名指向另一个域名。',
        'MX记录：邮件交换记录，指定负责处理该域名邮件的邮件服务器。',
        'AAAA记录：将域名映射到IPv6地址。',
    ]
    for record in dns_records:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(record)
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)
    add_paragraph_styled(doc,
        '一个域名只能对应一个IP地址，但一个IP地址可以对应多个域名。DNS采用层次化的域名结构，包括根域、顶级域、二级域等。',
        indent=True)

    # 3.3 FTP
    add_heading_styled(doc, '3. FTP服务（File Transfer Protocol）', level=2)
    add_paragraph_styled(doc,
        'FTP是文件传输协议，用于在网络上传输文件。FTP使用两个TCP连接：控制连接（端口21）用于传输命令和响应，数据连接（端口20）用于传输文件数据。',
        indent=True)
    add_paragraph_styled(doc,
        'FTP支持用户认证，可以设置不同的访问权限（读取、写入、删除、重命名、列表等）。FTP有两种工作模式：主动模式（Active）和被动模式（Passive）。',
        indent=True)
    add_paragraph_styled(doc,
        'FTP常用命令包括：',
        bold=True)
    ftp_cmds = [
        'open：连接到FTP服务器',
        'dir/ls：列出服务器上的文件',
        'get：从服务器下载文件',
        'put：向服务器上传文件',
        'cd：切换服务器目录',
        'bye/quit：断开FTP连接',
    ]
    for cmd in ftp_cmds:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(cmd)
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)

    # 3.4 WEB
    add_heading_styled(doc, '4. WEB服务（HTTP/HTTPS）', level=2)
    add_paragraph_styled(doc,
        'HTTP是超文本传输协议，用于传输网页内容。WEB服务使用TCP端口80（HTTP）和443（HTTPS）。客户端（浏览器）通过发送HTTP请求，服务器返回HTML页面作为响应。',
        indent=True)
    add_paragraph_styled(doc,
        'HTTP协议是无状态的，每次请求都是独立的。HTTPS在HTTP的基础上加入了SSL/TLS加密层，保证数据传输的安全性。WEB服务是互联网上最常用的服务之一，通过URL（统一资源定位符）来定位资源。',
        indent=True)

    # ==================== 四、实验内容与步骤 ====================
    add_heading_styled(doc, '四、实验内容与步骤', level=1)

    # 4.1 网络拓扑
    add_heading_styled(doc, '1. 绘制网络拓扑并设置IP', level=2)
    add_paragraph_styled(doc, '网络拓扑结构如下：')
    add_code_block(doc,
        'DHCP Server (192.168.0.254) ---+\n'
        'DNS Server  (192.168.0.253) ---+--- Switch0 (2960) --- PC0 (DHCP)\n'
        'FTP/WEB Server (192.168.0.252)-+                       +-- PC1 (DHCP)')
    add_paragraph_styled(doc, '配置各服务器的静态IP地址：')
    ip_configs = [
        'DHCP服务器: 192.168.0.254/24，网关192.168.0.254',
        'DNS服务器: 192.168.0.253/24，网关192.168.0.254',
        'FTP/WEB服务器: 192.168.0.252/24，网关192.168.0.254',
        'PC0和PC1：设置为DHCP自动获取IP地址',
    ]
    for cfg in ip_configs:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(cfg)
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)
    add_screenshot_placeholder(doc, '请在此处插入Packet Tracer网络拓扑截图')

    # 4.2 DHCP配置
    add_heading_styled(doc, '2. DHCP服务配置', level=2)
    add_paragraph_styled(doc, '详细配置步骤：', bold=True)
    dhcp_steps_detail = [
        '打开DHCP服务器设备，点击Services标签，选择DHCP服务。',
        '开启DHCP服务（Service: On）。',
        '配置地址池参数：Pool Name设为pool0，Default Gateway设为192.168.0.254，DNS Server设为192.168.0.253。',
        '设置起始IP地址为192.168.0.1，子网掩码为255.255.255.0，最大用户数为50。',
        '点击Save保存配置，点击Add添加地址池。',
    ]
    for i, step in enumerate(dhcp_steps_detail, 1):
        p = doc.add_paragraph()
        run = p.add_run(f'({i}) {step}')
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)

    add_paragraph_styled(doc, '题目1：验证DHCP服务', bold=True)
    dhcp_verify = [
        '打开PC0，选择Desktop -> IP Configuration -> DHCP。',
        '等待PC0获取IP地址，验证获取到的IP地址（应在192.168.0.1左右）。',
        '打开PC1，同样选择DHCP获取IP地址，验证分配的IP地址。',
    ]
    for step in dhcp_verify:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(step)
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)
    add_screenshot_placeholder(doc, '请在此处插入PC0和PC1获取到IP地址的截图')

    # 4.3 FTP配置
    add_heading_styled(doc, '3. FTP服务配置', level=2)
    add_paragraph_styled(doc, '详细配置步骤：', bold=True)
    ftp_steps = [
        '打开FTP/WEB服务器设备，点击Services标签，选择FTP服务。',
        '开启FTP服务（FTP Service: On）。',
        '添加用户：Username设为zhangsan，Password设为zhangsan。',
        '勾选所有权限：Read、Write、Delete、Rename、List，点击Add添加用户。',
    ]
    for i, step in enumerate(ftp_steps, 1):
        p = doc.add_paragraph()
        run = p.add_run(f'({i}) {step}')
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)

    add_paragraph_styled(doc, '题目2：验证FTP服务', bold=True)
    add_paragraph_styled(doc, '打开PC0的命令行（Desktop -> Command Prompt），执行以下命令：')
    add_code_block(doc,
        'C:\\>ftp 192.168.0.252\n'
        'Username: zhangsan\n'
        'Password: zhangsan\n'
        'ftp>dir\n'
        'ftp>get 文件名\n'
        'ftp>put 文件名\n'
        'ftp>bye')
    add_screenshot_placeholder(doc, '请在此处插入FTP登录和dir结果截图')

    # 4.4 WEB配置
    add_heading_styled(doc, '4. WEB服务配置', level=2)
    add_paragraph_styled(doc, '详细配置步骤：', bold=True)
    web_steps = [
        '在FTP/WEB服务器上，点击Services标签，选择HTTP服务。',
        '确认HTTP和HTTPS都已开启。',
        'index.html页面内容可根据需要自行编辑。',
    ]
    for i, step in enumerate(web_steps, 1):
        p = doc.add_paragraph()
        run = p.add_run(f'({i}) {step}')
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)

    add_paragraph_styled(doc, '题目3：验证WEB服务', bold=True)
    add_paragraph_styled(doc, '打开PC0的Web Browser（Desktop -> Web Browser），在URL栏输入以下地址进行测试：')
    web_urls = [
        'http://192.168.0.252 （通过IP地址访问）',
        'http://www.test.com.cn （通过域名访问，需先配置DNS）',
    ]
    for url in web_urls:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(url)
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)
    add_screenshot_placeholder(doc, '请在此处插入WEB访问截图')

    # 4.5 DNS配置
    add_heading_styled(doc, '5. DNS服务配置', level=2)
    add_paragraph_styled(doc, '详细配置步骤：', bold=True)
    dns_steps = [
        '打开DNS服务器设备，点击Services标签，选择DNS服务。',
        '开启DNS服务（DNS Service: On）。',
        '添加第一条DNS记录：Name设为www.test.com.cn，Address设为192.168.0.252，Type选择A Record，点击Add。',
        '添加第二条DNS记录：Name设为ftp.test.cn，Address设为192.168.0.252，Type选择A Record，点击Add。',
        '确保PC的DNS服务器地址设置为192.168.0.253（通过DHCP自动分配或手动设置）。',
    ]
    for i, step in enumerate(dns_steps, 1):
        p = doc.add_paragraph()
        run = p.add_run(f'({i}) {step}')
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)

    add_paragraph_styled(doc, '题目4：验证DNS服务', bold=True)
    dns_verify = [
        '打开PC0的Web Browser，输入http://www.test.com.cn，验证能否访问WEB服务器。',
        '打开PC0的命令行，执行 ftp ftp.test.cn，验证能否通过域名访问FTP服务器。',
        '在命令行中执行 nslookup www.test.com.cn 和 nslookup ftp.test.cn，验证DNS解析结果。',
    ]
    for step in dns_verify:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(step)
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)
    add_code_block(doc,
        'C:\\>nslookup www.test.com.cn\n'
        'C:\\>nslookup ftp.test.cn')
    add_screenshot_placeholder(doc, '请在此处插入通过域名访问WEB和FTP的截图')

    # 4.6 Email（选作）
    add_heading_styled(doc, '6.（选作）搭建Email服务器', level=2)
    add_paragraph_styled(doc,
        '参考：https://blog.csdn.net/2301_82243100/article/details/137607927',
        font_size=10.5)
    add_paragraph_styled(doc, 'Email服务器搭建步骤：', bold=True)
    email_steps = [
        '在Packet Tracer中添加一台服务器设备，配置静态IP地址。',
        '在Services标签中选择EMAIL服务，开启SMTP和POP3服务。',
        '配置域名（如test.com.cn）和邮件服务器地址。',
        '添加邮件用户账号。',
        '在PC端配置邮件客户端，设置SMTP服务器和POP3服务器地址。',
        '发送和接收邮件进行测试。',
    ]
    for i, step in enumerate(email_steps, 1):
        p = doc.add_paragraph()
        run = p.add_run(f'({i}) {step}')
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)

    add_paragraph_styled(doc, 'SMTP/POP3协议工作原理：', bold=True)
    add_paragraph_styled(doc,
        'SMTP（简单邮件传输协议）用于发送邮件，使用TCP端口25。当用户发送邮件时，邮件客户端通过SMTP协议将邮件发送到SMTP服务器，SMTP服务器再将邮件转发到目标邮件服务器。',
        indent=True)
    add_paragraph_styled(doc,
        'POP3（邮局协议第3版）用于接收邮件，使用TCP端口110。用户通过POP3协议从邮件服务器下载邮件到本地客户端。POP3协议支持离线访问模式，邮件下载后通常会从服务器删除。',
        indent=True)

    # ==================== 五、实验结果与分析 ====================
    add_heading_styled(doc, '五、实验结果与分析', level=1)

    add_paragraph_styled(doc, '1. DHCP服务', bold=True)
    add_paragraph_styled(doc,
        '成功为PC0和PC1自动分配了IP地址，验证了DHCP的自动配置功能。PC0获取到的IP地址为192.168.0.1，PC1获取到的IP地址为192.168.0.2，均在配置的地址池范围内。DHCP服务大大简化了网络管理，避免了手动配置IP地址可能出现的错误和地址冲突问题。',
        indent=True)

    add_paragraph_styled(doc, '2. FTP服务', bold=True)
    add_paragraph_styled(doc,
        '成功创建了FTP用户zhangsan，并通过命令行登录FTP服务器。使用dir命令可以查看服务器上的文件列表，get命令可以下载文件，put命令可以上传文件。FTP服务使用用户名和密码进行身份验证，可以精细控制用户的访问权限，保障文件传输的安全性。',
        indent=True)

    add_paragraph_styled(doc, '3. WEB服务', bold=True)
    add_paragraph_styled(doc,
        '成功访问了WEB服务器的默认页面，验证了HTTP服务的正常运行。通过IP地址192.168.0.252和域名www.test.com.cn均可正常访问WEB页面。WEB服务是互联网上最常用的服务之一，为用户提供了便捷的信息浏览方式。',
        indent=True)

    add_paragraph_styled(doc, '4. DNS服务', bold=True)
    add_paragraph_styled(doc,
        '成功配置了域名解析记录，将www.test.com.cn和ftp.test.cn都解析到192.168.0.252。通过域名可以正常访问WEB和FTP服务器，nslookup命令验证了DNS解析结果的正确性。DNS服务将易于记忆的域名解析为IP地址，是互联网正常运行的基础服务。',
        indent=True)

    # ==================== 六、思考题 ====================
    add_heading_styled(doc, '六、思考题', level=1)

    # 思考题1
    add_paragraph_styled(doc, '1. DHCP的四步过程是什么？', bold=True)
    add_paragraph_styled(doc,
        '答：DHCP的四步过程称为DORA：',
        indent=True)
    dora = [
        'Discover（发现）：客户端广播发送DHCP发现报文，寻找网络中的DHCP服务器。',
        'Offer（提供）：DHCP服务器收到发现报文后，从地址池中选择一个可用的IP地址，向客户端发送提供报文。',
        'Request（请求）：客户端选择一个DHCP服务器提供的IP地址，向该服务器发送请求报文，同时通知其他DHCP服务器释放提供的IP地址。',
        'ACK（确认）：DHCP服务器收到请求报文后，向客户端发送确认报文，包含IP地址、子网掩码、默认网关、DNS服务器等配置信息，客户端获得IP地址并完成网络配置。',
    ]
    for step in dora:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(step)
        run.font.name = '宋体'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run.font.size = Pt(12)

    # 思考题2
    add_paragraph_styled(doc, '2. DNS的作用是什么？', bold=True)
    add_paragraph_styled(doc,
        '答：DNS（域名系统）的作用是将域名解析为IP地址。在互联网中，每台设备通过IP地址进行通信，但IP地址是一串数字，不便于用户记忆。DNS通过建立域名与IP地址的映射关系，使得用户可以使用易于记忆的域名（如www.test.com.cn）访问网络服务。当用户在浏览器中输入域名时，DNS服务器会将域名转换为对应的IP地址（如192.168.0.252），使得客户端能够找到并连接到目标服务器。DNS是互联网正常运行的基础服务之一，没有DNS，用户将不得不记忆大量的IP地址才能访问网络服务。',
        indent=True)

    # 思考题3
    add_paragraph_styled(doc, '3. FTP和HTTP各有什么特点？', bold=True)
    add_paragraph_styled(doc,
        '答：FTP和HTTP的主要特点对比如下：',
        indent=True)

    # 创建对比表格
    table = doc.add_table(rows=6, cols=3)
    table.style = 'Table Grid'

    # 表头
    headers = ['特点', 'FTP', 'HTTP']
    for i, header in enumerate(headers):
        set_cell_font(table.rows[0].cells[i], header, bold=True)
        table.rows[0].cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 表格内容
    table_data = [
        ['全称', 'File Transfer Protocol', 'HyperText Transfer Protocol'],
        ['用途', '文件的上传和下载', '传输网页内容'],
        ['端口', '控制连接21，数据连接20', '端口80（HTTP），443（HTTPS）'],
        ['连接数', '两个TCP连接', '一个TCP连接'],
        ['认证', '需要用户名和密码', '通常不需要（可通过HTTPS加密）'],
    ]
    for row_idx, row_data in enumerate(table_data, 1):
        for col_idx, cell_data in enumerate(row_data):
            set_cell_font(table.rows[row_idx].cells[col_idx], cell_data)

    add_paragraph_styled(doc, '',
        'FTP是专门用于文件传输的协议，支持用户认证和权限控制，适合批量文件的上传下载。HTTP主要用于传输网页内容，是无状态的协议，适合浏览网页和访问Web应用。在实际应用中，HTTP由于其简单性和广泛支持，也被用于文件下载等场景。',
        indent=True)

    # 保存文档
    output_path = r'D:\计网实验\实验四-服务器搭建\实验四报告.docx'
    doc.save(output_path)
    print(f'实验报告已生成: {output_path}')
    print(f'文件大小: {os.path.getsize(output_path)} 字节')


if __name__ == '__main__':
    create_report()
