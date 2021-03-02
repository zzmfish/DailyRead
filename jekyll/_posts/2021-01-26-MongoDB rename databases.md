---
layout: posts
title: MongoDB rename databases
tags: 开发
---


> > The "copydb" command is deprecated, please use these two commands instead:
> 1. mongodump to back up data
> 2. mongorestore to recover data from mongodump into a new namespace

不赞成使用`copy`命令，请使用以下两个命令来代替：

1. `mongodump`备份数据
2. `mongorestore`从mongodump的数据恢复到一个新的命名空间



> We are aware of how painful and long it is to rename a database in MongoDB. Unfortunately, this is not an simple feature for us to implement due to the way that database metadata is stored in the original (default) storage engine. In MMAPv1 files, the namespace (e.g.: dbName.collection) that describes every single collection and index includes the database name, so to rename a set of database files, every single namespace string would have to be rewritten. This impacts:
> - the .ns file
> - every single numbered file for the collection
> - the namespace for every index
> - internal unique names of each collection and index
> - contents of system.namespaces and system.indexes (or their equivalents in the future)
> - other locations I may be missing

我们清楚在MongoDB重命名一个数据库有多痛苦和要多久。很不幸因为数据库**元数据**的存储方式，并不存在一种简单的实现方式。在`MMAPv1`文件中，**命名空间**描述每一个集合、索引和数据库的名称，因此为了修改一系列数据库文件，每个名字空间字符串都要被修改。这影响到：

* `.ns文件`

* 集合的每个`编号文件`

* 每个集合和索引的`内部唯一命名`
* `system.namespace`和`system.indexes`的内容
* 其他我可能遗漏的地方



> This is just to accomplish a rename of a single database in a standalone mongod instance. For replica sets the above would need to be done on every replica node, plus on each node every single oplog entry that refers this database would have to be somehow invalidated or rewritten, and then if it's a sharded cluster, one also needs to add these changes to every shard if the DB is sharded, plus the config servers have all the shard metadata in terms of namespaces with their full names.

这只是完成单一mongod实例的数据库重命名。**副本集**需要在每一个节点上做一遍以上操作，另外每个节点上的每个用到这个库的`oplog条目`都会变无效或需要重写。而对于**分片集群**，要对这个数据库的每个分片都加上这些修改，包括含有所有数据库完整名称的`分片元数据`的**配置服务器**。



> There would be absolutely no way to do this on a live system.
> To do it offline, it would require re-writing every single database file to accommodate the new name, and at that point it would be as slow as the current "copydb" command.

这实在无法在一个在线系统上实现。

离线做的话，这需要重写每一个数据库文件去适应新名字，然而这会和现在的`copydb`一样慢。



MongoDB Product Team，Sep 10, 2019

[阅读原文](https://jira.mongodb.org/browse/SERVER-701)