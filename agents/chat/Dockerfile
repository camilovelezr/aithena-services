FROM python:3.11-slim

RUN apt update && \
    apt upgrade -y

COPY . /aithena_agent_chat

RUN pip3 install /aithena_agent_chat --no-cache-dir
WORKDIR /aithena_agent_chat

EXPOSE 8765

CMD ["solara", "run", "src/polus/aithena_agent_chat/dashboard.py", "--host=0.0.0.0", "--production"]