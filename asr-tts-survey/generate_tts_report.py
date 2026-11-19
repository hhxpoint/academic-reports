#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成人工智能基础大作业报告：语音合成技术综述（TTS）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_report import create_report

# ===== 报告内容 =====

title = "语音合成技术综述"
subtitle = "——从统计参数模型到神经网络端到端方法的演进"
course_name = "人工智能基础"

abstract = """语音合成（Text-to-Speech, TTS）是人工智能领域的重要研究方向，旨在将文本信息转换为自然流畅的语音信号。\
本文系统综述了语音合成技术的发展历程，从早期的拼接合成与共振峰合成方法，到基于隐马尔可夫模型（HMM）的统计参数合成方法，\
再到近年来以深度学习为核心的神经网络端到端合成方法。重点介绍了WaveNet、Tacotron、FastSpeech、VITS等里程碑式的神经网络TTS模型，\
以及基于扩散模型和神经编解码器语言模型的最新进展。同时讨论了韵律建模、多说话人合成、零样本语音克隆等关键技术问题，\
并对语音合成技术的未来发展趋势进行了展望。"""

keywords = ["语音合成", "深度学习", "端到端模型", "神经声码器", "零样本合成"]

sections = [
    ("引言",
"""语音合成（Text-to-Speech, TTS）技术是人工智能和人机交互领域的核心研究方向之一，其目标是将输入的文本序列转换为可感知的语音波形信号。\
高质量的语音合成系统在智能语音助手、有声读物、无障碍辅助、影视配音、虚拟数字人等众多应用场景中具有广泛的实用价值。

从技术发展的时间线来看，语音合成技术经历了三个主要阶段：（1）基于规则的共振峰合成方法（1960s-1990s），\
（2）基于统计模型的参数合成方法（2000s-2010s），（3）基于深度学习的端到端合成方法（2016至今）。\
每一次技术范式的转变都显著提升了合成语音的自然度和表现力。

近年来，随着深度学习技术的快速发展，神经网络TTS系统在语音质量上已经接近甚至达到了人类语音的水平。\
特别是以WaveNet[1]、Tacotron 2[2]、VITS[3]、VALL-E[4]为代表的一系列工作，不断刷新着语音合成的质量上限。\
本文旨在对语音合成技术的发展脉络进行全面梳理，重点分析各阶段的代表性方法和技术特点，\
并对当前的研究热点和未来发展方向进行讨论。"""),

    ("传统语音合成方法",
"""## 2.1 拼接合成方法

拼接合成（Concatenative Synthesis）是最早被广泛商用的语音合成方法。其核心思想是预先录制大量语音片段并建立语音数据库，\
合成时根据目标音素序列和韵律要求，从数据库中选择最佳匹配的语音单元并进行拼接。Hunt和Black[5]于1996年提出了基于大语料库的单元选择框架，\
成为拼接合成的经典范式。

拼接合成的优点在于当语音数据库足够大时可以获得较高的语音质量，因为合成结果直接来源于真实录音。\
然而，该方法存在明显的局限性：需要庞大的语音数据库，对未见韵律上下文的泛化能力较差，且在单元拼接边界处容易产生可感知的拼接伪影。

## 2.2 共振峰合成方法

共振峰合成（Formant Synthesis）基于数学模型模拟人类声道的声学特性，通过规则控制共振峰频率、带宽和幅度等参数来生成语音。\
Klatt[6]于1980年提出的级联/并联共振峰合成器是该领域的经典工作。

共振峰合成的优点是模型体积极小、参数完全可控，适合嵌入式设备。\
但其合成语音带有明显的"机器音"，自然度较低，且规则的设计需要大量的语音学专业知识，难以扩展到新语言。

## 2.3 基于HMM的统计参数合成

隐马尔可夫模型（Hidden Markov Model, HMM）被引入语音合成领域后，催生了统计参数语音合成方法。\
该方法使用HMM对频谱参数、基频和时长等声学特征进行建模，合成时通过参数生成算法输出声学参数，再经声码器（如STRAIGHT或WORLD）重建波形。

Tokuda等人[7]于2000年提出了基于动态特征的语音参数生成算法，奠定了HMM-TTS的基础。\
Zen等人[8]在2009年发表了统计参数语音合成的权威综述，系统总结了该范式的完整流程：文本分析、基于决策树聚类的上下文相关HMM声学建模、参数生成和波形合成。

HMM-TTS的优点是模型灵活、体积小、完全由数据驱动。\
但其固有的过平滑问题导致合成语音听起来发闷，声码器伪影也影响了自然度。"""),

    ("神经网络语音合成方法",
"""## 3.1 WaveNet：神经声码器的革命

2016年，DeepMind的van den Oord等人[1]提出了WaveNet，这是一个直接对原始音频波形进行建模的深度生成模型。\
WaveNet使用扩张因果卷积（Dilated Causal Convolution）网络，以自回归方式逐采样点生成16kHz的音频波形。\
其核心创新包括：因果卷积确保模型不会使用未来信息；扩张卷积高效地处理长程依赖；门控激活机制和残差/跳跃连接提升模型表达能力。

WaveNet在TTS和语音生成任务上均取得了当时最优的平均意见得分（MOS），显著超越了传统方法。\
尽管WaveNet的自回归特性导致推理速度较慢（每秒仅能生成约200个采样点），但它证明了神经网络能够生成高度自然的语音波形，\
开创了神经声码器的研究范式。

## 3.2 Tacotron系列：端到端神经TTS

2017年，Google的Wang等人[9]提出了Tacotron，这是第一个实用的端到端神经TTS系统。\
Tacotron接收字符输入，通过编码器-注意力-解码器架构直接生成频谱图，再使用Griffin-Lim算法重建波形。\
该工作证明了单个神经网络能够直接从文本学习合成语音。

2018年，Shen等人[2]提出了Tacotron 2，将序列到序列声学模型与WaveNet声码器相结合。\
该系统在MOS评测中达到了与人类语音相当的水平（4.53 vs. 人类4.58），成为神经TTS领域的事实标准基线。\
Tacotron 2的成功表明，当声学模型和声码器都采用神经网络时，端到端TTS可以达到接近人类的语音质量。

## 3.3 FastSpeech系列：非自回归TTS

自回归TTS模型（如Tacotron）存在两个主要问题：推理速度慢和注意力对齐失败导致的单词跳过/重复。\
Ren等人[10]于2019年提出了FastSpeech，这是第一个非自回归神经TTS模型。\
FastSpeech使用前馈Transformer架构配合时长预测器，实现了并行生成，推理速度比Tacotron 2快270倍。

2020年，Ren等人[11]进一步提出了FastSpeech 2，通过直接使用真实目标进行训练（消除了对教师模型的依赖），\
并增加了基频预测器和能量预测器，实现了更好的韵律控制。\
FastSpeech 2在语音质量上达到了与自回归模型相当的水平，同时保持了快速推理的优势。

## 3.4 VITS：完全端到端的TTS

2021年，Kim等人[3]提出了VITS（Variational Inference with adversarial learning for end-to-end Text-to-Speech），\
将条件变分自编码器、归一化流和对抗训练结合在一个完全端到端的框架中。\
VITS直接从文本生成波形，无需独立的声码器，在MOS评测中达到了与人类语音相当的水平，\
并支持多说话人和情感合成。该工作获得了ISCA最佳论文奖，代表了端到端TTS的重要里程碑。

## 3.5 神经声码器的演进

除了WaveNet，神经声码器领域也涌现出众多重要工作。Kalchbrenner等人[12]于2018年提出了WaveRNN，\
通过单层循环神经网络配合权重剪枝和双Softmax实现了高效的波形生成，可在移动设备上实时运行。

Prenger等人[13]于2019年提出了WaveGlow，基于流模型（Glow）实现了并行波形生成，\
在保持WaveNet级别质量的同时大幅提升了生成速度。

Kong等人[14]于2020年提出的HiFi-GAN成为现代TTS流水线中的标准声码器。\
HiFi-GAN采用多感受野融合（MRF）生成器和多周期判别器，\
在实时因子上比WaveNet快数个数量级，同时保持了高保真度的合成质量。"""),

    ("前沿研究方向",
"""## 4.1 基于扩散模型的TTS

去噪扩散概率模型（Denoising Diffusion Probabilistic Models）被引入TTS领域后，为语音合成带来了新的研究方向。\
Popov等人[15]于2021年提出了Grad-TTS，将基于分数的扩散模型应用于频谱图生成，\
能够产生多样且高质量的输出。Jeong等人[16]同年提出了Diff-TTS，是最早将去噪扩散模型应用于TTS的工作之一。

2024年，Shen等人[17]提出了NaturalSpeech 2，使用潜在扩散模型实现零样本语音和歌唱合成，\
在未见说话人上实现了高自然度和说话人相似度。扩散模型在TTS中的应用为多样性和质量的平衡提供了新的解决思路。

## 4.2 基于神经编解码器语言模型的TTS

2023年，Wang等人[4]提出了VALL-E，将TTS建模为对神经编解码器token的条件语言生成任务。\
VALL-E在60,000小时的英语数据上训练，仅需3秒的注册音频即可实现零样本语音合成。\
这一工作标志着TTS范式的重大转变：从直接预测声学特征到语言建模。

VALL-E之后，基于编解码器语言模型的TTS方法迅速发展。\
Wang等人[18]于2024年提出了VALL-E 2，在零样本TTS基准测试上达到了人类水平。\
Du等人[19]提出了CosyVoice，使用有监督语义token实现多语言零样本TTS。

## 4.3 韵律建模与表现力合成

韵律（Prosody）——语音的节奏、重音和语调——对合成语音的自然度至关重要。\
Skerry-Ryan等人[20]于2018年提出了韵律编码器用于Tacotron中的说话风格迁移，\
实现了无需显式情感标签的表现力合成。Lee和Kim[21]于2019年提出了细粒度韵律控制方法。\
Sun等人[22]于2020年引入了层次化韵律建模，支持在话语、词和音素级别进行可解释的韵律控制。

## 4.4 多说话人与零样本TTS

多说话人TTS通过说话人编码器（Speaker Encoder）条件化声学模型来实现。\
Jia等人[23]于2019年展示了使用说话人编码器对多说话人Tacotron模型进行声音克隆的方法。\
VALL-E[4]和NaturalSpeech 2[17]进一步将零样本TTS推向了新的高度，\
仅需数秒的参考音频即可克隆未见说话人的声音。

## 4.5 语音克隆的伦理问题

从几秒音频克隆任意声音的能力引发了严重的伦理关切。\
深度伪造语音可能被用于欺诈、身份冒充和虚假信息传播。\
行业对此的应对措施包括音频水印技术（如Resemble AI的PerTh、Adobe的内容凭证）、\
基于同意的声音克隆机制，以及相关的立法努力。"""),

    ("应用场景",
"""语音合成技术在众多领域具有广泛的应用价值：

（1）智能语音助手：现代语音助手（Alexa、Siri、Google Assistant、Cortana）均采用神经TTS以提供更自然的语音交互体验。\
Google于2017年将其生产环境的TTS系统从拼接合成切换为基于WaveNet的合成方案。

（2）有声读物与内容创作：Amazon Polly、Google Cloud TTS、Microsoft Azure TTS等云服务提供神经TTS语音，\
用于有声书朗读、新闻播报和无障碍内容生成。

（3）无障碍辅助：TTS技术对视障用户的屏幕阅读器、语言障碍患者的辅助沟通设备、语言学习应用等至关重要。

（4）影视配音与娱乐：神经TTS用于自动配音、游戏角色语音和虚拟数字人。\
实时声音克隆技术的发展使得电影后期制作和本地化配音成为可能。

（5）虚拟数字人与元宇宙：随着虚拟数字人和元宇宙概念的兴起，\
高质量、可定制的语音合成成为构建沉浸式虚拟交互体验的关键技术。"""),

    ("挑战与未来展望",
"""尽管神经网络TTS取得了显著进展，仍面临以下挑战：

（1）鲁棒性问题：自回归TTS模型中的注意力机制容易出现对齐失败，导致单词跳过或重复。\
非自回归模型（如FastSpeech、VITS）基本解决了这一问题，但可能在表达力上有所牺牲。

（2）韵律自然度：虽然语音质量已大幅提升，但生成真正具有人类级韵律的语音——\
特别是对于有声书等长篇内容或情感细腻的对话——仍然具有挑战性。\
韵律预测误差会在长话语中累积。

（3）推理效率：虽然FastSpeech和HiFi-GAN能够实现实时合成，\
但最新的基于大语言模型的TTS方法（如VALL-E、Bark）需要大量计算资源。\
如何在质量、延迟和成本之间取得平衡是活跃的研究方向。

（4）低资源语言：大多数TTS研究集中在英语和中文等高资源语言上。\
将高质量TTS扩展到世界上数千种低资源语言需要跨语言迁移学习、多语言预训练和少样本/零样本方法。

（5）多模态融合：TTS越来越多地集成到多模态系统中（文本到视频、虚拟数字人、具身智能体），\
需要实现语音与面部动画、手势和唇形的同步。

展望未来，基于大语言模型的TTS方法将继续发展，零样本合成能力将进一步增强。\
扩散模型和流模型为质量与多样性的平衡提供了新思路。\
同时，语音合成的安全性和伦理问题将受到越来越多的关注，\
相关技术标准和法规也将逐步完善。"""),

]

