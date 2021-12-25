---
layout: posts
title: Bazel——Concepts and terminology
tags: 软件开发
header: 
  image: "http://zhouzm.cn/images/%E7%BE%8E%E5%9B%BE/210525%E8%BF%90%E5%8A%A8.jpg"
---




## Workspace, packages and targets

#### 🛸 Workspace

* Contains the **source files for the software** you want to build

* Contains symbolic links to directories that contain the **build outputs**

* **WORKSPACE** (or WORKSPACE.bazel) file contains references to **external dependencies** required to build the outputs

* Directories containing a WORKSPACE file are considered the **root** of a workspace

* Directory trees in a workspace rooted at a subdirectory containing a WORKSPACE file are ignored

  <br>

#### 🛸 Repositories
* Directory containing the WORKSPACE file is the root of the **main repository**, also called **@**

* **External repositories** are defined in the WORKSPACE file using workspace rules

<br/>

#### 🛸 Packages

* A collection of related **files** and a specification of the **dependencies** among them
* Contains a file named **BUILD** (or BUILD.bazel)

<br/>

#### 🛸 Targets

###### 1️⃣ Files

1. Source files

2. Generated files

###### 2️⃣ Rules

* The **relationship** between a set of **input** and a set of **output** files；

* The necessary **steps** to derive the outputs from the inputs

###### 3️⃣ Package groups

* Sets of packages whose purpose is to **limit accessibility** of certain rules

<br/>

#### 🛸 Labels

* The **name** of a target

```bash
@myrepo//my/app/main:app_binary

# same repository
//my/app/main:app_binary

# equals to "//my/app:app"
//my/app

# equals to ":app"、"//my/app"、"//my/app:app"
app
```

<center>🌒🌓🌔</center>

## BUILD files

* Every package contains a BUILD file

* Evaluated using an imperative language **Starlark**
* Order does matter
* **Functions** should be declared in **.bzl**  files

#### 🛸 Loading an extension

* Bazel extensions are files ending in **.bzl**
* Use the **load** statement to import a symbol from an extension.
* Symbols starting with **_** are not exported

```python
load("//foo/bar:file.bzl", "some_library")

# alias
load("//foo/bar:file.bzl", library_alias = "some_library")   

# multiple aliases
load(":my_rules.bzl", "some_rule", nice_alias = "some_other_rule")
```

<center>🌒🌓🌔</center>

## Types of build rule

#### 🛸 *_binary rules

* Build executable programs
* The executable will reside in the build tool's binary output tree at the corresponding name for the rule's label, so `//my:program` would appear at (e.g.) `$(BINDIR)/my/program`
* Create a runfiles directory containing all the files mentioned in a **data** attribute belonging to the rule, or any rule in its transitive closure of dependencies

<br>

#### 🛸 *_test rules

* for automated testing

<br>

#### 🛸 *_library rules

* specify separately-compiled modules in the given programming language

<center>🌒🌓🌔</center>

## Dependencies

* Induces a **Directed Acyclic Graph (DAG)** over targets, and we call this a **dependency graph**
*  A target's **direct dependencies** are those other targets reachable by a path of length 1 in the dependency graph
* A target's **transitive dependencies** are those targets upon which it depends via a path of any length through the graph.

#### 🛸 Actual and declared dependencies

#### 🛸 Types of dependencies

#### 🛸 Using labels to reference directories

[阅读原文](https://docs.bazel.build/versions/4.1.0/build-ref.html)

