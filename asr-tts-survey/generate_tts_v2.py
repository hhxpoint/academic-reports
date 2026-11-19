#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成人工智能基础大作业报告V2：语音合成技术综述（TTS）- 增强版
包含丰富的表格、公式、图描述
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_report_v2 import create_report_v2

title = "语音合成技术综述"
subtitle = "——从统计参数模型到神经网络端到端方法的演进"
course_name = "人工智能基础"

abstract = """语音合成（Text-to-Speech, TTS）是人工智能领域的重要研究方向，旨在将文本信息转换为自然流畅的语音信号。\
本文系统综述了语音合成技术的发展历程，从早期的拼接合成与共振峰合成方法，到基于隐马尔可夫模型（HMM）的统计参数合成方法，\
再到近年来以深度学习为核心的神经网络端到端合成方法。重点介绍了WaveNet、Tacotron、FastSpeech、VITS等里程碑式的神经网络TTS模型，\
以及基于扩散模型和神经编解码器语言模型的最新进展。本文详细分析了各方法的核心算法原理，给出了关键模型的数学公式描述，\
并通过对比表格展示了不同方法在合成质量、推理速度、鲁棒性等方面的性能差异。同时讨论了韵律建模、多说话人合成、零样本语音克隆等关键技术问题，\
并对语音合成技术的未来发展趋势进行了展望。"""

keywords = ["语音合成", "深度学习", "端到端模型", "神经声码器", "零样本合成"]

# ============================================================
# 章节内容定义
# ============================================================

