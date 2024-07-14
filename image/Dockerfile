FROM jenkins/jenkins:lts

USER root


# Обновляем пакеты и устанавливаем зависимости для сборки Python
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    python3   \
    python3-pip  \
    python3-venv \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libffi-dev \
    wget \
    curl \
    git \
    && apt-get install -y rsync


# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install poetry in the virtual environment
RUN pip install poetry

RUN pip install pytest allure-pytest 'python-dotenv==0.20.0'


USER jenkins
