---
layout: posts
title: C++ explicit、#pragma once
tags: 开发
---


## C++ explicit 关键字

#### 隐式类型转换

```C++
#include <iostream>
using namespace std;

class Point {
public:
    int x, y;
    Point(int x = 0, int y = 0)
        : x(x), y(y) {}
};

void displayPoint(const Point& p) 
{
    cout << "(" << p.x << "," 
         << p.y << ")" << endl;
}

int main()
{
    displayPoint(1); //隐式调用构造函数
    Point p = 1;  //隐式调用构造函数，而不是operator=
}
```



#### explicit关键字

指定构造函数或转换函数 (C++11起)为显式，即它不能用于*隐式转换*和*复制初始化*。



## C++ #pragma once 与 #ifndef 解析

为了避免同一个文件被include多次，C/C++中有两种方式：

#### #ifndef

```C++
#ifndef SOMEFILE_H
#define SOMEFILE_H
// 声明、定义语句...
#endif
```

 #### #pragma once

```C++
#pragma once
// 声明、定义语句...
```


[阅读原文](https://zhuanlan.zhihu.com/p/52152355)