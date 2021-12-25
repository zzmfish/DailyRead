---
layout: posts
title: Statically configure a Firewall to let OMG DDS Traffic through
tags: 未分类
---


## DDS端口

> The ports \(and multicast addresses\) used by DDS implementations \(such as RTI Connext DDS\) are specified by the [OMG DDS Interoperability Wire Protocol Specification \(DDS-RTPS\)](http://www.omg.org/spec/DDS-RTPS/).By default, each DomainParticipant opens 4 UDP/IP ports: Two of those ports are multicast ports which are shared among all domain participants in the same DomainId. The other two are unicast ports which are different for each participant within a computer. The multicast IP address used for discovery is 239.255.0.1 by default consistent which the DDS-RTPS specification.

默认情况下，每个DomainParticipant打开4个UDP/IP端口

* **2个组播端口**：同一个domainId下所有participants共享
* **2个单播端口**：每个participant都不同

用作发现的**组播IP**地：`239.255.0.1`

> The ports used are given by a formula that depends on the DDS domainId and the number of participants that are already running on the same operating system instance (computer or virtual machines):

端口分配依赖`DmainId`和`participant数量`


> Multicast Ports (common to all applications on a domainId):
>
> ```
> DiscoveryMulticastPort  =   PB + DG * domainId + d0
> UserMulticastPort	=   PB + DG * domainId + d2
> ```
>
> Unicast Ports (different for each participant running on a single operating system instance. Computer or VM):
>
> ```
> DiscoveryUnicastPort    =   PB + DG * domainId + d1 + PG * participantId
> UserUnicastPort         =   PB + DG * domainId + d3 + PG * participantId
> ```
>
> These formulas are depend on two variables: domainId and participantId
>
> ```
> domainId      - Is the DDS domainId
> participantId - Is an integer starting at 0 that enumerates each participant 
>                 that runs on a given operating system instance (computer 
>                 or virtual machine). 
>                 The first participant will be 0, the second 1, etc.
> ```
>
> The formulas are parameterized by the constants d0, d1, d2, d3, PB, DG, and PG which are all defined in the OMG DDS Interoperability Wire Protocol Specification (DDS-RTPS) as follows:
>
> ```
> d0  (builtin_multicast_port_offset)    = 0
> d2  (user_multicast_port_offset)       = 1 
> d1  (builtin_unicast_port_offset)      = 10
> d3  (user_unicast_port_offset)         = 11
> PB  (port_base)             = 7400
> DG ( domain_id_gain)        = 250
> PG  (participant_id_gain)   = 2
> ```
>

公式中使用的常数是DDS协议编译的默认值。

可以通过`DomainParticipantQos`里面的`WireProtocolQosPolicy`改变端口映射。

[阅读原文➡](https://community.rti.com/content/forum-topic/statically-configure-firewall-let-omg-dds-traffic-through)
