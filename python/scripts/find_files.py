#!/usr/bin/env python3
"""查找文件通用脚本"""
import os
import fnmatch


def find_files(dir_path, patterns_list=['*'], exclude_dirs_list=[]):
    for root, dirnames, filenames in os.walk(dir_path):
        for pattern in patterns_list:
            for name in filenames:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(root, name)
        for exclude_dir in exclude_dirs_list:
            if exclude_dir in dirnames:
                dirnames.remove(exclude_dir)


if __name__ == '__main__':
    # 应用示例：查找指定目录及子目录下最大的十张图片
    temp = {name: os.path.getsize(name) for name in find_files(r'C:\Users\Administrator\Pictures', ['*.jpg', '*.png'])}
    res = sorted(temp.items(), key=lambda item: item[1], reverse=True)[:10]
    print(res)