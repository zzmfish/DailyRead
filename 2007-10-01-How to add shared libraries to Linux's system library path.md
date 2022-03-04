---
tags: 软件开发
---



* Create a new file in /etc/ld.so.conf.d/ called .conf
* Edit the file and add a line per directory of shared libraries (*.so files), it will look something like:
```bash
/usr/lib/APPLICATION/lib
```
* Reload the list of system-wide library paths:
```bash
sudo ldconfig
```

[原文](https://blog.andrewbeacock.com/2007/10/how-to-add-shared-libraries-to-linuxs.html)