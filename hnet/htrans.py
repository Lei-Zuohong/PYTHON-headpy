# -*- coding: UTF-8 -*-
# Public package
import os
import sys
import requests
# Private package


def download(url, file_path):
    '''
    url: string, 下载地址
    file_path: string, 文件储存地址
    '''
    # 关闭网站证书
    r = requests.get(url, stream=True, verify=False)
    # 文件大小
    total_size = int(r.headers['Content-Length'])
    temp_size = 0
    # 写入文件
    with open(file_path, "wb") as f:
        # 指定单元大小
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                #############花哨的下载进度部分###############
                done = int(50 * temp_size / total_size)
                # 调用标准输出刷新命令行，看到\r回车符了吧
                # 相当于把每一行重新刷新一遍
                sys.stdout.write("\r[%s%s] %d%% %s" % (
                    '*' * done, ' ' * (50 - done), 100 * temp_size / total_size, file_path))
                sys.stdout.flush()
    print()  # 避免上面\r 回车符，执行完后需要换行了，不然都在一行显示
