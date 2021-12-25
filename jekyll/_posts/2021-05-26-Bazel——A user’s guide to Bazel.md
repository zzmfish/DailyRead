---
layout: posts
title: Bazel——A user’s guide to Bazel
tags: 软件开发
---




## Phases of a build

#### Loading phase

🔹All the necessary **BUILD files** for the initial targets, and their transitive closure of dependencies, are **loaded, parsed, evaluated and cached**

🔹Errors reported during this phase: 

⛔ package not found

⛔ target not found

⛔ lexical and grammatical errors in a BUILD file

⛔ evaluation errors

#### Analysis phase

🔹Semantic analysis and validation of each build rule

🔹Construction of a build dependency graph

🔹Determination of exactly what work is to be done in each step of the build

🔹Errors reported at this stage:

⛔ inappropriate dependencies

⛔ invalid inputs to a rule

⛔ all rule-specific error messages

#### Execution phase

🔹ensures that the outputs of each step in the build are consistent with its inputs

🔹re-running compilation/linking/etc

🔹Errors reported during this phase:

⛔ missing source files

⛔ errors in a tool executed by some build action

⛔ failure of a tool to produce the expected set of outputs

<center>☁️☁️☁️</center>

## Client/server implementation

#### Server

🔹A **long-lived** server process

🔹**Caches** of BUILD files, dependency graphs, and other metadata

🔹Improves the speed of **incremental builds**

🔹The name of a Bazel server process appears in the output of `ps x` or `ps -e f`

#### Client

🔹`bazel` command

🔹Finds the server based on the output base, which by default is determined by the path of the base **workspace directory** and your **userid**

🔹If the client cannot find a running server instance, it **starts** a new one

🔹Will **stop** after a period of inactivity (3 hours, by default, which can be modified using the startup option `--max_idle_secs`)

<center>☁️☁️☁️</center>

## .bazelrc, the Bazel configuration file

specify unchanged options

#### Imports

🔹`import`

🔹`try-import`

#### Option defaults

#### --config





[阅读原文](https://docs.bazel.build/versions/4.1.0/guide.html#phases-of-a-build)

