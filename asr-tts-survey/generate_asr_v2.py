#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成机器学习大作业报告V2：自动语音识别技术综述（ASR）- 增强版
包含丰富的表格、公式、图描述
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_report_v2 import create_report_v2

title = "自动语音识别技术综述"
subtitle = "——从传统GMM-HMM到端到端深度学习模型的演进"
course_name = "机器学习"

abstract = """自动语音识别（Automatic Speech Recognition, ASR）是机器学习领域的重要研究方向，\
旨在将语音信号自动转换为对应的文本序列。本文系统综述了ASR技术的发展历程，\
从早期的动态时间规整（DTW）方法，到基于高斯混合模型-隐马尔可夫模型（GMM-HMM）的经典方法，\
再到以深度神经网络为核心的现代端到端方法。重点介绍了DNN-HMM混合系统、\
基于连接主义时间分类（CTC）的模型、基于注意力机制的编码器-解码器模型、\
循环神经网络变换器（RNN-T/Transducer）以及Conformer架构等代表性工作。\
本文详细给出了各核心算法的数学公式推导，通过对比表格展示了不同方法在识别准确率、\
推理效率等方面的性能差异，并讨论了wav2vec 2.0、HuBERT等自监督预训练方法\
和Whisper等大规模弱监督模型的最新进展。"""

keywords = ["自动语音识别", "深度学习", "端到端模型", "自监督预训练", "Conformer"]

