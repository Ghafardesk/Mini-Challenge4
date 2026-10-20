FROM rocm/pytorch:rocm10.0_ubuntu26.04_py3.14_pytorch_release_2.13.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    LOCAL_LLM_BASE_URL=http://127.0.0.1:11434/v1 \
    QWEN_MODEL=qwen3:4b \
    APP_HOME=/opt/amd-ai-league-agent

WORKDIR ${APP_HOME}

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY . ${APP_HOME}

RUN mkdir -p /models

CMD ["python", "-m", "app.cli", "--help"]
