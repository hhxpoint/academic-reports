#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成学术报告的通用模板脚本
按照GB/T 7714参考文献格式，生成符合要求的大作业报告
"""

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os


def set_cell_border(cell, **kwargs):
    """设置单元格边框"""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            element = OxmlElement(f'w:{edge}')
            for key in edge_data:
                element.set(qn(f'w:{key}'), str(edge_data[key]))
            tcBorders.append(element)
    tcPr.append(tcBorders)


def create_report(title, subtitle, course_name, abstract, keywords, sections, conclusion, references, output_filename):
    """
    创建完整的大作业报告

    参数:
        title: 报告主标题
        subtitle: 副标题(综述报告)
        course_name: 课程名称
        abstract: 摘要内容
        keywords: 关键词列表
        sections: 正文章节列表，格式为 [(标题, 内容), ...]
        conclusion: 结论内容
        references: 参考文献列表
        output_filename: 输出文件名
    """
    doc = Document()

    # ===== 设置默认字体 =====
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # 设置页边距
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(3.17)
        section.right_margin = Cm(3.17)

    # ===== 封面 =====
    # 空行
    for _ in range(3):
        doc.add_paragraph()

    # 课程名称
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(course_name)
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    doc.add_paragraph()

    # 报告标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    doc.add_paragraph()

    # 副标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(subtitle)
    run.font.size = Pt(16)
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    for _ in range(3):
        doc.add_paragraph()

    # 信息表格
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    info_items = [
        ('姓    名：', ''),
        ('学    号：', ''),
        ('班    级：', ''),
        ('指导教师：', ''),
    ]

    for i, (label, value) in enumerate(info_items):
        cell_label = table.cell(i, 0)
        cell_value = table.cell(i, 1)

        p_label = cell_label.paragraphs[0]
        p_label.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run_label = p_label.add_run(label)
        run_label.font.size = Pt(14)
        run_label.font.name = 'Times New Roman'
        run_label.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

        p_value = cell_value.paragraphs[0]
        p_value.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run_value = p_value.add_run(value)
        run_value.font.size = Pt(14)
        run_value.font.name = 'Times New Roman'
        run_value.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        # 添加下划线
        run_value.underline = True

    for _ in range(3):
        doc.add_paragraph()

    # 日期
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('二〇二六年五月')
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # ===== 分页 =====
    doc.add_page_break()

    # ===== 摘要 =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('摘  要')
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    # 摘要内容
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0.74)  # 首行缩进2字符
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(abstract)
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # 关键词
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run('关键词：')
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    run = p.add_run('；'.join(keywords))
    run.font.size = Pt(12)
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    doc.add_page_break()

    # ===== 目录占位 =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('目  录')
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    doc.add_paragraph('(请在Word中插入自动目录)')
    doc.add_page_break()

    # ===== 正文 =====
    for i, (section_title, section_content) in enumerate(sections, 1):
        # 章节标题
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(f'{i}  {section_title}')
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.name = 'Times New Roman'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

        # 正文内容 - 按段落分割
        paragraphs = section_content.strip().split('\n')
        for para_text in paragraphs:
            para_text = para_text.strip()
            if not para_text:
                continue

            # 检查是否是子标题
            if para_text.startswith('##'):
                # 三级标题
                sub_title = para_text.lstrip('#').strip()
                p = doc.add_paragraph()
                run = p.add_run(sub_title)
                run.font.size = Pt(14)
                run.font.bold = True
                run.font.name = 'Times New Roman'
                run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
            elif para_text.startswith('#'):
                # 二级标题
                sub_title = para_text.lstrip('#').strip()
                p = doc.add_paragraph()
                run = p.add_run(f'{i}.{sub_title}')
                run.font.size = Pt(14)
                run.font.bold = True
                run.font.name = 'Times New Roman'
                run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
            else:
                p = doc.add_paragraph()
                p.paragraph_format.first_line_indent = Cm(0.74)
                p.paragraph_format.line_spacing = 1.5
                run = p.add_run(para_text)
                run.font.size = Pt(12)
                run.font.name = 'Times New Roman'
                run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

        # 在主要章节之间添加一些空行
        doc.add_paragraph()

    # ===== 结论 =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(f'{len(sections) + 1}  结论')
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    paragraphs = conclusion.strip().split('\n')
    for para_text in paragraphs:
        para_text = para_text.strip()
        if not para_text:
            continue
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0.74)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(para_text)
        run.font.size = Pt(12)
        run.font.name = 'Times New Roman'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    doc.add_page_break()

    # ===== 参考文献 =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('参考文献')
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    for i, ref in enumerate(references, 1):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.first_line_indent = Cm(-0.74)
        p.paragraph_format.left_indent = Cm(0.74)
        run = p.add_run(f'[{i}] {ref}')
        run.font.size = Pt(10.5)  # 五号字
        run.font.name = 'Times New Roman'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # 保存文件
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)
    doc.save(filepath)
    print(f'报告已保存: {filepath}')
    return filepath


if __name__ == '__main__':
    print('报告生成工具已就绪。请在主脚本中调用 create_report() 函数。')
