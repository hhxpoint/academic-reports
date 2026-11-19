#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成学术报告的通用模板脚本 V2 - 增强版
支持表格、公式、图描述等丰富内容
"""

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os


def set_cell_shading(cell, color_hex):
    """设置单元格底色"""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color_hex)
    shading_elm.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_table_border(table):
    """设置表格边框"""
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        element = OxmlElement(f'w:{edge}')
        element.set(qn('w:val'), 'single')
        element.set(qn('w:sz'), '4')
        element.set(qn('w:space'), '0')
        element.set(qn('w:color'), '000000')
        borders.append(element)
    tblPr.append(borders)


def add_formatted_paragraph(doc, text, font_size=12, bold=False, align='left',
                            first_indent=True, line_spacing=1.5, font_name='Times New Roman',
                            east_font='宋体', space_before=0, space_after=0):
    """添加格式化段落"""
    p = doc.add_paragraph()
    if align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == 'right':
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == 'justify':
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if first_indent:
        p.paragraph_format.first_line_indent = Cm(0.74)
    p.paragraph_format.line_spacing = line_spacing
    if space_before:
        p.paragraph_format.space_before = Pt(space_before)
    if space_after:
        p.paragraph_format.space_after = Pt(space_after)

    run = p.add_run(text)
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.name = font_name
    run.element.rPr.rFonts.set(qn('w:eastAsia'), east_font)
    return p


def add_section_title(doc, number, title, level=1):
    """添加章节标题"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if level == 1:
        text = f'{number}  {title}'
        size = 16
    elif level == 2:
        text = f'{number}  {title}'
        size = 14
    else:
        text = title
        size = 13
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    return p


def add_table_with_data(doc, headers, rows, caption=None, col_widths=None):
    """添加带数据的表格"""
    if caption:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(caption)
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.name = 'Times New Roman'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)

    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_border(table)

    # 表头
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header)
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.name = 'Times New Roman'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        set_cell_shading(cell, 'D9E2F3')

    # 数据行
    for r, row_data in enumerate(rows):
        for c, cell_text in enumerate(row_data):
            cell = table.cell(r + 1, c)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(cell_text))
            run.font.size = Pt(9)
            run.font.name = 'Times New Roman'
            run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    doc.add_paragraph()  # 表后空行
    return table


def add_figure_placeholder(doc, caption, description):
    """添加图的占位描述（由于python-docx不支持直接画图，用文字框描述）"""
    # 图描述框
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)

    # 用虚线框表示图的位置
    border_p = doc.add_paragraph()
    border_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    border_p.paragraph_format.space_before = Pt(3)
    border_p.paragraph_format.space_after = Pt(3)

    # 添加描述文字
    run = border_p.add_run(f'┌{"─" * 60}┐')
    run.font.size = Pt(9)
    run.font.name = 'Courier New'

    desc_lines = description.split('\n')
    for line in desc_lines:
        p_line = doc.add_paragraph()
        p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
        padded = f'│ {line.strip():^58} │'
        run = p_line.add_run(padded)
        run.font.size = Pt(9)
        run.font.name = 'Courier New'

    p_end = doc.add_paragraph()
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p_end.add_run(f'└{"─" * 60}┘')
    run.font.size = Pt(9)
    run.font.name = 'Courier New'

    # 图题
    p_caption = doc.add_paragraph()
    p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_caption.paragraph_format.space_after = Pt(6)
    run = p_caption.add_run(caption)
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')


