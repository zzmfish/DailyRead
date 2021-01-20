---
layout: post
title:  "PonyAI技术解读：自动驾驶中轨迹规划的探索和挑战.md"
---

## PonyAI技术解读：自动驾驶中轨迹规划的探索和挑战

#### 轨迹规划基本介绍


###### 轨迹规划的概念

核心是`解决车辆该怎么走的问题`

输入

* 拓扑地图
* 障碍物
* 障碍物的预测轨迹
* 交通信号灯的状态
* 定位
* 导航
* 车辆状态

输出是一个**轨迹**，是`时间到位置的函数 t→(x,y,z)`



###### 非凸优化问题
约束

* 遵守交规
* 避免碰撞
* 在车辆控制上可实现



目标：使得自动驾驶跟人类司机驾驶相似



**凸优化问题**是指一个问题如果有两个可行解，则要满足这两个可行解的线性组合也是可行的，且不比这两个可行解都差。

轨迹规划不是一个凸优化问题呢。



#### 为什么需要决策模块
###### 决策

* 限定非凸问题（轨迹规划）的解空间，将问题转化为凸的
* 使解更加稳定
* NP-hard（非确定性多项式困难）问题



需要决策的场景

* 抢行还是让行
* 是否要冲黄灯
* 在哪两辆车之间变道、并线
* 是否要主动变道
* 是从左还是右绕行前方障碍物



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vpZmM8j3lx85tEoQoFDusBdYHf8vO2s4GhLmmSGpic5vyUWmImogTzfQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



处理凸问题可以利用的快速算法有许多，线性规划，二次规划，序列二次规划……这些都是数值求解优化问题的方式。例如在二次规划中，如果Q正定，二次规划就是凸的问题，求解它会更加迅速和容易。



**纵向规划决策求解：动态规划**

**
**

在纵向规划决策上，我想介绍一种以动态规划算法作为决策的方法。



看看下图的案例，假设有两个人正在横穿马路，我们来研究一下如何决策才是最优的选择。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vSAFELNtKXvOiaan2IdepOJRFTzvMhPf18kvIYBaXevDfeNuBFC62rjg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

首先，将t - s图进行离散化，离散化之后，我们可以认为每一步的决策只与前边的两步有关系。两步是因为我们可以近似求出加速度，并能写出一个状态转移方程。



尽管这个方程在实际过程中比较难写，但确实是一种做法。虽然离散化t和s降低了精度，但降低精度也帮助降低了运行时间。



注意，这种方法并不能保证最后的速度是否舒适，它给出的是一个大概的决策方法，即到底让或者不让。



**决策面临的挑战**



第一个挑战上面已经提到，由于决策问题是一个NP-hard问题，不易直接求解，存在多种多样的近似算法。



第二个挑战是很难用规则去拟合人的经验，包括上述的状态转移方程中的cost也很难去表示。目前解决这个挑战可用的部分办法是根据各种不同的情况建立数学模型，以及采用机器学习的方法进行决策。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vby1KaaAhcgYYlV6kzWjVqTjzeOGC8tqXYjpw0wLYcMibzxltVfEZVNA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



以上图左侧的场景为例，一辆正在行驶的自动驾驶车辆打算绕行前面白车，但此时前车突然起步了，我们该如何继续行驶？是变道？还是跟在后边行驶，又或是继续绕行？处理这种情况确实依靠人类驾驶的经验。



再看上图右侧的例子：自动驾驶车准备在前方左转，但是前车停了很久也没有启动（可能前车驾驶员没反应过来），我们这时该不该变道呢？对这种情况，人类司机有时也很难判断。由此可见，场景的多变而复杂使得决策面临很多挑战。



***3***

## **横向规划**

## 



**横向规划的解法**



前面提到轨迹规划可以拆成横向和纵向的规划，现在我来具体介绍横向规划的解法。**横向规划就是行车方向上的规划，可以看成是如何打方向盘的规划，它决定了轨迹的形状。**



这个问题通常的解法分两种，一种是无车道的场景，比如在freespace（自由空间）中规划或者泊车之类的场景，车辆一般处在低速行驶状态，缺乏车道线等先验信息。业界大多都用搜索等路径生成的方式去处理无车道场景。



