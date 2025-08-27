# 使用官方 Python 3.9 镜像作为基础
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 更换为阿里云镜像源并安装编译 mysqlclient 和其他包所需的系统依赖
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt requirements.txt

# 使用阿里云的 pip 镜像源来安装依赖
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 将你的应用代码复制到镜像中
COPY . .

# 声明容器将监听 5000 端口
EXPOSE 5000

# 容器启动时运行的命令
CMD ["gunicorn", "--config", "gunicornConf.py", "server:app"]