def add_formula(doc, formula_text, label=None):
    """添加公式（以文本形式展示数学公式）"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Cm(0)

    run = p.add_run(formula_text)
    run.font.size = Pt(11)
    run.font.italic = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    if label:
        run2 = p.add_run(f'    ({label})')
        run2.font.size = Pt(10)
        run2.font.name = 'Times New Roman'
    return p


def create_report_v2(title, subtitle, course_name, abstract, keywords, sections, conclusion,
                     references, output_filename):
    """创建增强版报告"""
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
    for _ in range(3):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(course_name)
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(subtitle)
    run.font.size = Pt(16)
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    for _ in range(3):
        doc.add_paragraph()

    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (label, value) in enumerate([
        ('姓    名：', ''), ('学    号：', ''),
        ('班    级：', ''), ('指导教师：', ''),
    ]):
        cell_l = table.cell(i, 0)
        p_l = cell_l.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run_l = p_l.add_run(label)
        run_l.font.size = Pt(14)
        run_l.font.name = 'Times New Roman'
        run_l.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

        cell_v = table.cell(i, 1)
        p_v = cell_v.paragraphs[0]
        run_v = p_v.add_run(value)
        run_v.font.size = Pt(14)
        run_v.font.name = 'Times New Roman'
        run_v.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        run_v.underline = True

    for _ in range(3):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('二〇二六年五月')
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    doc.add_page_break()

    # ===== 摘要 =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('摘  要')
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    add_formatted_paragraph(doc, abstract, first_indent=True, line_spacing=1.5)

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

    add_formatted_paragraph(doc, '(请在Word中插入自动目录：引用 → 目录 → 自动目录)',
                            align='center', first_indent=False, font_size=12)
    doc.add_page_break()

    # ===== 正文 =====
    section_counter = 0
    for section_data in sections:
        section_counter += 1

        # 解析section数据
        if isinstance(section_data, dict):
            sec_title = section_data['title']
            sec_content = section_data.get('content', '')
            tables = section_data.get('tables', [])
            figures = section_data.get('figures', [])
            formulas = section_data.get('formulas', [])
            subsections = section_data.get('subsections', [])
        else:
            sec_title, sec_content = section_data
            tables, figures, formulas, subsections = [], [], [], []

        # 章节标题
        add_section_title(doc, section_counter, sec_title, level=1)

        # 正文内容
        if sec_content:
            paragraphs = sec_content.strip().split('\n')
            for para_text in paragraphs:
                para_text = para_text.strip()
                if not para_text:
                    continue
                add_formatted_paragraph(doc, para_text)

        # 公式
        for formula_data in formulas:
            if isinstance(formula_data, dict):
                add_formula(doc, formula_data['text'], formula_data.get('label'))
            else:
                add_formula(doc, formula_data)

        # 表格
        for table_data in tables:
            if isinstance(table_data, dict):
                add_table_with_data(doc, table_data['headers'], table_data['rows'],
                                    table_data.get('caption'))

        # 图
        for fig_data in figures:
            if isinstance(fig_data, dict):
                add_figure_placeholder(doc, fig_data['caption'], fig_data['description'])

        # 子章节
        sub_counter = 0
        for sub_data in subsections:
            sub_counter += 1

            if isinstance(sub_data, dict):
                sub_title = sub_data['title']
                sub_content = sub_data.get('content', '')
                sub_tables = sub_data.get('tables', [])
                sub_figures = sub_data.get('figures', [])
                sub_formulas = sub_data.get('formulas', [])
            else:
                sub_title, sub_content = sub_data
                sub_tables, sub_figures, sub_formulas = [], [], []

            add_section_title(doc, f'{section_counter}.{sub_counter}', sub_title, level=2)

            if sub_content:
                paragraphs = sub_content.strip().split('\n')
                for para_text in paragraphs:
                    para_text = para_text.strip()
                    if not para_text:
                        continue
                    add_formatted_paragraph(doc, para_text)

            for formula_data in sub_formulas:
                if isinstance(formula_data, dict):
                    add_formula(doc, formula_data['text'], formula_data.get('label'))
                else:
                    add_formula(doc, formula_data)

            for table_data in sub_tables:
                if isinstance(table_data, dict):
                    add_table_with_data(doc, table_data['headers'], table_data['rows'],
                                        table_data.get('caption'))

            for fig_data in sub_figures:
                if isinstance(fig_data, dict):
                    add_figure_placeholder(doc, fig_data['caption'], fig_data['description'])

    # ===== 结论 =====
    add_section_title(doc, section_counter + 1, '结论', level=1)

    paragraphs = conclusion.strip().split('\n')
    for para_text in paragraphs:
        para_text = para_text.strip()
        if not para_text:
            continue
        add_formatted_paragraph(doc, para_text)

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
        run.font.size = Pt(10.5)
        run.font.name = 'Times New Roman'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)
    doc.save(filepath)
    print(f'报告已保存: {filepath}')
    return filepath


if __name__ == '__main__':
    print('报告生成工具V2已就绪。')
