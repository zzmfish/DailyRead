---
layout: posts
title: 百度Apollo：Cyber RT简介
tags: 自动驾驶
header: 
  image: "http://zhouzm.cn/images/%E7%BE%8E%E5%9B%BE/210526%E6%A9%99%E5%AD%90.jpg"
---


## ROS 应用于自动驾驶的不足

独立进程的节点的 **运行顺序无法确定**；

分布式系统存在 **通信开销**

<center>💮💮💮</center>

## Cyber RT 框架

#### 🚘 基础库

高性能；无锁队列

#### 🚘 通信层

Publish/Subscribe 机制；

Service/Client 机制；

服务自发现；

自适应的通信机制：共享内存、Socket、进程内存

#### 🚘 数据层

数据缓存与融合

#### 🚘 计算层

计算模型；

任务以及任务调度

![](http://zhouzm.cn/DailyRead/assets/images/210526-CyberNode.png)

<br>

<center>💮💮💮</center>

## 运行流程

![](http://zhouzm.cn/DailyRead/assets/images/210526-CyberTask.png)

#### 🚘 算法模块

通过 **有向无环图（DAG）** 配置任务间的逻辑关系；

每个算法可以进行 **优先级、运行时间、使用资源** 等方面的配置

#### 🚘 创建任务

结合DAG、调度配置创建任务；

内部 **协程（coroutine）**

#### 🚘 调度器

把任务放到各个  **Processor队列**

#### 🚘 数据输入

Sensor 输入数据驱动系统运转



<center>💮💮💮</center>

## 基本概念

#### 🚘 Component

组件之间通过 Cyber channel 通信

#### 🚘 Channel

管理数据通信

#### 🚘 Node

每一个模块包含 Node 并通过 Node 来通信

#### 🚘 Reader/Writer

**订阅者模式**，往 channel 读写消息的类

#### 🚘 Service/Client

**请求/响应模式**

#### 🚘 Message

模块间通信的 **数据单元**

基于 **protobuf**

#### 🚘 Parameter

全局参数

#### 🚘 Record file

**记录** 从 channel 发送或接收的消息

**回放** record file 可以重现之前的操作行为

#### 🚘 Launch file 

提供一种 **启动模块** 的便利途径；

通过在 launch file 中定义一个或多个 dag 文件，可以同时启动多个 modules

#### 🚘 Task

异步计算任务

#### 🚘 CRoutine

协程

#### 🚘 Scheduler

用户空间任务调度器

#### 🚘 Dag file

定义 **模块拓扑结构** 的配置文件

[阅读原文](https://blog.csdn.net/kesalin/article/details/88914029)