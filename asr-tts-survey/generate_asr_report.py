#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成机器学习大作业报告：自动语音识别技术综述（ASR）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_report import create_report

# ===== 报告内容 =====

title = "自动语音识别技术综述"
subtitle = "——从传统GMM-HMM到端到端深度学习模型的演进"
course_name = "机器学习"

abstract = """自动语音识别（Automatic Speech Recognition, ASR）是机器学习领域的重要研究方向，\
旨在将语音信号自动转换为对应的文本序列。本文系统综述了ASR技术的发展历程，\
从早期的动态时间规整（DTW）方法，到基于高斯混合模型-隐马尔可夫模型（GMM-HMM）的经典方法，\
再到以深度神经网络为核心的现代端到端方法。重点介绍了深度神经网络-隐马尔可夫模型（DNN-HMM）混合系统、\
基于连接主义时间分类（CTC）的模型、基于注意力机制的编码器-解码器模型、\
循环神经网络变换器（RNN-T/Transducer）以及Conformer架构等代表性工作。\
同时讨论了wav2vec 2.0、HuBERT等自监督预训练方法和Whisper等大规模弱监督模型的最新进展，\
并对ASR技术的未来发展趋势进行了展望。"""

keywords = ["自动语音识别", "深度学习", "端到端模型", "自监督预训练", "Conformer"]