sections = [
    # ===== 第1章：引言 =====
    {
        'title': '引言',
        'content': """自动语音识别（Automatic Speech Recognition, ASR）技术是人工智能和人机交互领域的核心研究方向之一，其目标是将输入的语音波形信号自动转换为对应的文本序列。高质量的ASR系统在智能语音助手、自动转写、实时字幕、呼叫中心分析、医疗/法律记录等众多应用场景中具有广泛的实用价值。

从技术发展的时间线来看，ASR技术经历了四个主要阶段：（1）基于模板匹配的方法（1960s-1980s），（2）基于统计模型的GMM-HMM方法（1990s-2010s），（3）深度神经网络与HMM的混合方法（2012-2017），（4）端到端深度学习方法（2015至今）。每一次技术范式的转变都显著提升了识别的准确率和鲁棒性。

本文旨在对ASR技术的发展脉络进行全面梳理，重点分析各阶段的代表性方法和技术特点，并对当前的研究热点和未来发展方向进行讨论。""",
        'tables': [
            {
                'headers': ['发展阶段', '时间范围', '代表性方法', '核心技术', 'LibriSpeech WER'],
                'rows': [
                    ['模板匹配', '1960s-1980s', 'DTW', '动态规划对齐', '仅限孤立词'],
                    ['GMM-HMM', '1990s-2012', 'Kaldi/HTK', 'GMM+HMM+NGram', '~15%'],
                    ['DNN-HMM混合', '2012-2017', 'DNN/LSTM-HMM', 'DNN替代GMM', '~8%'],
                    ['端到端CTC', '2014-2018', 'Deep Speech 2', 'CTC损失函数', '~6%'],
                    ['端到端注意力', '2016-2019', 'LAS/Transformer', '注意力对齐', '~5%'],
                    ['RNN-T/Conformer', '2020至今', 'Conformer-RNN-T', '卷积+注意力', '~2%'],
                    ['自监督+微调', '2020至今', 'wav2vec 2.0/HuBERT', '预训练+微调', '~2%'],
                    ['大规模弱监督', '2022至今', 'Whisper', '680K小时训练', '~3%(多语言)'],
                ],
                'caption': '表1  自动语音识别技术发展阶段概览'
            }
        ],
        'figures': [
            {
                'caption': '图1  ASR系统通用处理流程',
                'description': '语音波形 → 特征提取 → 声学模型 → 解码器 → 文本输出\n[Fbank/MFCC] → [DNN/Transformer] → [CTC/RNN-T/Attention] → [词序列]'
            }
        ],
    },

    # ===== 第2章：传统语音识别方法 =====
    {
        'title': '传统语音识别方法',
        'subsections': [
            {
                'title': '动态时间规整方法',
                'content': """动态时间规整（Dynamic Time Warping, DTW）是最早被应用于语音识别的方法之一。DTW通过动态规划算法计算测试语音与参考模板之间的最优时间对齐距离，从而实现语音模式的匹配。

DTW的核心思想是：给定测试序列 X = (x₁, x₂, ..., xₘ) 和参考序列 Y = (y₁, y₂, ..., yₙ)，寻找最优的对齐路径 W = (w₁, w₂, ..., wₖ)，使得累积距离最小：""",
                'formulas': [
                    {'text': 'D(i, j) = d(xᵢ, yⱼ) + min{D(i-1, j), D(i, j-1), D(i-1, j-1)}', 'label': '1-1'},
                    {'text': '其中 d(xᵢ, yⱼ) = ||xᵢ - yⱼ||² 为局部距离度量，D(i,j) 为从(1,1)到(i,j)的最小累积距离。', 'label': None},
                ],
                'content2': """DTW方法的优点是概念简单、易于实现，适用于小词汇量的孤立词识别。但其局限性也很明显：需要为每个词存储参考模板，计算复杂度随词汇量增长而急剧增加，且对说话人变化和环境噪声的鲁棒性较差。""",
            },
            {
                'title': '基于GMM-HMM的经典方法',
                'content': """高斯混合模型-隐马尔可夫模型（GMM-HMM）框架是统计语音识别的经典范式，自1990年代起主导了ASR领域长达二十年。

在GMM-HMM框架中，HMM建模语音信号的时序动态特性。给定观测序列 O = (o₁, o₂, ..., oₜ)，HMM的联合概率可以分解为：""",
                'formulas': [
                    {'text': 'P(O, S|λ) = Πₜ p(oₜ|sₜ) · p(sₜ|sₜ₋₁)', 'label': '1-2'},
                    {'text': '其中 S = (s₁, s₂, ..., sₜ) 为隐状态序列，p(oₜ|sₜ) 为发射概率，p(sₜ|sₜ₋₁) 为转移概率。', 'label': None},
                ],
                'content': """GMM用于建模每个HMM状态的发射概率，即在给定状态下观测到某一特征向量的概率：""",
                'formulas': [
                    {'text': 'p(oₜ|sₜ) = Σₖ wₖ · N(oₜ; μₖ, Σₖ)', 'label': '1-3'},
                    {'text': '其中 K 为高斯分量数，wₖ 为混合权重（Σwₖ=1），μₖ 和 Σₖ 分别为第k个分量的均值向量和协方差矩阵。', 'label': None},
                ],
                'content': """在解码阶段，使用维特比算法（Viterbi Algorithm）搜索最可能的状态序列。维特比算法的递推公式为：""",
                'formulas': [
                    {'text': 'δₜ(j) = max_i [δₜ₋₁(i) · aᵢⱼ] · bⱼ(oₜ)', 'label': '1-4'},
                    {'text': '其中 δₜ(j) 为t时刻状态j的最大概率路径得分，aᵢⱼ 为状态转移概率，bⱼ(oₜ) 为发射概率。', 'label': None},
                ],
                'content2': """Rabiner于1989年发表了HMM的经典教程，系统总结了HMM在语音识别中的应用。该方法的代表性工具包包括HTK和Kaldi。GMM-HMM方法在大规模语音识别任务上取得了显著成功，但GMM的表达能力有限，难以捕捉声学特征中的复杂非线性关系。""",
                'figures': [
                    {
                        'caption': '图2  GMM-HMM语音识别系统架构',
                        'description': '语音信号 → MFCC/Fbank特征 → GMM声学建模 → HMM状态解码 → 语言模型重打分 → 文本\n[预处理] → [特征提取] → [P(O|S)] → [Viterbi] → [N-gram] → [词序列]'
                    }
                ],
            },
        ],
    },

    # ===== 第3章：深度学习在语音识别中的应用 =====
    {
        'title': '深度学习在语音识别中的应用',
        'subsections': [
            {
                'title': 'DNN-HMM混合系统',
                'content': """2012年，深度学习技术的引入彻底改变了语音识别的格局。Hinton等人提出使用深度神经网络（DNN）替代GMM来估计HMM状态的发射概率，开创了DNN-HMM混合系统的研究范式。

在DNN-HMM系统中，DNN输出的是HMM状态的后验概率 P(sₜ|oₜ)，通过贝叶斯公式转换为似然概率：""",
                'formulas': [
                    {'text': 'p(oₜ|sₜ) = P(sₜ|oₜ) · p(oₜ) / P(sₜ)', 'label': '2-1'},
                    {'text': '其中 P(sₜ) 为状态先验概率（从训练数据中统计），p(oₜ) 为观测概率（在解码时可忽略）。', 'label': None},
                ],
                'content': """DNN的前向传播过程可以表示为多层非线性变换：""",
                'formulas': [
                    {'text': 'h⁽⁰⁾ = oₜ  （输入特征）', 'label': None},
                    {'text': 'h⁽ˡ⁾ = σ(W⁽ˡ⁾ · h⁽ˡ⁻¹⁾ + b⁽ˡ⁾)  ，  l = 1, 2, ..., L', 'label': '2-2'},
                    {'text': 'y = softmax(W⁽ᴸ⁺¹⁾ · h⁽ᴸ⁾ + b⁽ᴸ⁺¹⁾)  （输出层）', 'label': None},
                    {'text': '其中 W⁽ˡ⁾, b⁽ˡ⁾ 为第l层的权重矩阵和偏置向量，σ 为激活函数（如ReLU），L为隐藏层数。', 'label': None},
                ],
                'content2': """Dahl等人将DNN应用于大词汇量连续语音识别，展示了深度学习在ASR中的巨大潜力。Seide等人在Switchboard数据集上首次展示了DNN-HMM系统相对于GMM-HMM系统的显著性能提升——词错误率从18.5%降至12.2%，相对降低34%。""",
            },
            {
                'title': '端到端模型：CTC方法',
                'content': """连接主义时间分类（Connectionist Temporal Classification, CTC）由Graves等人于2006年提出，是一种直接对输入序列和输出序列之间的对齐关系进行建模的损失函数。

CTC引入了"空白"（blank）符号 ε，允许模型在输入和输出长度不一致时进行端到端训练。给定输入序列 X 和目标标签序列 Y，CTC损失函数定义为所有可能对齐路径的概率之和的负对数：""",
                'formulas': [
                    {'text': 'L_CTC = -log P(Y|X) = -log Σ_{π∈B⁻¹(Y)} P(π|X)', 'label': '2-3'},
                    {'text': '其中 π 为输入长度为T的对齐路径，B 为去除重复和空白的映射函数，B⁻¹(Y) 为所有映射到Y的路径集合。', 'label': None},
                ],
                'content': """单步发射概率通过softmax计算：""",
                'formulas': [
                    {'text': 'P(πₜ|X) = softmax(zₜ)[πₜ]', 'label': '2-4'},
                    {'text': '其中 zₜ 为编码器在t时刻的输出logits。路径概率为各步发射概率的乘积：P(π|X) = Πₜ P(πₜ|X)。', 'label': None},
                ],
                'content': """CTC的关键算法是前向-后向算法，用于高效计算边际概率。前向变量 αₜ(j) 定义为：""",
                'formulas': [
                    {'text': 'αₜ(j) = Σ_{i∈{j-2,j-1,j}} αₜ₋₁(i) · P(πₜ=j|X)', 'label': '2-5'},
                    {'text': '其中边界条件为 α₁(1) = P(π₁=ε|X), α₁(2) = P(π₁=y₁|X), 其余为0。', 'label': None},
                ],
                'content2': """Hannun等人于2014年提出了Deep Speech，这是第一个大规模端到端CTC语音识别系统。Amodei等人于2016年进一步提出了Deep Speech 2，在英语和中文上均取得了当时最优的识别性能。""",
            },
            {
                'title': '端到端模型：注意力机制方法',
                'content': """注意力机制（Attention Mechanism）由Bahdanau等人于2015年在机器翻译领域提出，随后被引入语音识别。Chan等人于2016年提出了Listen, Attend and Spell（LAS），这是第一个基于注意力机制的端到端ASR模型。

在LAS中，编码器（Listener）将输入声学特征序列 X = (x₁, ..., xₜ) 编码为隐藏表示 H = (h₁, ..., hₜ')。解码器（Speller）在每一步通过注意力机制计算上下文向量：""",
                'formulas': [
                    {'text': 'eₜ,ᵢ = v^T · tanh(W_s · sₜ₋₁ + W_h · hᵢ + b_attn)', 'label': '2-6'},
                    {'text': 'αₜ,ᵢ = softmax(eₜ,ᵢ)  ，  cₜ = Σᵢ αₜ,ᵢ · hᵢ', 'label': '2-7'},
                    {'text': '其中 sₜ₋₁ 为解码器上一步的隐藏状态，αₜ,ᵢ 为注意力权重，cₜ 为上下文向量。', 'label': None},
                ],
                'content': """解码器输出字符概率分布：""",
                'formulas': [
                    {'text': 'P(yₜ|y<t, X) = softmax(W_o · [sₜ; cₜ] + b_o)', 'label': '2-8'},
                    {'text': '其中 [sₜ; cₜ] 为解码器状态和上下文向量的拼接，训练目标为最大化序列的对数似然。', 'label': None},
                ],
                'content2': """LAS消除了对发音词典、语言模型和HMM的依赖，实现了真正的端到端识别。然而，注意力机制在处理长序列时容易出现对齐错误。""",
            },
            {
                'title': '端到端模型：RNN-T/Transducer方法',
                'content': """RNN变换器（RNN-Transducer, RNN-T）由Graves于2012年提出，是对CTC框架的重要扩展。RNN-T由三个组件构成：编码器、预测网络和联合网络。

给定声学特征序列 X = (x₁, ..., xₜ) 和已输出的标签序列 y<ᵤ = (y₁, ..., yᵤ₋₁)，RNN-T的输出概率为：""",
                'formulas': [
                    {'text': 'hₜ = Encoder(X)₁₍ₜ₎  （编码器输出）', 'label': None},
                    {'text': 'gᵤ = Predictor(y<ᵤ)  （预测网络输出）', 'label': None},
                    {'text': 'P(yᵤ|X, y<ᵤ) = softmax(Joint(hₜ, gᵤ))', 'label': '2-9'},
                    {'text': '其中 Joint(hₜ, gᵤ) = W_j · [hₜ; gᵤ] + b_j 为联合网络。', 'label': None},
                ],
                'content': """与CTC不同，RNN-T能够建模输出标签之间的相互依赖关系。其训练目标为对所有合法对齐路径求和：""",
                'formulas': [
                    {'text': 'L_RNNT = -log Σ_{π∈B⁻¹(Y)} Πₜ P(πₜ|X, π<ₜ)', 'label': '2-10'},
                    {'text': '使用前向-后向算法在 (T×U) 的网格上高效计算。', 'label': None},
                ],
                'content2': """RNN-T已被广泛应用于Google、Apple等公司的生产级语音识别系统中，成为端到端ASR的主流架构之一。""",
            },
            {
                'title': 'Conformer架构',
                'content': """2020年，Gulati等人提出了Conformer（Convolution-augmented Transformer），将自注意力机制和卷积操作结合在单个编码器块中。

Conformer块采用"Macaron"结构，包含以下四个子模块：""",
                'formulas': [
                    {'text': 'x\' = x + 0.5 · FFN(x)  （第一个前馈模块）', 'label': None},
                    {'text': 'x\'\' = x\' + MHSA(x\')  （多头自注意力）', 'label': None},
                    {'text': 'x\'\'\' = x\'\' + Conv(x\'\')  （卷积模块）', 'label': None},
                    {'text': 'y = LayerNorm(x\'\'\' + 0.5 · FFN(x\'\'))  （第二个前馈模块）', 'label': '2-11'},
                ],
                'content': """其中多头自注意力（MHSA）的计算为：""",
                'formulas': [
                    {'text': 'Q = XW_Q, K = XW_K, V = XW_V', 'label': None},
                    {'text': 'MHSA(X) = softmax(QK^T / √d_k) · V', 'label': '2-12'},
                    {'text': '其中 d_k 为键向量的维度，用于缩放点积以防止梯度消失。', 'label': None},
                ],
                'content': """卷积模块包含一个扩展为两倍的逐点卷积、GLU门控激活、深度可分离卷积和批归一化：""",
                'formulas': [
                    {'text': 'Conv(x) = BN(DepthwiseConv(GLU(PWConv(x))))', 'label': '2-13'},
                    {'text': '其中 GLU(a,b) = a ⊙ σ(b) 为门控线性单元，BN为批归一化。', 'label': None},
                ],
                'content2': """Conformer的核心思想是自注意力和卷积是互补的：自注意力擅长捕捉全局依赖关系，而卷积擅长学习局部特征。两者结合后，Conformer在LibriSpeech基准测试上取得了当时最优的识别性能，WER在test-clean/test-other上分别达到1.9%/3.9%（不使用语言模型）。""",
                'figures': [
                    {
                        'caption': '图3  Conformer编码器块结构',
                        'description': '输入 → FFN(×0.5) → 多头自注意力 → 卷积模块 → FFN(×0.5) → LayerNorm → 输出\n[Macaron结构] 残差连接 + 0.5缩放'
                    }
                ],
            },
        ],
    },

    # ===== 第4章：自监督预训练方法 =====
    {
        'title': '自监督预训练方法',
        'content': """自监督预训练方法通过在大量无标注语音数据上学习通用的语音表示，然后在下游任务上进行微调，极大地降低了对标注数据的依赖。""",
        'tables': [
            {
                'headers': ['模型', '年份', '预训练目标', '预训练数据', '标注数据需求', 'LibriSpeech WER'],
                'rows': [
                    ['wav2vec 2.0', '2020', '掩码预测+对比学习', '960h(无标注)', '10min', '3.4%'],
                    ['HuBERT', '2021', '掩码预测(聚类伪标签)', '60kh(无标注)', '10min', '3.3%'],
                    ['WavLM', '2022', '掩码预测+去噪', '94kh(无标注)', '10min', '3.2%'],
                    ['wav2vec 2.0 Large', '2020', '掩码预测+对比学习', '60kh(无标注)', '100h', '1.8%'],
                    ['HuBERT Large', '2021', '掩码预测(聚类伪标签)', '60kh(无标注)', '100h', '1.9%'],
                ],
                'caption': '表2  自监督预训练语音模型对比（LibriSpeech test-clean WER）'
            }
        ],
        'subsections': [
            {
                'title': 'wav2vec 2.0',
                'content': """wav2vec 2.0由Baevski等人于2020年提出，是一种自监督语音表示学习框架。该方法的核心思想是对原始音频进行掩码预测：使用CNN特征编码器和Transformer编码器处理语音信号，对潜在语音表示进行掩码，并通过对比损失学习量化表示。

wav2vec 2.0的训练包含两个关键步骤。首先，CNN编码器将原始波形转换为帧级特征序列 Z = (z₁, z₂, ..., zₜ)，然后对部分帧进行掩码。Transformer编码器处理掩码后的特征，输出上下文化表示 C = (c₁, c₂, ..., cₜ)。

对比损失函数定义为：""",
                'formulas': [
                    {'text': 'L_k = -log exp(sim(cₜ, qₜ) / κ) / Σ_{q̃~Q} exp(sim(cₜ, q̃) / κ)', 'label': '3-1'},
                    {'text': '其中 qₜ 为目标量化表示（正样本），Q 为包含负样本的量化表示集合，κ 为温度参数。', 'label': None},
                ],
                'content': """量化过程使用产品量化（Product Quantization），将特征空间分割为多个子空间，每个子空间独立进行k-means聚类。最终的量化码本由各子空间码本的笛卡尔积构成。""",
                'formulas': [
                    {'text': 'qₜ = Quantize(zₜ) = [qₜ¹, qₜ², ..., qₜᵍ]', 'label': '3-2'},
                    {'text': '其中 G 为子空间数量，每个 qₜᵍ 从对应的码本中选择。', 'label': None},
                ],
                'content2': """wav2vec 2.0的关键创新在于：仅需10分钟的标注数据即可在LibriSpeech上取得有竞争力的识别性能，同时利用约53,000小时的无标注音频进行自监督预训练。这一工作开创了"预训练+微调"的语音识别新范式。""",
            },
            {
                'title': 'HuBERT',
                'content': """HuBERT（Hidden-Unit BERT）由Hsu等人于2021年提出，是一种受BERT启发的自监督语音表示学习方法。HuBERT使用离线聚类生成伪标签（隐藏单元），并以掩码预测的方式进行训练。

HuBERT的训练损失函数为：""",
                'formulas': [
                    {'text': 'L_HuBERT = -Σ_{t∈M} log P(cₜ | x̃)', 'label': '3-3'},
                    {'text': '其中 M 为被掩码的位置集合，cₜ 为聚类伪标签，x̃ 为掩码后的输入。', 'label': None},
                ],
                'content': """HuBERT的训练过程是迭代的：第一轮使用MFCC特征进行k-means聚类生成伪标签；后续轮次使用上一轮模型的中间层特征进行聚类，随着模型的改进，聚类质量也在迭代中不断提升。这种迭代训练策略使得HuBERT能够学习到越来越好的语音表示。""",
                'content2': """HuBERT在多个语音任务（ASR、说话人识别、情感识别等）上取得了最优结果，证明了掩码预测与聚类分配相结合的方法在语音表示学习中的有效性。""",
            },
            {
                'title': 'WavLM',
                'content': """WavLM由Chen等人于2022年提出，通过在预训练中引入去噪目标，增强了模型对噪声和说话人变化的鲁棒性。WavLM的训练目标结合了掩码预测和去噪：""",
                'formulas': [
                    {'text': 'L_WavLM = L_masked + λ · L_denoise', 'label': '3-4'},
                    {'text': '其中 L_masked 为掩码预测损失，L_denoise 为去噪损失，λ 为权重系数。', 'label': None},
                ],
                'content2': """WavLM在SUPERB基准测试中表现出色，特别是在说话人相关任务上展现了强大的能力。WavLM与wav2vec 2.0和HuBERT一起，成为自监督语音表示学习的三大基础模型。""",
            },
        ],
    },

    # ===== 第5章：Whisper模型 =====
    {
        'title': '大规模弱监督模型：Whisper',
        'content': """Whisper由Radford等人于2022年提出，是OpenAI开发的通用语音识别模型。Whisper在680,000小时的多语言和多任务监督数据上训练，这些数据通过弱监督方式从互联网上收集。""",
        'tables': [
            {
                'headers': ['模型规模', '参数量', '编码器层', '解码器层', '模型维度', '多语言WER'],
                'rows': [
                    ['Tiny', '39M', '4', '4', '384', '12.7%'],
                    ['Base', '74M', '6', '6', '512', '10.0%'],
                    ['Small', '244M', '12', '12', '768', '7.3%'],
                    ['Medium', '769M', '24', '24', '1024', '5.4%'],
                    ['Large-v3', '1550M', '32', '32', '1280', '4.5%'],
                ],
                'caption': '表3  Whisper模型规模与性能对比'
            }
        ],
        'content': """Whisper采用标准的编码器-解码器Transformer架构。编码器处理80维对数mel频谱图特征，使用步长为2的卷积进行下采样，然后通过Transformer层进行编码。

Whisper的训练数据格式包含了多种任务标记：""",
        'formulas': [
            {'text': '输入: <|startoftranscript|><|language|><|task|><|notimestamps|> ... <|endoftranscript|>', 'label': '4-1'},
            {'text': '其中 <|language|> 标记目标语言，<|task|> 区分转写(transcribe)和翻译(translate)任务。', 'label': None},
        ],
        'content': """Whisper的核心特点包括：（1）大规模、多样化的训练数据带来了强大的泛化能力；（2）支持多语言语音识别、语音翻译、语种识别和语音活动检测等多种任务；（3）模型规模从Tiny到Large不等，支持不同计算资源条件下的部署。""",
    },

    # ===== 第6章：端到端方法对比分析 =====
    {
        'title': '端到端方法对比分析',
        'tables': [
            {
                'headers': ['方法', '代表模型', '对齐方式', '语言模型依赖', '流式支持', 'LibriSpeech WER'],
                'rows': [
                    ['CTC', 'Deep Speech 2', '隐式(空白)', '需要融合', '天然支持', '~6%'],
                    ['注意力', 'LAS', '显式(注意力)', '可选', '困难', '~5%'],
                    ['RNN-T', 'Conformer-RNN-T', '隐式(空白)', '可选融合', '天然支持', '~2.5%'],
                    ['Transducer', 'RNN-T+Conformer', '隐式(空白)', '可选融合', '天然支持', '~2.0%'],
                    ['混合CTC/Attention', 'ESPnet', 'CTC+注意力', '可选', '部分支持', '~2.5%'],
                ],
                'caption': '表4  端到端ASR方法综合对比'
            },
            {
                'headers': ['基准数据集', '语言', '训练集大小', '测试集', '主要特点'],
                'rows': [
                    ['LibriSpeech', '英语', '960小时', 'test-clean/test-other', '有声书朗读，最常用基准'],
                    ['AISHELL-1', '中文(普通话)', '178小时', 'test', '中文ASR标准基准'],
                    ['Switchboard', '英语', '300小时', 'eval2000', '电话对话，口语化'],
                    ['Common Voice', '多语言', '>10000小时', '各语言test', '众包录音，多语言'],
                    ['GigaSpeech', '英语', '10000小时', 'test', '大规模多领域'],
                    ['WenetSpeech', '中文', '10000+小时', 'test_net/test_meeting', '大规模中文多场景'],
                ],
                'caption': '表5  主流ASR基准数据集'
            },
        ],
        'content': """不同的端到端方法在对齐方式、语言模型依赖和流式支持等方面各有特点。CTC和RNN-T天然支持流式识别，因为它们不需要等待完整话语即可输出结果。注意力机制方法在非流式场景下通常能达到更好的识别准确率，但在流式场景下需要特殊设计（如单调注意力）。

在语言模型融合方面，CTC和RNN-T通常受益于外部语言模型的浅融合（Shallow Fusion），即在解码时将声学模型和语言模型的得分进行线性加权：""",
        'formulas': [
            {'text': 'score(y|X) = log P_AM(y|X) + α · log P_LM(y) + β · |y|', 'label': '5-1'},
            {'text': '其中 P_AM 为声学模型输出概率，P_LM 为语言模型概率，α 为语言模型权重，β 为长度惩罚系数。', 'label': None},
        ],
    },

    # ===== 第7章：应用场景与挑战 =====
    {
        'title': '应用场景与挑战展望',
        'tables': [
            {
                'headers': ['挑战', '具体问题', '当前解决方案', '未来方向'],
                'rows': [
                    ['噪声鲁棒性', '高噪声环境下性能下降', '数据增强(SpecAugment)', '抗噪预训练+前端处理'],
                    ['口音处理', '不同口音识别率差异大', '多口音混合训练', '自适应微调+口音编码'],
                    ['代码混合', '多语言混合使用', '多语言联合训练', '语言感知编码器'],
                    ['长音频', '计算复杂度高', '分段处理+拼接', '流式+上下文建模'],
                    ['计算效率', '大模型推理成本高', '模型压缩/量化/蒸馏', '高效架构设计'],
                    ['领域适配', '专业术语识别率低', '领域微调+热词增强', '持续学习+提示学习'],
                ],
                'caption': '表6  ASR技术主要挑战与解决方案'
            }
        ],
        'content': """自动语音识别技术在众多领域具有广泛的应用价值。在智能语音助手领域，Siri、Alexa、Google Assistant等语音助手的核心就是ASR系统。在自动转写领域，ASR技术可以大幅提高文字记录的效率。在实时字幕领域，ASR技术可以生成实时字幕，提升信息获取的便利性。

数据增强是提升ASR鲁棒性的重要手段。SpecAugment是最常用的数据增强方法之一，通过对频谱图进行时间扭曲、频率掩码和时间掩码来增加训练数据的多样性：""",
        'formulas': [
            {'text': 'S_augmented = TimeMask(FreqMask(TimeWarp(S_original)))', 'label': '6-1'},
            {'text': '其中 S_original 为原始频谱图，FreqMask 随机遮蔽频率通道，TimeMask 随机遮蔽时间帧。', 'label': None},
        ],
        'content2': """展望未来，ASR技术将在以下方向继续发展：（1）语音基础模型将变得更加强大和通用；（2）端到端模型将与大语言模型深度融合；（3）自监督预训练方法将进一步降低对标注数据的依赖；（4）多模态融合将为ASR提供更丰富的上下文信息；（5）隐私保护和联邦学习将在ASR训练和部署中发挥越来越重要的作用。""",
    },
]

