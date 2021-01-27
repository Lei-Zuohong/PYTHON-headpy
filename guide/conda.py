# -*- coding: UTF-8 -*-
# Public package

# Private package


conda = '''
[升级]
conda update conda
conda update anaconda
conda update --all

[包管理]
安装包 conda install package_name，添加版本号（例如 conda install numpy=1.10）
卸载包 conda remove package_name
更新包 conda update package_name，conda update --all
列出包 conda list
搜索包 conda search search_term

[环境管理]
创建环境 conda create -n env_name list of packages，
创建特定 Python 版本环境conda create -n py3 python=3或 conda create -n py2 python=2 的命令，安装特定版本（如 Python 3.3） conda create -n py python=3.3
激活环境OSX/Linux ：source activate my_env ； Windows： activate my_env
离开环境OSX/Linux ：source deactivate ； Windows： deactivate
保存环境conda env export > environment.yaml
加载环境conda env create -f environment.yaml 或conda env update -f=environment.yaml
列出所有环境conda env list
删除环境conda env remove -n env_name

补充包
jupyter: conda install jupyter notebook
自动关联环境:conda install nb_conda
代码自动补全包:conda install pyreadline

'''

conda_source = '''
Anaconda 是一个用于科学计算的 Python 发行版，支持 Linux, Mac, Windows, 包含了众多流行的科学计算、数据分析的 Python 包。

Anaconda 安装包可以到 https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/ 下载。

TUNA 还提供了 Anaconda 仓库与第三方源（conda-forge、msys2、pytorch等，查看完整列表）的镜像，各系统都可以通过修改用户目录下的 .condarc 文件。Windows 用户无法直接创建名为 .condarc 的文件，可先执行 conda config --set show_channel_urls yes 生成该文件之后再修改。

注：由于更新过快难以同步，我们不同步pytorch-nightly, pytorch-nightly-cpu, ignite-nightly这三个包。

channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
即可添加 Anaconda Python 免费仓库。

运行 conda clean -i 清除索引缓存，保证用的是镜像站提供的索引。

运行 conda create -n myenv numpy 测试一下吧。
'''
