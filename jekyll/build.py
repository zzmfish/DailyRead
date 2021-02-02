#!/usr/bin/env python3
import re
import os
import os.path
import datetime
import shutil

jekyll_dir = os.path.dirname(__file__)
os.chdir(jekyll_dir)
os.system('rm -rvf _posts/*')

# 列出markdown文件
file_list = []
os.chdir(os.path.join(jekyll_dir, '..'))
for root, dirs, files in os.walk('.'):
    if root.startswith('./.'):
        continue
    root = root.strip('./')
    if root.startswith('jekyll'):
        continue
    for file_name in files:
        if file_name.endswith('.md'):
            file_path = os.path.join(root, file_name)
            match_obj = re.search('(\d\d)(\d\d)-(.*md)', file_name)
            if not match_obj:
                print('File name not match: ', file_name)
                continue
            month = int(match_obj.group(1))
            date = int(match_obj.group(2))
            file_name = match_obj.group(3)
            try:
                file_date = datetime.datetime(2021, month, date).strftime('%Y-%m-%d')
            except ValueError:
                print('date not match: ', file_name)
                continue
            new_path = 'jekyll/_posts/%s-%s' % (file_date, file_name)
            file_list.append(new_path)
            if not os.path.exists(new_path) or os.path.getmtime(new_path) < os.path.getmtime(file_path):
                # 拷贝文件
                print('# Writing %s' % (new_path))
                with open(new_path, 'w') as new_file:
                    new_file.write('---\n')
                    new_file.write('layout: post\n')
                    new_file.write('title: %s\n' % (file_name[: file_name.rfind('.')]))
                    new_file.write('---\n')
                    new_file.write(open(file_path).read())
# TODO: 删除旧文件

# 编译网站
os.chdir(jekyll_dir)
os.system('bundle exec jekyll build')

