FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置 Python 环境变量
ENV PYTHONUNBUFFERED=1

# 启动 Bot
CMD ["python", "bot.py"]
