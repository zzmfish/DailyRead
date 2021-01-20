2021年1月18日 星期一

## Mobileye REM地图如何解决高精地图落地难点？

#### 高精地图的挑战

**规模化**

2025年之后，自动驾驶会在消费者层面全面落地，Scale是一个无法规避的问题

**鲜度**

理想情况下，地图是在实时更新的

**精度**

车载系统(OnBoard System)检测的车辆和行人需要与高精地图(High Definiation Map)实现厘米级精度的匹配




#### 通用高精地图制作方法的缺陷

**全局坐标系下厘米级精度不是必需的**

**语义层数据生产难以自动化**

* 没有车道线
* 转向规则
* 红绿灯
* Stop/Yield Point
* 道路几何、限速、文化



#### Mobileye如何解决这些问题

* 从成百上千辆车获取`检测信息并传送`到云端
* 将每辆车的数据进行`Alignment处理`，生成高精度的地图数据
* 生成地图的`语义数据`

![图片](https://mmbiz.qpic.cn/mmbiz_png/hcvXjXPVObrRE1hMbFh68bv3ZqljkL13gHVusTvAia4GyEZMQAVAdf7AKrA9iaWslGOfGkgSzGALqZIXTicGMTRAQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)


##### Harvesting

车辆检测`landmarks`、`lane marks`、`driving path`等语义信息。

成百上千的过路车辆会让检测结果越来越好。

##### Alignment

检测每个RSD中每个元素的6D Pose，然后`对齐相同位置的元素`，得到`厘米度精度`的driving path等信息。

每个车辆检测的道路元素位置都存在噪声，不能只依靠简单的求均值，而是依靠**几何运算**。

##### Modeling & Semantics

使用**神经网络**



#### 为什么语义理解离不开众包

* 可以在没有Lane Marking的道路上获取Driving Path

* 众包数据提供了复杂场景下的所有可通行路径

* 获得红绿灯与车道的关联关系、Yield Sign的Stop Point、Crosswalk与红绿灯的关联关系等
* 到没有Traffic Sign情况下各个道路的路权优先级

* 路口其它司机的停车位置
* 在无保护左转的场景下车辆的Stop Point
* 获得各个道路Common Speed的唯一高效的方法



#### 总结

* Mobileye与超过`6家汽车制造厂商`合作
* 每天覆盖`800万公里`的路网更新
* 预计到2024年，每天覆盖的路网会达到`10亿公里`



[阅读原文](https://mp.weixin.qq.com/s/P-InX0BuLp1UIkuSFAyUBA)