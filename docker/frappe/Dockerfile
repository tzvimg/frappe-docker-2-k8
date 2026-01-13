# Frappe + siud app production image
# Build context: frappe_docker/development/frappe-bench/apps directory
# Expects siud app at: ./siud
ARG PYTHON_VERSION=3.11.6
ARG NODE_VERSION=20.19.2

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

ARG FRAPPE_BRANCH=version-15
ARG FRAPPE_PATH=https://github.com/frappe/frappe

WORKDIR /home/frappe

# Initialize bench with frappe
RUN bench init --frappe-branch=${FRAPPE_BRANCH} --frappe-path=${FRAPPE_PATH} \
    --no-procfile --no-backups --skip-redis-config-generation --verbose frappe-bench

WORKDIR /home/frappe/frappe-bench

# Copy siud app from build context
COPY --chown=frappe:frappe siud apps/siud

# Install siud app dependencies (no frontend assets to build)
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
