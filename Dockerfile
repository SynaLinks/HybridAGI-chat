# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR HybridAGI-chat
COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install --upgrade pip && pip3 install -r requirements.txt
COPY ./ ./
CMD ["streamlit", "run", "Chat.py"]