sections = [
    # ===== 第1章：引言 =====
    {
        'title': '引言',
        'content': """语音合成（Text-to-Speech, TTS）技术是人工智能和人机交互领域的核心研究方向之一，其目标是将输入的文本序列转换为可感知的语音波形信号。高质量的语音合成系统在智能语音助手、有声读物、无障碍辅助、影视配音、虚拟数字人等众多应用场景中具有广泛的实用价值。

从技术发展的时间线来看，语音合成技术经历了三个主要阶段：（1）基于规则的共振峰合成方法（1960s-1990s），（2）基于统计模型的参数合成方法（2000s-2010s），（3）基于深度学习的端到端合成方法（2016至今）。每一次技术范式的转变都显著提升了合成语音的自然度和表现力。

近年来，随着深度学习技术的快速发展，神经网络TTS系统在语音质量上已经接近甚至达到了人类语音的水平。特别是以WaveNet、Tacotron 2、VITS、VALL-E为代表的一系列工作，不断刷新着语音合成的质量上限。本文旨在对语音合成技术的发展脉络进行全面梳理，重点分析各阶段的代表性方法和技术特点，并对当前的研究热点和未来发展方向进行讨论。""",
        'tables': [
            {
                'headers': ['发展阶段', '时间范围', '代表性方法', '核心技术', '合成质量'],
                'rows': [
                    ['规则合成', '1960s-1990s', 'Klatt合成器', '共振峰参数控制', '低（明显机器音）'],
                    ['拼接合成', '1990s-2000s', 'AT&T Natural Voices', '单元选择与拼接', '中（有拼接伪影）'],
                    ['统计参数合成', '2000s-2010s', 'HTS (HMM-TTS)', 'HMM+声码器', '中（过平滑问题）'],
                    ['神经网络TTS', '2016至今', 'Tacotron 2, VITS', '深度学习端到端', '高（接近人类）'],
                    ['大模型TTS', '2023至今', 'VALL-E, StyleTTS 2', '编解码器语言模型', '极高（人类水平）'],
                ],
                'caption': '表1  语音合成技术发展阶段概览'
            }
        ],
        'figures': [
            {
                'caption': '图1  语音合成系统通用架构框图',
                'description': '文本前端 → 声学模型 → 声码器 → 语音波形\n[文本分析] → [音素序列] → [声学特征] → [波形信号]'
            }
        ],
    },

    # ===== 第2章：传统语音合成方法 =====
    {
        'title': '传统语音合成方法',
        'subsections': [
            {
                'title': '拼接合成方法',
                'content': """拼接合成（Concatenative Synthesis）是最早被广泛商用的语音合成方法。其核心思想是预先录制大量语音片段并建立语音数据库，合成时根据目标音素序列和韵律要求，从数据库中选择最佳匹配的语音单元并进行拼接。Hunt和Black于1996年提出了基于大语料库的单元选择框架，成为拼接合成的经典范式。

拼接合成的目标函数可以表示为最小化拼接代价和目标代价的加权和。设候选单元序列为 u = (u₁, u₂, ..., uₙ)，则最优单元序列通过以下优化问题求得：""",
                'formulas': [
                    {'text': 'û = arg min_u [ Σᵢ D_target(uᵢ) + Σᵢ D_concat(uᵢ, uᵢ₊₁) ]', 'label': '1-1'},
                    {'text': '其中 D_target(uᵢ) 表示单元 uᵢ 与目标韵律特征的偏差，D_concat(uᵢ, uᵢ₊₁) 表示相邻单元的拼接代价。', 'label': None},
                ],
                'content2': """拼接合成的优点在于当语音数据库足够大时可以获得较高的语音质量，因为合成结果直接来源于真实录音。然而，该方法存在明显的局限性：需要庞大的语音数据库（通常需要数十小时的录音），对未见韵律上下文的泛化能力较差，且在单元拼接边界处容易产生可感知的拼接伪影。""",
            },
            {
                'title': '共振峰合成方法',
                'content': """共振峰合成（Formant Synthesis）基于数学模型模拟人类声道的声学特性，通过规则控制共振峰频率、带宽和幅度等参数来生成语音。Klatt于1980年提出的级联/并联共振峰合成器是该领域的经典工作。

在共振峰合成中，声道传递函数 V(z) 通常表示为多个二阶谐振器的级联形式：""",
                'formulas': [
                    {'text': 'V(z) = Πₖ Gₖ / (1 - 2rₖcos(2πfₖT)z⁻¹ + rₖ²z⁻²)', 'label': '1-2'},
                    {'text': '其中 fₖ 为第k个共振峰频率，rₖ 为极点半径（控制带宽），Gₖ 为增益因子，T为采样周期。', 'label': None},
                ],
                'content2': """共振峰合成的优点是模型体积极小（仅需几百字节的参数）、参数完全可控，适合嵌入式设备。但其合成语音带有明显的"机器音"，自然度较低，且规则的设计需要大量的语音学专业知识，难以扩展到新语言。""",
            },
            {
                'title': '基于HMM的统计参数合成',
                'content': """隐马尔可夫模型（Hidden Markov Model, HMM）被引入语音合成领域后，催生了统计参数语音合成方法。该方法使用HMM对频谱参数、基频和时长等声学特征进行建模，合成时通过参数生成算法输出声学参数，再经声码器（如STRAIGHT或WORLD）重建波形。

在HMM-TTS中，给定文本特征序列 W，声学特征序列 O = (o₁, o₂, ..., o_T) 的生成过程可以表示为：""",
                'formulas': [
                    {'text': 'P(O|W) = Σ_π Πₜ p(oₜ|sₜ, W) · p(sₜ|sₜ₋₁, W)', 'label': '1-3'},
                    {'text': '其中 sₜ 为t时刻的HMM状态，π 为状态序列，p(oₜ|sₜ) 为高斯发射概率。', 'label': None},
                ],
                'content2': """Tokuda等人于2000年提出了基于动态特征的语音参数生成算法，奠定了HMM-TTS的基础。Zen等人在2009年发表了统计参数语音合成的权威综述，系统总结了该范式的完整流程。

HMM-TTS的优点是模型灵活、体积小、完全由数据驱动。但其固有的过平滑问题导致合成语音听起来发闷，声码器伪影也影响了自然度。""",
            },
        ],
    },

    # ===== 第3章：神经网络语音合成方法 =====
    {
        'title': '神经网络语音合成方法',
        'subsections': [
            {
                'title': 'WaveNet：神经声码器的革命',
                'content': """2016年，DeepMind的van den Oord等人提出了WaveNet，这是一个直接对原始音频波形进行建模的深度生成模型。WaveNet使用扩张因果卷积（Dilated Causal Convolution）网络，以自回归方式逐采样点生成16kHz的音频波形。

WaveNet的核心思想是将联合概率分布分解为条件概率的乘积：""",
                'formulas': [
                    {'text': 'p(x) = Πₜ p(xₜ | x₁, x₂, ..., xₜ₋₁)', 'label': '2-1'},
                    {'text': '其中 x = (x₁, x₂, ..., x_T) 为原始音频采样序列，每个采样点的条件分布由神经网络参数化。', 'label': None},
                ],
                'content': """WaveNet的网络结构采用扩张因果卷积，第l层的输出可以表示为：""",
                'formulas': [
                    {'text': 'hₗ = tanh(Wₗ,f ∗ x) ⊙ σ(Wₗ,g ∗ x)', 'label': '2-2'},
                    {'text': '其中 ∗ 表示扩张卷积运算，⊙ 表示逐元素乘法，σ 为sigmoid激活函数。门控激活机制结合了tanh和sigmoid，使模型能够选择性地传递信息。', 'label': None},
                ],
                'content2': """WaveNet在TTS和语音生成任务上均取得了当时最优的平均意见得分（MOS），显著超越了传统方法。尽管WaveNet的自回归特性导致推理速度较慢，但它证明了神经网络能够生成高度自然的语音波形，开创了神经声码器的研究范式。""",
                'figures': [
                    {
                        'caption': '图2  WaveNet扩张因果卷积结构示意图',
                        'description': '输入层 → 扩张卷积(d=1) → 扩张卷积(d=2) → 扩张卷积(d=4) → ... → 输出层\n每层使用门控激活: tanh ⊙ sigmoid\n扩张因子呈指数增长: 1, 2, 4, 8, 16, ...'
                    }
                ],
            },
            {
                'title': 'Tacotron系列：端到端神经TTS',
                'content': """2017年，Google的Wang等人提出了Tacotron，这是第一个实用的端到端神经TTS系统。Tacotron接收字符输入，通过编码器-注意力-解码器架构直接生成频谱图，再使用Griffin-Lim算法重建波形。

在Tacotron 2中，编码器将输入的音素序列 p = (p₁, p₂, ..., pₙ) 映射为隐藏表示 h = (h₁, h₂, ..., hₙ)。解码器在每一步 t 通过注意力机制计算上下文向量 cₜ：""",
                'formulas': [
                    {'text': 'αₜᵢ = softmax(eₜᵢ)  ，  eₜᵢ = score(sₜ₋₁, hᵢ)', 'label': '2-3'},
                    {'text': 'cₜ = Σᵢ αₜᵢ · hᵢ', 'label': '2-4'},
                    {'text': '其中 sₜ₋₁ 为解码器上一步的隐藏状态，αₜᵢ 为注意力权重，score() 为注意力打分函数。', 'label': None},
                ],
                'content': """Tacotron 2在解码器端采用自回归方式逐帧生成mel频谱图：""",
                'formulas': [
                    {'text': 'mₜ = Decoder(sₜ, cₜ)  ，  sₜ = RNN(sₜ₋₁, [mₜ₋₁, cₜ])', 'label': '2-5'},
                    {'text': '其中 mₜ 为t时刻的mel频谱帧，RNN为循环神经网络单元。', 'label': None},
                ],
                'content2': """Tacotron 2将序列到序列声学模型与WaveNet声码器相结合，在MOS评测中达到了与人类语音相当的水平（4.53 vs. 人类4.58），成为神经TTS领域的事实标准基线。""",
            },
            {
                'title': 'FastSpeech系列：非自回归TTS',
                'content': """自回归TTS模型存在两个主要问题：推理速度慢和注意力对齐失败导致的单词跳过/重复。Ren等人于2019年提出了FastSpeech，这是第一个非自回归神经TTS模型。

FastSpeech的核心是时长预测器（Duration Predictor），它预测每个音素对应的帧数。给定音素序列的隐藏表示 H，时长预测器输出：""",
                'formulas': [
                    {'text': 'd̂ = DurationPredictor(H)  ，  d̂ᵢ ∈ ℤ⁺', 'label': '2-6'},
                    {'text': '其中 d̂ᵢ 为第i个音素预测的持续帧数。通过时长信息，隐藏表示被展开为帧级别的序列。', 'label': None},
                ],
                'content': """FastSpeech 2在此基础上增加了基频（F0）预测器和能量预测器，实现了更好的韵律控制。其总训练损失函数为：""",
                'formulas': [
                    {'text': 'L = L_mel + λ₁·L_dur + λ₂·L_pitch + λ₃·L_energy', 'label': '2-7'},
                    {'text': '其中 L_mel 为mel频谱重建损失，L_dur、L_pitch、L_energy 分别为时长、基频和能量的预测损失，λ₁、λ₂、λ₃ 为权重系数。', 'label': None},
                ],
                'content2': """FastSpeech 2在语音质量上达到了与自回归模型相当的水平，同时推理速度比Tacotron 2快270倍以上。""",
            },
            {
                'title': 'VITS：完全端到端的TTS',
                'content': """2021年，Kim等人提出了VITS，将条件变分自编码器（CVAE）、归一化流和对抗训练结合在一个完全端到端的框架中。

VITS的训练目标基于变分推断的证据下界（ELBO）：""",
                'formulas': [
                    {'text': 'L_ELBO = E_q(z|x)[log p(x|z)] - KL(q(z|x) || p(z|c))', 'label': '2-8'},
                    {'text': '其中 z 为潜在变量，x 为波形，c 为文本条件，q(z|x) 为编码器后验分布，p(z|c) 为先验分布。', 'label': None},
                ],
                'content': """VITS还引入了归一化流（Normalizing Flow）来增强先验分布的表达能力，以及对抗训练来提升生成质量。其完整训练损失为：""",
                'formulas': [
                    {'text': 'L = L_ELBO + L_adv(G) + L_fm + L_dur + L_cls(D)', 'label': '2-9'},
                    {'text': '其中 L_adv 为对抗损失，L_fm 为特征匹配损失，L_dur 为时长损失，L_cls 为判别器分类损失。', 'label': None},
                ],
                'content2': """VITS直接从文本生成波形，无需独立的声码器，在MOS评测中达到了与人类语音相当的水平，并支持多说话人和情感合成。该工作获得了ISCA最佳论文奖。""",
            },
        ],
    },

    # ===== 第4章：神经声码器的演进 =====
    {
        'title': '神经声码器的演进',
        'content': """神经声码器是神经网络TTS系统的关键组件，负责将声学特征（如mel频谱图）转换为时域波形。自WaveNet开创这一研究方向以来，多种不同架构的神经声码器相继被提出，在合成质量和推理效率之间取得了不同的平衡。""",
        'tables': [
            {
                'headers': ['声码器', '年份', '架构类型', '生成方式', '实时因子', 'MOS (LJSpeech)'],
                'rows': [
                    ['WaveNet', '2016', '扩张因果CNN', '自回归', '~0.01', '4.35'],
                    ['WaveRNN', '2018', '单层RNN', '自回归', '~0.5', '4.20'],
                    ['WaveGlow', '2019', '归一化流', '并行', '~40', '4.30'],
                    ['MelGAN', '2019', 'GAN', '并行', '>100', '3.90'],
                    ['MB-MelGAN', '2020', 'GAN+多频带', '并行', '>200', '4.10'],
                    ['HiFi-GAN v1', '2020', 'GAN+MRF', '并行', '>100', '4.36'],
                    ['HiFi-GAN v3', '2020', 'GAN+MRF(轻量)', '并行', '>200', '4.18'],
                ],
                'caption': '表2  主流神经声码器性能对比'
            }
        ],
        'subsections': [
            {
                'title': 'WaveRNN：高效循环声码器',
                'content': """Kalchbrenner等人于2018年提出了WaveRNN，通过单层循环神经网络配合权重剪枝和双Softmax实现了高效的波形生成。WaveRNN将16位音频采样分解为高8位和低8位两个部分，分别进行预测，从而将输出空间从65536缩减到2×256，大幅降低了计算复杂度。WaveRNN可在移动设备上实时运行，推理速度比WaveNet快约50倍。""",
            },
            {
                'title': 'WaveGlow：流模型声码器',
                'content': """Prenger等人于2019年提出了WaveGlow，基于流模型（Glow）实现了并行波形生成。WaveGlow通过一系列可逆变换将简单的高斯分布映射到复杂的波形分布，训练时使用最大似然估计：""",
                'formulas': [
                    {'text': 'log p(x) = log p(z) + Σₖ log|det(∂fₖ/∂zₖ₋₁)|⁻¹', 'label': '3-1'},
                    {'text': '其中 z 为高斯噪声，fₖ 为第k个可逆变换。推理时直接从噪声采样并通过变换生成波形。', 'label': None},
                ],
                'content2': """WaveGlow在保持WaveNet级别质量的同时大幅提升了生成速度，但由于模型参数量较大（约256M），部署时需要较多计算资源。""",
            },
            {
                'title': 'HiFi-GAN：高保真对抗声码器',
                'content': """Kong等人于2020年提出的HiFi-GAN成为现代TTS流水线中的标准声码器。HiFi-GAN采用多感受野融合（MRF）生成器和多周期判别器。其生成器的损失函数包括：""",
                'formulas': [
                    {'text': 'L_G = L_adv(G) + λ_fm · L_fm(G, D) + λ_mel · L_mel(G)', 'label': '3-2'},
                    {'text': '其中 L_adv 为对抗损失，L_fm 为特征匹配损失，L_mel 为mel频谱重建损失。', 'label': None},
                ],
                'content': """多周期判别器（Multi-Period Discriminator, MPD）由多个子判别器组成，每个子判别器在不同的周期上对输入进行一维处理，从而捕捉不同时间尺度上的模式。其判别器损失为：""",
                'formulas': [
                    {'text': 'L_D = Σₖ [E[(Dₖ(x)-1)²] + E[Dₖ(G(y))²]]', 'label': '3-3'},
                    {'text': '其中 Dₖ 为第k个周期子判别器，x为真实波形，y为mel频谱，G(y)为生成波形。', 'label': None},
                ],
                'content2': """HiFi-GAN在实时因子上比WaveNet快数个数量级，同时保持了高保真度的合成质量，已被广泛应用于各种TTS系统中。""",
            },
        ],
    },

    # ===== 第5章：前沿研究方向 =====
    {
        'title': '前沿研究方向',
        'subsections': [
            {
                'title': '基于扩散模型的TTS',
                'content': """去噪扩散概率模型（Denoising Diffusion Probabilistic Models, DDPM）被引入TTS领域后，为语音合成带来了新的研究方向。扩散模型的核心思想是定义一个从数据到噪声的前向过程和一个从噪声到数据的反向去噪过程。

前向过程逐步向数据添加高斯噪声：""",
                'formulas': [
                    {'text': 'q(xₜ|xₜ₋₁) = N(xₜ; √(1-βₜ)·xₜ₋₁, βₜ·I)', 'label': '4-1'},
                    {'text': '其中 βₜ 为噪声调度参数，T为总步数。反向过程通过神经网络学习去噪：', 'label': None},
                ],
                'content': """反向去噪过程：""",
                'formulas': [
                    {'text': 'p_θ(xₜ₋₁|xₜ) = N(xₜ₋₁; μ_θ(xₜ, t), σₜ²·I)', 'label': '4-2'},
                    {'text': '其中 μ_θ 为神经网络预测的均值，σₜ 为固定的方差。训练目标为简化的去噪目标：', 'label': None},
                    {'text': 'L_simple = E_{t,x₀,ε}[||ε - ε_θ(xₜ, t)||²]', 'label': '4-3'},
                    {'text': '其中 ε 为添加的噪声，ε_θ 为噪声预测网络。', 'label': None},
                ],
                'content2': """Popov等人于2021年提出了Grad-TTS，将扩散模型应用于mel频谱图生成。Jeong等人同年提出了Diff-TTS。2024年，Shen等人提出了NaturalSpeech 2，使用潜在扩散模型实现零样本语音和歌唱合成。""",
            },
            {
                'title': '基于神经编解码器语言模型的TTS',
                'content': """2023年，Wang等人提出了VALL-E，将TTS建模为对神经编解码器token的条件语言生成任务。VALL-E使用EnCodec将语音波形离散化为多层codec token序列，然后以自回归语言模型的方式生成这些token。

设语音波形 x 经EnCodec编码后得到离散token序列 C = {c¹, c², ..., cᴸ}，其中每层 l 包含 T 个token。VALL-E的训练目标为：""",
                'formulas': [
                    {'text': 'L = -Σₜ Σₗ log P(cₜˡ | c<ₜ, cₜ<ˡ, e(p))', 'label': '4-4'},
                    {'text': '其中 e(p) 为音素序列的嵌入表示，c<ₜ 为前序时间步的token，cₜ<ˡ 为当前时间步低层的token。', 'label': None},
                ],
                'content2': """VALL-E在60,000小时的英语数据上训练，仅需3秒的注册音频即可实现零样本语音合成。这一工作标志着TTS范式的重大转变：从直接预测声学特征到语言建模。随后，VALL-E 2在零样本TTS基准测试上达到了人类水平。""",
            },
            {
                'title': '韵律建模与表现力合成',
                'content': """韵律（Prosody）——语音的节奏、重音和语调——对合成语音的自然度至关重要。韵律建模的核心挑战是如何从文本中预测出自然且多样化的韵律模式。

在层次化韵律建模中，韵律信息可以在三个层次上进行建模：话语级（utterance-level）、词级（word-level）和音素级（phoneme-level）。设韵律潜在变量为 z，其层次分解为：""",
                'formulas': [
                    {'text': 'z = [z_utt; z_word; z_phone]', 'label': '4-5'},
                    {'text': '其中 z_utt 为话语级韵律特征，z_word 为词级韵律特征，z_phone 为音素级韵律特征。', 'label': None},
                ],
                'content2': """Skerry-Ryan等人于2018年提出了韵律编码器用于Tacotron中的说话风格迁移。Lee和Kim于2019年提出了细粒度韵律控制方法。Sun等人于2020年引入了层次化韵律建模，支持在话语、词和音素级别进行可解释的韵律控制。""",
            },
        ],
    },

    # ===== 第6章：关键技术对比分析 =====
    {
        'title': '关键技术对比分析',
        'tables': [
            {
                'headers': ['方法类型', '代表模型', '生成方式', '推理速度', '语音质量(MOS)', '鲁棒性', '可控性'],
                'rows': [
                    ['自回归频谱', 'Tacotron 2', '逐帧生成', '慢(×1)', '4.53', '中(注意力失败)', '中'],
                    ['非自回归频谱', 'FastSpeech 2', '并行生成', '快(×270)', '4.40', '高', '高(时长/基频/能量)'],
                    ['端到端VAE/Flow', 'VITS', '并行生成', '快(×100)', '4.50', '高', '中'],
                    ['编解码器LM', 'VALL-E', '自回归token', '慢', '4.38', '中', '高(3秒克隆)'],
                    ['扩散模型', 'NaturalSpeech 2', '迭代去噪', '中', '4.52', '高', '高(零样本)'],
                    ['风格扩散', 'StyleTTS 2', '风格采样', '快', '4.61', '高', '高(风格控制)'],
                ],
                'caption': '表3  主流TTS方法综合对比'
            },
            {
                'headers': ['注意力机制', '类型', '优点', '缺点', '应用场景'],
                'rows': [
                    ['加性注意力', '软注意力', '计算简单', '对齐不稳定', '早期Seq2Seq'],
                    ['位置敏感注意力', '软注意力', '利用累积权重', '仍有失败情况', 'Tacotron'],
                    ['单调注意力', '硬注意力', '强制单调对齐', '灵活性较低', '鲁棒TTS'],
                    ['MAS (Glow-TTS)', '动态规划', '确定性对齐', '需要训练配合', 'Glow-TTS/VITS'],
                ],
                'caption': '表4  TTS中常用注意力机制对比'
            },
        ],
        'content': """自回归与非自回归方法各有优劣。自回归方法（如Tacotron 2、VALL-E）能够捕捉帧间的依赖关系，生成多样化的语音，但推理速度较慢且容易出现注意力对齐失败。非自回归方法（如FastSpeech 2、VITS）通过并行生成实现了快速推理和高鲁棒性，但通常需要额外的机制（如时长预测器）来处理输入输出的对齐问题。

在声码器选择上，基于GAN的声码器（如HiFi-GAN）因其高效的并行生成能力和高质量的合成效果，已成为现代TTS流水线的首选。基于流模型的声码器（如WaveGlow）虽然也能并行生成，但模型体积较大。自回归声码器（如WaveNet、WaveRNN）在质量上仍有优势，但推理速度成为瓶颈。""",
    },

    # ===== 第7章：应用场景与挑战 =====
    {
        'title': '应用场景与挑战展望',
        'content': """语音合成技术在众多领域具有广泛的应用价值。在智能语音助手领域，现代语音助手（Alexa、Siri、Google Assistant）均采用神经TTS以提供更自然的语音交互体验。在有声读物与内容创作领域，Amazon Polly、Google Cloud TTS等云服务提供神经TTS语音。在无障碍辅助领域，TTS技术对视障用户的屏幕阅读器和语言障碍患者的辅助沟通设备至关重要。""",
        'tables': [
            {
                'headers': ['挑战', '具体问题', '当前解决方案', '未来方向'],
                'rows': [
                    ['鲁棒性', '注意力对齐失败导致单词跳过/重复', '非自回归模型(FastSpeech)', '更可靠的对齐机制'],
                    ['韵律自然度', '长话语韵律不自然', '层次化韵律建模', '上下文感知韵律预测'],
                    ['推理效率', '大模型推理成本高', '模型压缩/量化', '高效架构设计'],
                    ['低资源语言', '缺少训练数据', '跨语言迁移学习', '多语言预训练基础模型'],
                    ['安全性', '语音克隆被滥用', '音频水印/检测', '法规+技术双重保障'],
                ],
                'caption': '表5  TTS技术主要挑战与解决方案'
            }
        ],
        'subsections': [
            {
                'title': '语音克隆的伦理问题',
                'content': """从几秒音频克隆任意声音的能力引发了严重的伦理关切。深度伪造语音可能被用于欺诈、身份冒充和虚假信息传播。行业对此的应对措施包括音频水印技术（如Resemble AI的PerTh、Adobe的内容凭证）、基于同意的声音克隆机制，以及相关的立法努力。研究者也在积极开发深度伪造语音检测技术，以识别AI生成的语音。""",
            },
        ],
    },
]