conclusion = """自动语音识别技术经过数十年的发展，已经从早期的模板匹配方法演进到基于深度学习的端到端方法，识别准确率从早期的有限词汇量孤立词识别提升到了接近人类水平的连续语音识别。

本文系统回顾了ASR技术的发展历程：从基于DTW的模板匹配方法，到基于GMM-HMM的经典统计方法，再到以DNN-HMM混合系统、CTC模型、注意力机制模型和RNN-T为代表的端到端深度学习方法。特别地，DNN-HMM混合系统开创了深度学习在ASR中的应用，CTC和RNN-T实现了真正的端到端训练，Conformer架构将自注意力和卷积的优势相结合，成为现代ASR系统的标准编码器。

在自监督预训练方面，wav2vec 2.0、HuBERT和WavLM等方法通过在大量无标注数据上进行预训练，大幅降低了对标注数据的依赖，为低资源语言的ASR提供了新的解决方案。Whisper通过大规模弱监督学习，构建了通用的、鲁棒的语音识别系统，标志着ASR进入了基础模型时代。

然而，ASR技术仍面临噪声鲁棒性、口音处理、代码混合和长音频等挑战。随着深度学习技术的持续进步和计算资源的不断提升，我们有理由期待ASR技术将在更多场景中实现真正鲁棒、高效的人机语音交互。同时，语音基础模型的发展将进一步推动ASR技术的通用化和民主化，使得高质量的语音识别能力惠及更多语言和应用场景。"""

