---
tags: 自动驾驶
---



驾驶辅助产品装车量达到 <hu>100 万辆</hu>，积累 <hu>100 万公里</hu>的真实数据。

#### 云 + 端架构

* 云端大模型 <hu>Fundamental Model</hu>：基于 Transformer 的全任务感知大模型
* 车端小模型 <hu>Domain Model</hu>：通过灰度测试的模式感知环境信息，可能遗漏很多高价值场景
* 通过云端大模型对比验证车端模型的判断结果，找到有用数据补充样本，训练现有模型

#### 无监督聚类

* 在百万公里真实数据通过无监督聚类找到更多相似数据
* 在聚类结果中找到正样本和负样本
* 挑选类中心和类边界附近的数据出来提升标注效率

#### Swin-Transformer

* <hu>Transformer</hu>
  * 利用自注意力机制捕获全局上下文信息，对目标建立起远距离的依赖
* <hu>Swin-Transformer</hu>
  * 通过小图像片元和逐层进行邻域合并的方式构建层级特征表达，将自注意力限制在一定范围内

#### CSS+ ICU 3.0

* 语义场景的自动化转化工具和参数泛化工具可以将 CSS 中场景库的描述文本自动转化为仿真测试场景，并且在合适的范围内离散采样得到巨量的仿真测试用例。通过在云端并行，每天可以自动生成一万多个仿真测试用例
* 自动驾驶计算平台 ICU 3.0 采用<hu>高通 8540+9000</hu> 芯片，单卡算力 360 TOPS，可扩展到 <hu>4 卡 1440 TOPS</hu>。 

[原文](https://www.jiqizhixin.com/articles/2021-09-29-9)

