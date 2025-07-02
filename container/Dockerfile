# Python Verison: 3.12
# python 3.12-slim-bookworm for linux/amd64
FROM python@sha256:69ce3aed05675d284bee807e7c45e560e98db21fb1e4c670252b4ee0f2496b6d

COPY pip.conf /etc/pip.conf

# appディレクトリを作成
WORKDIR /app

# 必要なPythonライブラリのインストール
COPY requirements.txt /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# プログラムや設定ファイルなどをコピーする
COPY main.py /app
COPY modules/ /app/modules/