references = [
    'Radford A, Kim J W, Xu T, et al. Robust speech recognition via large-scale weak supervision[C]. International Conference on Machine Learning (ICML), Honolulu, USA: PMLR, 2023.',
    'Baevski A, Zhou Y, Mohamed A, et al. wav2vec 2.0: A framework for self-supervised learning of speech representations[C]. Advances in Neural Information Processing Systems (NeurIPS), Virtual: Curran Associates, 2020.',
    'Gulati A, Qin J, Chung C, et al. Conformer: Convolution-augmented transformer for speech recognition[C]. Interspeech, Shanghai, China: ISCA, 2020: 5036-5040.',
    'Sakoe H, Chiba S. Dynamic programming algorithm optimization for spoken word recognition[J]. IEEE Transactions on Acoustics, Speech, and Signal Processing, 1978, 26(1): 43-49.',
    'Rabiner L. A tutorial on hidden Markov models and selected applications in speech recognition[J]. Proceedings of the IEEE, 1989, 77(2): 257-286.',
    'Hinton G, Deng L, Yu D, et al. Deep neural networks for acoustic modeling in speech recognition: The shared views of four research groups[J]. IEEE Signal Processing Magazine, 2012, 29(6): 82-97.',
    'Dahl G E, Yu D, Deng L, et al. Context-dependent pre-trained deep neural networks for large-vocabulary speech recognition[J]. IEEE Transactions on Audio, Speech, and Language Processing, 2012, 20(1): 30-42.',
    'Seide F, Li G, Chen X, et al. Feature engineering in context-dependent deep neural networks for conversational speech transcription[C]. IEEE Workshop on Automatic Speech Recognition and Understanding (ASRU), Waikoloa, USA: IEEE, 2011: 24-29.',
    'Abdel-Hamid O, Mohamed A, Jiang H, et al. Applying convolutional neural networks concepts to hybrid NN-HMM model for speech recognition[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Kyoto, Japan: IEEE, 2012: 4277-4280.',
    'Hochreiter S, Schmidhuber J. Long short-term memory[J]. Neural Computation, 1997, 9(8): 1735-1780.',
    'Graves A, Fernández S, Gomez F, et al. Connectionist temporal classification: Labelling unsegmented sequence data with recurrent neural networks[C]. International Conference on Machine Learning (ICML), Pittsburgh, USA: ACM, 2006: 369-376.',
    'Hannun A, Case C, Casper J, et al. Deep speech: Scaling up end-to-end speech recognition[J]. arXiv preprint arXiv:1412.5567, 2014.',
    'Amodei D, Ananthanarayanan S, Anubhai R, et al. Deep speech 2: End-to-end speech recognition in English and Mandarin[C]. International Conference on Machine Learning (ICML), New York, USA: PMLR, 2016: 173-182.',
    'Bahdanau D, Cho K, Bengio Y. Neural machine translation by jointly learning to align and translate[C]. International Conference on Learning Representations (ICLR), San Diego, USA: OpenReview, 2015.',
    'Chan W, Jaitly N, Le Q, et al. Listen, attend and spell: A neural network for large vocabulary conversational speech recognition[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Shanghai, China: IEEE, 2016: 4960-4964.',
    'Graves A. Sequence transduction with recurrent neural networks[C]. ICML Workshop on Representation Learning, Edinburgh, UK: PMLR, 2012.',
    'Hsu W N, Bolte B, Tsai Y H, et al. HuBERT: Self-supervised speech representation learning by masked prediction of hidden units[J]. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 2021, 29: 3451-3460.',
    'Chen S, Wang C, Chen Z, et al. WavLM: Large-scale self-supervised pre-training for full stack speech processing[J]. IEEE Journal of Selected Topics in Signal Processing, 2022, 16(6): 1505-1518.',
    'Bommasani R, Hudson D A, Adeli E, et al. On the opportunities and risks of foundation models[J]. arXiv preprint arXiv:2108.07258, 2021.',
    'Pratap V, Tjandra A, Shi B, et al. Scaling speech technology to 1,000+ languages[J]. Journal of Machine Learning Research, 2024, 25(1): 1-52.',
    'Graves A, Mohamed A, Hinton G. Speech recognition with deep recurrent neural networks[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Vancouver, Canada: IEEE, 2013: 6645-6649.',
    'Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need[C]. Advances in Neural Information Processing Systems (NeurIPS), Long Beach, USA: Curran Associates, 2017: 5998-6008.',
    'Panayotov V, Chen G, Povey D, et al. LibriSpeech: An ASR corpus based on public domain audio books[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Brisbane, Australia: IEEE, 2015: 5206-5210.',
    'Bu H, Du J, Na X, et al. AISHELL-1: An open-source Mandarin speech corpus and a speech recognition baseline[C]. Oriental COCOSDA, Seoul, South Korea: IEEE, 2017: 1-5.',
    'Xu Q, Baevski A, Likhomanenko T, et al. Self-training and pre-training are complementary for speech recognition[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Toronto, Canada: IEEE, 2021: 3030-3034.',
    'Park D S, Zhang W, Jia Y, et al. SpecAugment: A simple data augmentation method for ASR[C]. Interspeech, Graz, Austria: ISCA, 2019: 2613-2617.',
    'Ko T, Peddinti V, Povey D, et al. Audio augmentation for speech recognition[C]. Interspeech, Dresden, Germany: ISCA, 2015: 3586-3589.',
    'Li B, Gulati A, Yu J, et al. A better and faster end-to-end model for streaming ASR[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Toronto, Canada: IEEE, 2021: 5654-5658.',
    'Watanabe S, Mandel M, Barker J, et al. CHiME-6 challenge: Tackling multispeaker speech recognition for unsegmented recordings[C]. CHiME Workshop, Barcelona, Spain: ISCA, 2020.',
    'Synnaeve G, Xu Q, Kahn J, et al. End-to-end ASR: From supervised to semi-supervised learning with modern architectures[C]. ICML Workshop on Self-Supervised Learning for Speech and Audio Processing, Virtual: PMLR, 2020.',
]

output_file = '机器学习_自动语音识别技术综述报告_V2.docx'
create_report_v2(title=title, subtitle=subtitle, course_name=course_name,
                 abstract=abstract, keywords=keywords, sections=sections,
                 conclusion=conclusion, references=references, output_filename=output_file)
print("ASR增强版报告生成完成！")
