---
tags: 软件开发
header:
  image: "http://zhouzm.cn/images/%E7%BE%8E%E5%9B%BE/210517%E8%8A%B1%E6%B5%B7.jpg"
---



## Sandboxing

🐣restricting file system access

🐣constructs an `execroot/` directory for each action

🐣`execroot/` contains all input files to the action

## Reasons for sandboxing

🐣not know if a tool uses undeclared input files

🐣incorrect reuse of cache entries creates problems during remote caching

🐣closely related to remote execution

## sandboxfs

🐣a FUSE file system

🐣exposes an arbitrary view of the underlying file system

## Debugging

#### Deactivated namespaces

On some platforms user namespaces are deactivated by default due to security concerns.

#### Rule execution failures

#### Detailed debugging for build failures

If your build failed, use `--verbose_failures` and `--sandbox_debug` to make Bazel show the exact command.

[阅读原文](https://docs.bazel.build/versions/master/sandboxing.html)