conclusion = """语音合成技术经过数十年的发展，已经从早期的规则驱动方法演进到数据驱动的神经网络方法，合成语音的质量从明显的"机器音"提升到了接近人类语音的水平。

本文系统回顾了语音合成技术的发展历程：从拼接合成和共振峰合成等传统方法，到基于HMM的统计参数合成方法，再到以WaveNet、Tacotron 2、FastSpeech、VITS为代表的神经网络端到端方法。特别地，WaveNet开创了神经声码器的研究范式，Tacotron 2实现了端到端TTS的人类级质量，FastSpeech解决了推理效率和鲁棒性问题，VITS实现了完全端到端的高质量合成。

在前沿方向上，基于扩散模型的TTS方法为多样性和质量的平衡提供了新思路，基于神经编解码器语言模型的方法（如VALL-E）将TTS推向了零样本合成的新范式。韵律建模、多说话人合成和语音克隆等技术也在不断取得突破。

然而，语音合成技术仍面临鲁棒性、韵律自然度、推理效率和低资源语言等挑战。随着深度学习技术的持续进步和计算资源的不断提升，我们有理由期待语音合成技术将在更多场景中实现真正自然、表现力丰富的人机语音交互。同时，语音合成技术的伦理和安全问题也需要得到充分重视，以确保技术的健康发展。"""