conclusion = """语音合成技术经过数十年的发展，已经从早期的规则驱动方法演进到数据驱动的神经网络方法，\
合成语音的质量从明显的"机器音"提升到了接近人类语音的水平。

本文系统回顾了语音合成技术的发展历程：从拼接合成和共振峰合成等传统方法，\
到基于HMM的统计参数合成方法，再到以WaveNet、Tacotron 2、FastSpeech、VITS为代表的神经网络端到端方法。\
特别地，WaveNet开创了神经声码器的研究范式，Tacotron 2实现了端到端TTS的人类级质量，\
FastSpeech解决了推理效率和鲁棒性问题，VITS实现了完全端到端的高质量合成。

在前沿方向上，基于扩散模型的TTS方法为多样性和质量的平衡提供了新思路，\
基于神经编解码器语言模型的方法（如VALL-E）将TTS推向了零样本合成的新范式。\
韵律建模、多说话人合成和语音克隆等技术也在不断取得突破。

然而，语音合成技术仍面临鲁棒性、韵律自然度、推理效率和低资源语言等挑战。\
随着深度学习技术的持续进步和计算资源的不断提升，\
我们有理由期待语音合成技术将在更多场景中实现真正自然、表现力丰富的人机语音交互。\
同时，语音合成技术的伦理和安全问题也需要得到充分重视，以确保技术的健康发展。"""

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
    'Wang C, Chen S, Wu Y, et al. VALL-E 2: Neural codec language models are human parity zero-shot text to speech synthesizers[J]. arXiv preprint arXiv:2406.05370, 2024.',
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

# ===== 生成报告 =====
output_file = '人工智能基础_语音合成技术综述报告.docx'
create_report(
    title=title,
    subtitle=subtitle,
    course_name=course_name,
    abstract=abstract,
    keywords=keywords,
    sections=sections,
    conclusion=conclusion,
    references=references,
    output_filename=output_file
)

print("TTS报告生成完成！")