sections = [
    ("引言",
"""自动语音识别（Automatic Speech Recognition, ASR）技术是人工智能和人机交互领域的核心研究方向之一，\
其目标是将输入的语音波形信号自动转换为对应的文本序列。\
高质量的ASR系统在智能语音助手、自动转写、实时字幕、呼叫中心分析、医疗/法律记录等众多应用场景中具有广泛的实用价值。

从技术发展的时间线来看，ASR技术经历了四个主要阶段：（1）基于模板匹配的方法（1960s-1980s），\
（2）基于统计模型的GMM-HMM方法（1990s-2010s），（3）深度神经网络与HMM的混合方法（2012-2017），\
（4）端到端深度学习方法（2015至今）。每一次技术范式的转变都显著提升了识别的准确率和鲁棒性。

近年来，随着深度学习技术的快速发展，特别是自监督预训练和大规模弱监督学习方法的出现，\
ASR系统的性能已经接近甚至达到了人类水平。以Whisper[1]、wav2vec 2.0[2]、Conformer[3]为代表的一系列工作，\
不断刷新着语音识别的性能上限。本文旨在对ASR技术的发展脉络进行全面梳理，\
重点分析各阶段的代表性方法和技术特点，并对当前的研究热点和未来发展方向进行讨论。"""),

    ("传统语音识别方法",
"""## 2.1 动态时间规整方法

动态时间规整（Dynamic Time Warping, DTW）是最早被应用于语音识别的方法之一。\
DTW通过动态规划算法计算测试语音与参考模板之间的最优时间对齐距离，从而实现语音模式的匹配。\
Sakoe和Chiba[4]于1978年提出了基于DTW的语音识别优化方法，成为该领域的经典工作。

DTW方法的优点是概念简单、易于实现，适用于小词汇量的孤立词识别。\
但其局限性也很明显：需要为每个词存储参考模板，计算复杂度随词汇量增长而急剧增加，\
且对说话人变化和环境噪声的鲁棒性较差。

## 2.2 基于GMM-HMM的经典方法

高斯混合模型-隐马尔可夫模型（GMM-HMM）框架是统计语音识别的经典范式，自1990年代起主导了ASR领域长达二十年。\
在该框架中，HMM对语音信号的时序动态特性进行建模，每个HMM状态的发射概率由GMM表示。

Rabiner[5]于1989年发表了HMM的经典教程，系统总结了HMM在语音识别中的应用。\
该方法的核心流程包括：（1）特征提取——将原始语音转换为MFCC或Fbank等声学特征；\
（2）声学建模——使用GMM对每个HMM状态的声学特征分布进行建模；\
（3）解码——使用维特比算法搜索最可能的词序列；\
（4）语言模型——通过N-gram语言模型对候选词序列进行重排序。

GMM-HMM方法的代表性工具包包括HTK和Kaldi。\
尽管该方法在大规模语音识别任务上取得了显著成功，但GMM的表达能力有限，\
难以捕捉声学特征中的复杂非线性关系，且特征工程和模型调参需要大量专业知识。"""),

    ("深度学习在语音识别中的应用",
"""## 3.1 DNN-HMM混合系统

2012年，深度学习技术的引入彻底改变了语音识别的格局。\
Hinton等人[6]提出使用深度神经网络（DNN）替代GMM来估计HMM状态的发射概率，\
开创了DNN-HMM混合系统的研究范式。

Dahl等人[7]将DNN应用于大词汇量连续语音识别，展示了深度学习在ASR中的巨大潜力。\
Seide等人[8]在Switchboard数据集上首次展示了DNN-HMM系统相对于GMM-HMM系统的显著性能提升。\
随后，卷积神经网络（CNN）[9]和长短时记忆网络（LSTM）[10]被相继引入ASR领域，\
进一步提升了声学建模的能力。特别是双向LSTM（BLSTM）结合CTC损失函数的方法，\
成为深度学习ASR的主流架构之一。

## 3.2 端到端模型：CTC方法

连接主义时间分类（Connectionist Temporal Classification, CTC）由Graves等人[11]于2006年提出，\
是一种直接对输入序列和输出序列之间的对齐关系进行建模的损失函数。\
CTC引入了"空白"（blank）符号，允许模型在输入和输出长度不一致时进行端到端训练。

Hannun等人[12]于2014年提出了Deep Speech，这是第一个大规模端到端CTC语音识别系统。\
Amodei等人[13]于2016年进一步提出了Deep Speech 2，在英语和中文上均取得了当时最优的识别性能，\
证明了端到端深度学习方法可以媲美甚至超越传统流水线方法。

## 3.3 端到端模型：注意力机制方法

注意力机制（Attention Mechanism）由Bahdanau等人[14]于2015年在机器翻译领域提出，\
随后被引入语音识别。Chan等人[15]于2016年提出了Listen, Attend and Spell（LAS），\
这是第一个基于注意力机制的端到端ASR模型。

LAS由"监听器"（Listener）和"拼写器"（Speller）两部分组成：\
监听器是一个金字塔双向LSTM编码器，将声学特征编码为高级表示；\
拼写器是一个基于注意力的LSTM解码器，直接输出字符序列。\
LAS消除了对发音词典、语言模型和HMM的依赖，实现了真正的端到端识别。

然而，注意力机制在处理长序列时容易出现对齐错误，导致识别结果不稳定。\
为此，研究者们提出了多种改进方案，包括单调注意力（Monotonic Attention）和硬注意力（Hard Attention）等。

## 3.4 端到端模型：RNN-T/Transducer方法

RNN变换器（RNN-Transducer, RNN-T）由Graves[16]于2012年提出，\
是对CTC框架的重要扩展。RNN-T由三个组件构成：\
（1）编码器（Transcription Network）——处理声学特征；\
（2）预测网络（Prediction Network）——建模输出标签之间的依赖关系（类似于语言模型）；\
（3）联合网络（Joint Network）——结合编码器和预测网络的输出，产生输出标签和空白符号的概率分布。

与CTC不同，RNN-T能够建模输出标签之间的相互依赖关系，这使得它在实际应用中表现出更好的性能。\
RNN-T已被广泛应用于Google、Apple等公司的生产级语音识别系统中，成为端到端ASR的主流架构之一。

## 3.5 Conformer架构

2020年，Gulati等人[3]提出了Conformer（Convolution-augmented Transformer），\
将自注意力机制和卷积操作结合在单个编码器块中。Conformer块采用"Macaron"结构，\
用两个前馈模块夹住多头自注意力模块和卷积模块。

Conformer的核心思想是自注意力和卷积是互补的：\
自注意力擅长捕捉全局依赖关系，而卷积擅长学习局部特征。\
两者结合后，Conformer在LibriSpeech基准测试上取得了当时最优的识别性能，\
WER（词错误率）在test-clean/test-other上分别达到1.9%/3.9%（不使用语言模型）。\
Conformer已成为现代ASR系统的标准编码器架构。"""),

    ("自监督预训练方法",
"""## 4.1 wav2vec 2.0

wav2vec 2.0由Baevski等人[2]于2020年提出，是一种自监督语音表示学习框架。\
该方法的核心思想是对原始音频进行掩码预测：使用CNN特征编码器和Transformer编码器处理语音信号，\
对潜在语音表示进行掩码，并通过对比损失学习量化表示。

wav2vec 2.0的关键创新在于：仅需10分钟的标注数据即可在LibriSpeech上取得有竞争力的识别性能，\
同时利用约53,000小时的无标注音频进行自监督预训练。\
这一工作开创了"预训练+微调"的语音识别新范式，极大地降低了对标注数据的依赖。

## 4.2 HuBERT

HuBERT（Hidden-Unit BERT）由Hsu等人[17]于2021年提出，\
是一种受BERT启发的自监督语音表示学习方法。HuBERT使用离线聚类生成伪标签（隐藏单元），\
并以掩码预测的方式进行训练。随着模型的改进，聚类质量也在迭代中不断提升。

HuBERT在多个语音任务（ASR、说话人识别、情感识别等）上取得了最优结果，\
证明了掩码预测与聚类分配相结合的方法在语音表示学习中的有效性。\
HuBERT与wav2vec 2.0和WavLM[18]一起，成为自监督语音表示学习的基础模型。

## 4.3 WavLM

WavLM由Chen等人[18]于2022年提出，通过在预训练中引入去噪目标，\
增强了模型对噪声和说话人变化的鲁棒性。WavLM在SUPERB基准测试中表现出色，\
特别是在说话人相关任务上展现了强大的能力。

## 4.4 自监督预训练的意义

自监督预训练方法的意义在于：（1）大幅降低对标注数据的依赖，使得低资源语言的ASR成为可能；\
（2）学习到的语音表示具有良好的通用性，可迁移到多种下游任务；\
（3）为大规模语音基础模型的构建奠定了基础。"""),

    ("大规模弱监督模型：Whisper",
"""Whisper由Radford等人[1]于2022年提出，是OpenAI开发的通用语音识别模型。\
Whisper在680,000小时的多语言和多任务监督数据上训练，这些数据通过弱监督方式从互联网上收集。

Whisper的核心特点包括：（1）大规模、多样化的训练数据带来了强大的泛化能力，\
在多个数据集和领域上往往与专门训练的模型具有竞争力；\
（2）支持多语言语音识别、语音翻译、语种识别和语音活动检测等多种任务；\
（3）模型规模从Tiny（约39M参数）到Large（约1.55B参数）不等，支持不同计算资源条件下的部署。

Whisper的出现标志着语音识别进入了一个新的时代：通过大规模弱监督学习，\
可以构建通用的、鲁棒的语音识别系统，而无需针对每个领域或语言进行专门的数据收集和模型训练。\
这一范式对ASR的研究和应用产生了深远的影响。"""),

    ("当前研究趋势",
"""## 6.1 语音基础模型

随着大语言模型（LLM）的成功，语音领域也在探索基础模型（Foundation Model）的概念。\
Bommasani等人[19]提出的基础模型概念正在语音领域得到实践：\
通过在海量语音数据上进行大规模预训练，构建可以适配多种下游任务的通用语音模型。

代表性的语音基础模型包括HuBERT、WavLM、Whisper以及Meta的MMS（Massively Multilingual Speech）[20]。\
MMS在1,000多种语言上训练了语音识别和语音合成模型，极大地扩展了语音技术的语言覆盖范围。

## 6.2 多语言ASR

多语言ASR旨在构建能够处理多种语言的统一识别系统。\
传统方法需要为每种语言单独训练模型，而现代方法通过共享编码器和多语言训练，\
实现了跨语言的知识共享和迁移。Whisper和MMS是多语言ASR的代表性工作。

## 6.3 流式ASR与设备端部署

实时语音识别（Streaming ASR）要求模型在语音输入的同时进行识别，不能等待完整话语结束。\
这需要特殊的模型架构设计，如单向编码器、块式处理（Chunked Processing）和前瞻限制（Look-ahead Limiting）。\
同时，在移动设备和嵌入式设备上部署ASR模型需要考虑计算资源、内存和功耗的限制，\
模型压缩、量化和知识蒸馏等技术被广泛应用。

## 6.4 抗噪鲁棒性

真实应用场景中的语音信号通常受到背景噪声、混响、回声等干扰。\
提升ASR系统的抗噪鲁棒性是重要的研究方向，常用的方法包括数据增强（加噪、混响模拟）、\
多条件训练、波束形成前端处理以及自监督预训练中的去噪目标（如WavLM）。"""),

    ("应用场景",
"""自动语音识别技术在众多领域具有广泛的应用价值：

（1）智能语音助手：Siri、Alexa、Google Assistant等语音助手的核心就是ASR系统，\
将用户的语音指令转换为文本以便后续的自然语言理解和任务执行。

（2）自动转写服务：会议记录、讲座笔记、采访转写等场景中，\
ASR技术可以大幅提高文字记录的效率。代表性产品包括Otter.ai、讯飞听见、阿里云语音转写等。

（3）实时字幕：视频会议、直播、电视节目等实时场景中，\
ASR技术可以生成实时字幕，提升信息获取的便利性和无障碍性。

（4）呼叫中心分析：ASR技术用于将通话录音转换为文本，\
支持通话质量监控、客户情感分析、关键词检测等应用。

（5）医疗/法律记录：在医疗问诊和法律庭审等专业场景中，\
ASR技术可以辅助专业人员进行记录和文档整理，提高工作效率。

（6）语音搜索与输入：ASR技术使得用户可以通过语音进行搜索和文字输入，\
在驾驶、烹饪等双手不便操作的场景中尤为实用。"""),

    ("挑战与未来展望",
"""尽管深度学习ASR取得了显著进展，仍面临以下挑战：

（1）噪声鲁棒性：在高噪声环境（如嘈杂的街道、工厂车间）中，ASR系统的性能会显著下降。\
尽管数据增强和抗噪训练有所帮助，但在极端噪声条件下的识别仍然是一个开放问题。

（2）口音和方言处理：不同说话人的口音、方言和个人发音习惯对ASR系统构成了挑战。\
构建能够泛化到各种口音的统一模型需要大规模、多样化的训练数据。

（3）代码混合（Code-Switching）：在多语言环境中，说话人经常在同一句话中混合使用多种语言。\
代码混合ASR需要模型能够无缝处理语言切换，这对传统的单语言模型提出了挑战。

（4）长音频处理：处理数小时的长音频（如会议录音、播客）时，\
模型的计算复杂度和内存需求会急剧增加，且上下文信息的建模也更加困难。

（5）计算效率：虽然Whisper等大模型性能优异，但其推理成本较高，\
难以在资源受限的设备上实时运行。如何在性能和效率之间取得平衡是重要的研究方向。

展望未来，ASR技术将在以下方向继续发展：\
（1）语音基础模型将变得更加强大和通用，能够处理更多语言和任务；\
（2）端到端模型将与大语言模型深度融合，实现语音理解和生成的统一；\
（3）自监督预训练方法将进一步降低对标注数据的依赖，使得低资源语言的ASR成为可能；\
（4）多模态融合（音频+视觉+文本）将为ASR提供更丰富的上下文信息；\
（5）隐私保护和联邦学习将在ASR训练和部署中发挥越来越重要的作用。"""),

]