references = [
    'van den Oord A, Dieleman S, Zen H, et al. WaveNet: A generative model for raw audio[J]. arXiv preprint arXiv:1609.03499, 2016.',
    'Shen J, Pang R, Weiss R J, et al. Natural TTS synthesis by conditioning WaveNet on mel spectrogram predictions[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Calgary, Canada: IEEE, 2018: 4779-4783.',
    'Kim J, Kong J, Son J. Conditional variational autoencoder with adversarial learning for end-to-end text-to-speech[C]. International Conference on Machine Learning (ICML), Virtual: PMLR, 2021: 5530-5540.',
    'Wang C, Chen S, Wu Y, et al. Neural codec language models are zero-shot text to speech synthesizers[C]. International Conference on Learning Representations (ICLR), Vienna, Austria: OpenReview, 2024.',
    'Hunt A J, Black A W. Unit selection in a concatenative speech synthesis system using a large speech database[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Atlanta, USA: IEEE, 1996: 373-376.',
    'Klatt D H. Software for a cascade/parallel formant synthesizer[J]. Journal of the Acoustical Society of America, 1980, 67(3): 971-995.',
    'Tokuda K, Yoshimura T, Masuko T, et al. Speech parameter generation algorithms for HMM-based speech synthesis[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Istanbul, Turkey: IEEE, 2000: 1315-1318.',
    'Zen H, Tokuda K, Black A W. Statistical parametric speech synthesis[J]. Speech Communication, 2009, 51(11): 1039-1064.',
    'Wang Y, Skerry-Ryan R J, Stanton D, et al. Tacotron: Towards end-to-end speech synthesis[C]. Interspeech, Stockholm, Sweden: ISCA, 2017: 2227-2231.',
    'Ren Y, Ruan Y, Tan X, et al. FastSpeech: Fast, robust and controllable text to speech[C]. Advances in Neural Information Processing Systems (NeurIPS), Vancouver, Canada: Curran Associates, 2019: 3171-3180.',
    'Ren Y, Hu C, Tan X, et al. FastSpeech 2: Fast and high-quality end-to-end text to speech[C]. International Conference on Learning Representations (ICLR), Virtual: OpenReview, 2021.',
    'Kalchbrenner N, Elsen E, Simonyan K, et al. Efficient neural audio synthesis[C]. International Conference on Machine Learning (ICML), Stockholm, Sweden: PMLR, 2018: 2410-2419.',
    'Prenger R, Valle R, Catanzaro B. WaveGlow: A flow-based generative network for speech synthesis[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Brighton, UK: IEEE, 2019: 3617-3621.',
    'Kong J, Kim J, Bae J. HiFi-GAN: Generative adversarial networks for efficient and high fidelity speech synthesis[C]. Advances in Neural Information Processing Systems (NeurIPS), Virtual: Curran Associates, 2020: 17022-17033.',
    'Popov V, Vovk I, Gogoryan V, et al. Grad-TTS: A diffusion probabilistic model for text-to-speech[C]. International Conference on Machine Learning (ICML), Virtual: PMLR, 2021: 8599-8608.',
    'Jeong M, Kim H, Cheon S J, et al. Diff-TTS: A denoising diffusion model for text-to-speech[C]. Interspeech, Brno, Czech Republic: ISCA, 2021: 3605-3609.',
    'Shen K, Ju Z, Tan X, et al. NaturalSpeech 2: Latent diffusion models are natural and zero-shot speech and singing synthesizers[C]. International Conference on Learning Representations (ICLR), Vienna, Austria: OpenReview, 2024.',
    'Wang C, et al. VALL-E 2: Neural codec language models are human parity zero-shot text to speech synthesizers[J]. arXiv preprint arXiv:2406.05370, 2024.',
    'Du Z, Chen Q, Zhang Y, et al. CosyVoice: A scalable multilingual zero-shot text-to-speech synthesizer based on supervised semantic tokens[J]. arXiv preprint arXiv:2407.05407, 2024.',
    'Skerry-Ryan R J, Battenberg E, Xiao Y, et al. Towards end-to-end prosody transfer for expressive speech synthesis[C]. International Conference on Machine Learning (ICML), Stockholm, Sweden: PMLR, 2018: 4693-4702.',
    'Lee Y, Kim T. Robust and fine-grained prosody control of end-to-end speech synthesis[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Brighton, UK: IEEE, 2019: 5911-5915.',
    'Sun G, Zhang Y, Weiss R J, et al. Fully-hierarchical fine-grained prosody modeling for interpretable speech synthesis[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Barcelona, Spain: IEEE, 2020: 6274-6278.',
    'Jia Y, Weiss R J, Biadsy F, et al. Direct cloning of voices using neural TTS[C]. Interspeech, Graz, Austria: ISCA, 2019: 266-270.',
    'Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need[C]. Advances in Neural Information Processing Systems (NeurIPS), Long Beach, USA: Curran Associates, 2017: 5998-6008.',
    'Kim J, Kong J, Son J. Glow-TTS: A generative flow for text-to-speech via monotonic alignment search[C]. Advances in Neural Information Processing Systems (NeurIPS), Virtual: Curran Associates, 2020: 10609-10620.',
    'Tan X, Chen J, Liu H, et al. NaturalSpeech: End-to-end text to speech synthesis with human-level quality[C]. International Conference on Machine Learning (ICML), Baltimore, USA: PMLR, 2022: 33887-33910.',
    'Li T, Liu T, Kulkarni A, et al. StyleTTS 2: Towards human-level text-to-speech through style diffusion and adversarial training with large speech language models[C]. Advances in Neural Information Processing Systems (NeurIPS), New Orleans, USA: Curran Associates, 2023.',
    'Arik S O, Chrzanowski M, Coates A, et al. Deep Voice: Real-time neural text-to-speech[C]. International Conference on Machine Learning (ICML), Sydney, Australia: PMLR, 2017: 195-204.',
    'Yang G, Yang S, Liu K, et al. Multi-band MelGAN: Faster waveform generation for high-quality text-to-speech[C]. IEEE Spoken Language Technology Workshop (SLT), Shenzhen, China: IEEE, 2021: 492-499.',
    'Kundan K, Kumar R, Raghuram A, et al. MelGAN: Generative adversarial networks for conditional waveform synthesis[C]. Advances in Neural Information Processing Systems (NeurIPS), Vancouver, Canada: Curran Associates, 2019: 14910-14921.',
]

output_file = '人工智能基础_语音合成技术综述报告_V2.docx'
create_report_v2(title=title, subtitle=subtitle, course_name=course_name,
                 abstract=abstract, keywords=keywords, sections=sections,
                 conclusion=conclusion, references=references, output_filename=output_file)
print("TTS增强版报告生成完成！")
