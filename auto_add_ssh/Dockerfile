# 请不要压缩这些RUN命令为一行，这个是构建容器，并非运行的容器，无需通过减少层，来压缩镜像体积
FROM conda/miniconda3-centos6

MAINTAINER Allen.W

# 添加conda源，加速构建
RUN conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
RUN conda config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
RUN conda config --add channels https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
RUN conda config --set show_channel_urls yes


# 工作目录
WORKDIR /auto_add_ssh
# 创建 pyinstaller 的dist目录
RUN mkdir -p ./dist
# 创建 pyinstaller 的build目录
RUN mkdir -p ./build
# release 发布目录
RUN mkdir -p ./release

# 复制所有文件
COPY . .

# conan 压缩目录
RUN mkdir -p ./aas-$(cat VERSION)

RUN conda info
# init conda 环境
RUN conda init bash

# 安装依赖，指定阿里源
#RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 构建单文件包
RUN pyinstaller --onefile ./run.py

RUN cp -r ./dist/run ./aas-$(cat VERSION)/auto-add-ssh
RUN cp -r ./VERSION ./aas-$(cat VERSION)/
RUN cp -r ./README.md ./aas-$(cat VERSION)/

# 压缩
RUN tar -czf aas-$(cat VERSION).tar.gz ./aas-$(cat VERSION)/

# 运行时，输出目录，到release，运行完结束
CMD cp ./aas-$(cat VERSION).tar.gz ./release/
