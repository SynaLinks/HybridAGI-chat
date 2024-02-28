# syntax=docker/dockerfile:1
FROM python:3.10
WORKDIR HybridAGI-chat
COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install --upgrade pip && pip3 install --default-timeout=100 -r requirements.txt
COPY ./ ./
CMD ["streamlit", "run", "app.py"]