另一种是有车道的情况。虽然可以参考车道线信息，但是规划上想输出s→(x,y)函数，难度并不小。常见的做法是离线生成参考线，随后就可以将求解s→(x,y)的问题变为求解s→l的问题，l是指车辆在这个参考线上的横向偏移量。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vicsEgqOuUpBX4zTb52W0bzquaoVQt1zVUNbnYgNCo8OHAJxqkaP65XQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



以上图右侧场景为例，原本车是沿车道向前走，但由于有前方车辆的遮挡，我们就必须绕行它，即向右横向偏移。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vpkhKMabdQgy33Eu8Wqe7Yyn1RwZB957vicK5U1WqRdq2n3yYfF53TXg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



而参考线的生成，其实类似于开卡丁车时别人教你的过弯的最优路线，它也是一个优化问题，当然也要保证安全性和舒适性。方便的是，有了高精地图辅助后，参考线可以通过离线去进行，所以可以用一些开销比较大的算法做到最优。参考线的约束在于其需要在车道线内，并且在控制上可实现。优化目标则是参考线需接近车道中心，曲率不能太大，曲率变化率也不大。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4v2ia3fs7qrvlibfHyjIdiaNRKwjwPPwWoD4ITdn3ib8JWCKkKPxQLt15Pibg/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



确定参考线后，通过把参考线离散化，采一些点出来，那么横向规划问题就转化为求解一个离参考线偏移距离的一个问题，即转化成s→l的问题。其约束是车辆行驶不跨越边界，避免碰撞，而优化的目标是要离参考线近，要离障碍物远，曲率不大，曲率变化率不大等等。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vlFAGK8iaQeG2foARUPnR2kZOOfxWDoC4tgoLsHoHTPyzmS6pBduvRiaA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



借助上图右侧的例子，你会发现横向规划可看成一个二次规划（QP）的问题。其中“0”，“-1”，“-2”是自动驾驶车行驶过的路径，0号点是车当前的位置，现在我们需要解的就是1，2，3，4，5，6这些点相对于参考线的横向偏移x。换句话说，已知x[-2]，x[-1]，x[0]，求解x[1]，x[2]等。



该函数约束是车辆行驶不能超过左右边界包括马路牙，实线，障碍物等。优化目标则是车辆要离参考线近，方向盘不能打太多太快，保证乘坐的舒适。上图中的公式其实是一个关于x的二次的形式，所以可以使用二次规划的方法来解决。



**横向规划的挑战**



虽然大部分时候车都行驶在有车道线的马路上，但也会面临特殊的挑战。例如下图里左侧显示的路口，我们的车行驶的方向上有三条直行车道，但过路口后变成四条直行车道，并且对得很不齐。现实中，右侧的行驶的车（白车）往往不依据车道线行驶，可能会横跨车道线挤占自动驾驶车辆所在车道的空间。



而下图右上角则展示了没有车道线的主辅路场景。在这种主辅路之间切换，就像解决一种没有参考线的freespace的规划，挑战也不小。总的来说，要想解决没有车道线或者说普通车辆不按车道线行驶的路径规划问题，难度都不小。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vDeuXE4mlqeTk3nyU2v0hciaCMhviby2R3JmXuoQokPNVOmNeaW2j95DA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



另外的挑战就是环境的问题，因为车外行驶环境瞬息万变，要对周围进行环境预测也很困难。以下图为例，我们的自动驾驶车准备往左变道，而左下角橙色块代表的摩托车正飞速地向前行驶，于是我们的车辆迅速给出取消变道的决策，生成平滑的曲线回到原来行驶的道路上。因此，面对这类的情况，轨迹规划模块需要保证规划的路径光滑且在控制上可实现。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vCC5auggzsda8CCp3icrXxYYllUyQJ9oF7GE4ULtvVnnDjQE6WKU1smQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



***4\***

**纵向规划
**



**纵向规划的定义和场景**



**纵向规划本质是对车辆在设定好的路径上的速度规划，决定了车辆在整个轨迹上的运动过程。**

**
**

求解这类优化问题，第一个约束是遵守交规（信号灯、限速、停车让行等），第二个约束是避免碰撞。而纵向规划的优化的目标是乘坐舒适，也意味着车辆的速度变化率不大，加速度变化率不大，行驶速度也要尽量快一点（限速内）等。