conclusion = """自动语音识别技术经过数十年的发展，已经从早期的模板匹配方法演进到基于深度学习的端到端方法，\
识别准确率从早期的有限词汇量孤立词识别提升到了接近人类水平的连续语音识别。

本文系统回顾了ASR技术的发展历程：从基于DTW的模板匹配方法，到基于GMM-HMM的经典统计方法，\
再到以DNN-HMM混合系统、CTC模型、注意力机制模型和RNN-T为代表的端到端深度学习方法。\
特别地，DNN-HMM混合系统开创了深度学习在ASR中的应用，\
CTC和RNN-T实现了真正的端到端训练，Conformer架构将自注意力和卷积的优势相结合，\
成为现代ASR系统的标准编码器。

在自监督预训练方面，wav2vec 2.0、HuBERT和WavLM等方法通过在大量无标注数据上进行预训练，\
大幅降低了对标注数据的依赖，为低资源语言的ASR提供了新的解决方案。\
Whisper通过大规模弱监督学习，构建了通用的、鲁棒的语音识别系统，\
标志着ASR进入了基础模型时代。

然而，ASR技术仍面临噪声鲁棒性、口音处理、代码混合和长音频等挑战。\
随着深度学习技术的持续进步和计算资源的不断提升，\
我们有理由期待ASR技术将在更多场景中实现真正鲁棒、高效的人机语音交互。\
同时，语音基础模型的发展将进一步推动ASR技术的通用化和民主化，\
使得高质量的语音识别能力惠及更多语言和应用场景。"""

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
    'Watanabe S, Mandel M, Barker J, et al. CHiME-6 challenge: Tackling multispeaker speech recognition for unsegmented recordings[C]. CHiME Workshop, Barcelona, Spain: ISCA, 2020.',
    'Panayotov V, Chen G, Povey D, et al. LibriSpeech: An ASR corpus based on public domain audio books[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Brisbane, Australia: IEEE, 2015: 5206-5210.',
    'Bu H, Du J, Na X, et al. AISHELL-1: An open-source Mandarin speech corpus and a speech recognition baseline[C]. Oriental COCOSDA, Seoul, South Korea: IEEE, 2017: 1-5.',
    'Xu Q, Baevski A, Likhomanenko T, et al. Self-training and pre-training are complementary for speech recognition[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Toronto, Canada: IEEE, 2021: 3030-3034.',
    'Synnaeve G, Xu Q, Kahn J, et al. End-to-end ASR: From supervised to semi-supervised learning with modern architectures[C]. ICML Workshop on Self-Supervised Learning for Speech and Audio Processing, Virtual: PMLR, 2020.',
    'Li B, Gulati A, Yu J, et al. A better and faster end-to-end model for streaming ASR[C]. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Toronto, Canada: IEEE, 2021: 5654-5658.',
    'Park D S, Zhang W, Jia Y, et al. SpecAugment: A simple data augmentation method for ASR[C]. Interspeech, Graz, Austria: ISCA, 2019: 2613-2617.',
    'Ko T, Peddinti V, Povey D, et al. Audio augmentation for speech recognition[C]. Interspeech, Dresden, Germany: ISCA, 2015: 3586-3589.',
]

# ===== 生成报告 =====
output_file = '机器学习_自动语音识别技术综述报告.docx'
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

print("ASR报告生成完成！")
