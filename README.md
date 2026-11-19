# Academic Reports · 课程报告工具集

> 课程报告/实验报告的生成与排版工具：**ASR/TTS 综述报告** 与 **计算机网络实验报告**。代码负责生成结构、图表、表格与 Word 排版，正文由报告模板填充。

作者：**hhxpoint**

---

## 包含内容

### `asr-tts-survey/`

- `ASR_Survey_Paper.tex`：自动语音识别综述论文 LaTeX 源
- `generate_asr_report.py` / `generate_asr_v2.py`：ASR 报告生成
- `generate_tts_report.py` / `generate_tts_v2.py`：TTS 报告生成
- `generate_report.py` / `generate_report_v2.py`：通用报告生成
- 依赖：`python-docx`、`matplotlib`（按脚本实际 import）

### `network-labs/`

- `fix_all_reports.py`：批量修正实验报告中的截图/标题/编号
- `实验一-交换机路由器基本配置/`
- `实验二-局域网扩展/`
- `实验三-VLAN划分/`
- `实验四-服务器搭建/`
- 各实验含拓扑图、设备配置与 `generate_report.py`
- 原始 `.docx` 报告未纳入仓库（含个人姓名/学号）

---

## 运行

```bash
python -m venv .venv
.venv\Scripts\activate
pip install python-docx matplotlib
```

```bash
# ASR/TTS 报告
cd asr-tts-survey
python generate_asr_v2.py

# 网络实验报告
cd network-labs/实验一-交换机路由器基本配置
python generate_report.py
```

> 脚本中的输入/输出路径按本地目录编写，运行前请检查顶部常量。

---

## 说明

- 仓库仅包含代码、LaTeX、拓扑图、设备配置；**不包含带姓名/学号的 docx 报告**。
- 课程名称、实验模板版权归学校/课程组；代码与排版脚本由 hhxpoint 编写。
- 原始报告模板/截图未公开，避免隐私问题。

---

## 测试

```bash
python -m py_compile asr-tts-survey/*.py network-labs/fix_all_reports.py
# 各实验目录
python -m py_compile network-labs/实验*/generate_report.py
```

---

## License

MIT License（代码/脚本）；课程模板与图片素材遵循原课程要求。
