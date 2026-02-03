# Frappe + siud app production image
# Build context: frappe_docker/development/frappe-bench/apps directory
# Expects frappe at: ./frappe, siud at: ./siud
ARG PYTHON_VERSION=3.14.2
ARG NODE_VERSION=24.12.0

FROM python:${PYTHON_VERSION}-slim-bookworm AS base

ARG NODE_VERSION
ENV NVM_DIR=/home/frappe/.nvm
ENV PATH=${NVM_DIR}/versions/node/v${NODE_VERSION}/bin/:${PATH}

RUN useradd -ms /bin/bash frappe \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
    curl git vim nginx gettext-base file \
    libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libpangocairo-1.0-0 \
    restic gpg mariadb-client less libpq-dev postgresql-client \
    wait-for-it jq media-types \
    && mkdir -p ${NVM_DIR} \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash \
    && . ${NVM_DIR}/nvm.sh && nvm install ${NODE_VERSION} && npm install -g yarn \
    && rm -rf /var/lib/apt/lists/* ${NVM_DIR}/.cache \
    && rm -fr /etc/nginx/sites-enabled/default \
    && pip3 install frappe-bench \
    && sed -i '/user www-data/d' /etc/nginx/nginx.conf \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    && touch /run/nginx.pid \
    && chown -R frappe:frappe /etc/nginx/conf.d /etc/nginx/nginx.conf /var/log/nginx /var/lib/nginx /run/nginx.pid

FROM base AS build

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    wget libpq-dev libffi-dev liblcms2-dev libldap2-dev libmariadb-dev \
    libsasl2-dev libtiff5-dev libwebp-dev pkg-config redis-tools rlwrap \
    tk8.6-dev cron gcc build-essential libbz2-dev \
    && rm -rf /var/lib/apt/lists/*

USER frappe

FROM build AS builder

WORKDIR /home/frappe

# Create bench structure manually using frappe from build context
RUN mkdir -p frappe-bench/apps frappe-bench/sites frappe-bench/logs frappe-bench/config

WORKDIR /home/frappe/frappe-bench

# Copy frappe app from build context (instead of cloning from GitHub)
COPY --chown=frappe:frappe frappe apps/frappe

# Create Python virtual environment and install frappe
RUN python -m venv env \
    && ./env/bin/pip install --upgrade pip wheel setuptools \
    && ./env/bin/pip install -e apps/frappe

# Create bench config files required for bench CLI to work
RUN echo "" > patches.txt \
    && echo 'web: bench serve --port 8000\nsocketio: node apps/frappe/socketio.js\nwatch: bench watch\nschedule: bench schedule\nworker: bench worker' > Procfile

# Copy pre-built assets from build context (skip rebuilding)
# Assets were already built in the devcontainer

# Copy siud app from build context
COPY --chown=frappe:frappe siud apps/siud

# Install siud app and finalize setup
RUN ./env/bin/pip install -e apps/siud \
    && printf "frappe\nsiud\n" > sites/apps.txt \
    && echo "{}" > sites/common_site_config.json \
    && find apps -mindepth 1 -path "*/.git" | xargs rm -fr

FROM base AS production

USER frappe
WORKDIR /home/frappe/frappe-bench

COPY --from=builder --chown=frappe:frappe /home/frappe/frappe-bench /home/frappe/frappe-bench

VOLUME ["/home/frappe/frappe-bench/sites"]

EXPOSE 8000 9000 8080

CMD ["/home/frappe/frappe-bench/env/bin/gunicorn", \
     "--chdir=/home/frappe/frappe-bench/sites", \
     "--bind=0.0.0.0:8000", "--threads=4", "--workers=2", \
     "--worker-class=gthread", "--worker-tmp-dir=/dev/shm", \
     "--timeout=120", "--preload", "frappe.app:application"]