前边我提到了行人横穿马路的场景，在t - s图中，行人的运动过程可以转化一个矩形，最终给出了两种车辆的对应决策——加速超过行人或减速让行。那么决策之后该怎么做呢？



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vjJ2o3t2kZrjV0EHhphPJwVclQhXtjsvgZsAb1mdNaPzMdfsbzvQiaiaQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



如果决定要抢行，我们可以将矩形的约束条件扩展到最下部，便能转化为凸问题求最优解。如果采取避让，车辆的路线则从t - s图中的矩形下边穿过。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vpaYyWGB7cibYKtLZJucSbumIje87ExLkDFOXmwDp1S28tr2DhKND3DA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



但是如果是行人斜着穿过马路呢？在t - s图中，行人的运动过程又该如何表示？答案就是一个斜向上的平行四边形（如上图）。



黄灯也是我们要应对的场景之一。黄灯即将到来，如果决策要冲，那么车辆须尽快通过路口，否则很容易被逼停在路中间出不去。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vvwUOD2AEamkA4215GPYtU4R6cnlnB9ibMC6bdcbsr0x9sAHBtVSvahQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



这种情况我们也可以用一样的t - s图表示（上图），左边界是表示黄灯亮的时刻，这个白色矩形存在一个缺角。当黄灯亮起的时候，车辆如果要尽快通过路口，那么随着t在增大的过程中，s也要迅速增大，并且增大的速率要超过缺角的斜率。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4v7XQbwXiaaY0PbCdWCoNG9l5EbBjK5BlDrBicd7wLhWbuE4iat7kNayJfQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



再看一些更有趣的场景案例（上图）。当自动驾驶车跟车时，假设所跟的前车在减速，如果能够精确预测前车的运动的状态，那么展现在t - s图中的白色部分会出现各种各样的形状，这样解优化问题就能解出一条好的速度曲线。



**纵向规划的挑战**



纵向规划会面临什么挑战呢？



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vTozKutWf70huA44jpicyZFpK0rY0TVrkua9mtLfPrTXER3GXfrhdomw/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



首先存在**博弈的挑战**。以上图为例，自动驾驶车前方的左转绿灯亮起并准备左转，这时，一辆电动车突然出现在左前方，准备快速横穿马路。



这种情况，人类驾驶员会怎么开呢？人类司机会和电动车司机迅速对一下眼神，通过眼神比较气势谁猛，另一方就会主动地让对方。当然这有开玩笑的成分。



但在决策上这个场景并不好处理，它是一个博弈的过程，自动驾驶车不能一开始就决定无视还是让步，所以在很多时候要在激进和保守之间掌握一个平衡点，这需要不同的参数和不同的模式去处理不同场景。



除此之外，感知和预测带来的困难也会使纵向规划面临挑战。



可以看下图中右上方连续两张相似的图，在第二张图里你会发现有人突然从车前冲出来，俗称叫做“鬼探头”，也就是盲区。对于这种情况，感知需要提前检测到盲区，车辆进行减速，规避可能的安全隐患。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vxVW5eCgRPO2HNZiaE0zsMVL66let0iacsnficKGibSf289wwlttZtquqGA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



预测给规划带来的挑战出现在左下角（上图）的场景里。此时，自动驾驶车的右前方行驶着一辆面包车，面包车前边有一辆速度很慢的自行车，一般人类司机会主动预测面包车极有可能向左变道。但这类场景对预测模块提出了很大的挑战，如果缺乏这类预测，自动驾驶车辆的后续应对同样挑战不小。



![图片](https://mmbiz.qpic.cn/mmbiz_jpg/6PYxCJZfNqdTEGtX6DpdLkzLnTGvgY4vpIrtWO57kor1jIibIStJ6Td18OSvo0R2J5BvKlqRzJNclYckC5o0muA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)



自动驾驶还有一些极端的情况，需要考虑到横纵向协调配合。上图是一个非常极限的车辆加塞案例：自动驾驶车正在高速行驶时，右侧的一辆慢车突然加塞，一般人类司机会选择打方向避让，如果当时左车道没有车，甚至会向左变道，如果左车道有车，他也会扭一点方向进行避让。



这类处理就需要横纵向规划的配合，共同解决极端情况。比如从纵向规划来说，当时已经无法保持安全车距，规划需要做到的是保证不相撞，并尽快拉开车距，而不是一脚刹到底。