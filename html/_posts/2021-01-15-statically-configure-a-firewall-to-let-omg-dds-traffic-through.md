---
layout: posts
title:  "statically-configure-a-firewall-to-let-omg-dds-traffic-through"
---

# Statically configure a Firewall to let OMG DDS Traffic through

There are various strategies that can be used to have DDS applications communicate between each other `despite` the fact that one or more of these applications are protected by a firewall.

尽管应用程序可能被防火墙隔离，还是有多种策略可以让DDS应用程序彼此通讯。

This HOWTO focuses in the situation where there is a desire to use static configuration \(i.e. manually open specific ports or multicast addresses in the firewall\) and the applications are protected with Firewalls but are not behind Network Address Translators \(NATs\). In other words the IP of one computer is reachable from the other directly \(assuming the Firewall forwards the traffic\).

## Background: Ports used by DDS Discovery

The ports \(and multicast addresses\) used by DDS implementations \(such as RTI Connext DDS\) are specified by the [OMG DDS Interoperability Wire Protocol Specification \(DDS-RTPS\)](http://www.omg.org/spec/DDS-RTPS/).By default, each DomainParticipant opens 4 UDP/IP ports: Two of those ports are multicast ports which are shared among all domain participants in the same DomainId. The other two are unicast ports which are different for each participant within a computer. The multicast IP address used for discovery is 239.255.0.1 by default consistent which the DDS-RTPS specification.

The ports used are given by a formula that depends on the DDS domainId and the number of participants that are already running on the same operating system instance \(computer or virtual machines\):

Multicast Ports \(common to all applications on a domainId\):

```text
DiscoveryMulticastPort  =   PB + DG * domainId + d0
UserMulticastPort    =   PB + DG * domainId + d2
```

Unicast Ports \(different for each participant running on a single operating system instance. Computer or VM\):

```text
DiscoveryUnicastPort    =   PB + DG * domainId + d1 + PG * participantId
UserUnicastPort         =   PB + DG * domainId + d3 + PG * participantId
```

These formulas are depend on two variables: domainId and participantId

```text
domainId      - Is the DDS domainId
participantId - Is an integer starting at 0 that enumerates each participant 
                that runs on a given operating system instance (computer 
                or virtual machine). 
                The first participant will be 0, the second 1, etc.
```

The formulas are parameterized by the constants d0, d1, d2, d3, PB, DG, and PG which are all defined in the OMG DDS Interoperability Wire Protocol Specification \(DDS-RTPS\) as follows:

```text
d0  (builtin_multicast_port_offset)    = 0
d2  (user_multicast_port_offset)       = 1 
d1  (builtin_unicast_port_offset)      = 10
d3  (user_unicast_port_offset)         = 11
PB  (port_base)             = 7400
DG ( domain_id_gain)        = 250
PG  (participant_id_gain)   = 2
```

For example, assuming you are running in domainId=0 \(the default\), if you have two participants running in the computer, then the ports used will be:

All applications:

```text
DiscoveryMulticastPort  = 7400
UserMulticastPort       = 7401
```

First application:

```text
DiscoveryUnicastPort    = 7410
UserUnicastPort         = 7411
```

Second application:

```text
DiscoveryUnicastPort    = 7412
UserUnicastPort         = 7413
```

So if the maximum number of participants that will be running on the computer is 2, you need to open the following ports in the firewall: 7400, 7401, 7410, 7411, 7412, 7413 You can download this [Spreadsheet UDP Ports Used by OMG DDS](http://community.rti.com/filedepot?cid=11&fid=14) to compute which ports will be open for a specific domainId and participantId.

It should be noted that the above formulas are for the default setup which complies with the OMG DDS Interoperability Wire Protocol. In addition to this RTI Connext DDS allows integrators to change the port mappings to fit specific deployment scenario. This is done using the WireProtocolQosPolicy within the DomainParticipantQos

Specifically the member rtps\_well\_known\_ports within the [WireProtocolQosPolicy](http://community.rti.com/rti-doc/500/ndds.5.0.0/doc/html/api_cpp/structDDS__WireProtocolQosPolicy.html) allows an application to override the default settings for all the above constants. Note that if this Qos Policy is changed, then it must be done consistently on all the DomainParticipants within the DDS Domain or else they will not discover each other.

## Opening firewall ports

If your firewall configuration supports opening multicast addresses for given ports as well as opening ports without specifying a particular IP where to redirect the packets received on that port then taking advanatge of this feature is often the simplest thing to do.

First use the [Spreadsheet UDP Ports Used by OMG DDS](http://community.rti.com/filedepot?cid=11&fid=14) to determine which ports you need to open based on the domainId \(or domainIds\) that will be communicating across the firewall and the maximum number of participants that you will ever have running on a a single computer on that domain Id. If you are unsure of this number just use the maximum of 120 participants \(participantId 0-119\).

For example if we will be communicating on domainId=0 and we want to open ports for any number of participants per computer \(up to the maximum\), then we would open the UDP range 7400-7649 \(both included\). 7400 is the lowest UDP port used when participantId=0 and 7649 is the highest one used when participantId=119

If we wanted the same only for domainId=10, then we would open UDP ports 9900-10149.

In addition to the above you also need to configure the firewall to forward multicast packets on the multicast address 239.255.0.1 for the multicast ports in the domainId that you plan to use. For example if you are using domainId=0, you need to configure that multicast address to be open on UDP ports 7400 and 7401. If yiu are using domainId=10 it would be UDP ports 9900 amd 9901.

## Setting port-forwarding rules in the firewall or firewalls that do not support multicast

Some firewalls do not allow ports to simply be open such that packets can reach any computer behind the firewall. Rather they only allow ports to be forwarded where all IP packets reaching the firewall on that port are forwarded to a specific IP address \(and port number\) behind the firewall. Other firewalls cannot be configured to forward multicast IP packets.

If you have this kind of firewall and you are planning to run DDS on more than one computer behind the firewall then you face a problem. The packets forwarded by the firewall on a particular port can only go to one destination so it would not be possible to reach all the computers behind the firewall.

The solution to this scenario is to deploy a RTI DDS Routing Service behind the Firewall. The RTI DDS Routing Service acts as proxy for all the computers that run DDS behind the firewall. The Firewall is configured to forward all traffic on the DDS ports to the RTI DDS Routing Service and this application will then relay it to their intended destinations.

The RTI DDS Routing Service can be configured to automatically relay all traffic between two domains, or to do it only for certain DDS Topics, or packets with specific content on a Topic, giving you additional control over which data flows in and out of the Firewall via DDS.

The RTI DDS Routing Service will have two DomainParticipants each with its own domainId. One domainId is used to communicate with the applications outside the firewall and the other with the applications inside. Since all the DDS traffic from the firewall is forwarded to the Participant in the RTI DDS Routing Service that is using the domainId chosen for the "outside-the-firewall" configuration you only need to forward the ports that domainId.

For example, assume we choose domainId=0 to be our "outside the firewall" domain and domainId=1 for the applications behind the firewall. Then we just need to forward the ports to a single participant running on domainId=0 \(the one inside RTI DDS Routing Service\) so this only necessitates opening ports 7400-7411 \(both included\).

The above assumes you will only one instance of the RTI DDS Routing Service, which is the normal case. If you wanted to run multiple instances on the same computer, for example to a redundant scenario or a load-balancing scenario, then you would have t take that into consideration when computing the range of ports that should be forwarded.

## Reaching applications behing a firewall with a NAT

If the firewall also has a Network Address Translators \(NATs\), then the IP addresses of any computer inside the firewall are not directly reachable outside the firewall. This scenario is also supported using the RTI DDS Routing Service but the setup will be explained in a separate HOWTO.

