FROM python:slim

ARG VERSION

ARG API_HOST
ENV API_HOST=${API_HOST}

ARG API_PORT
ENV API_PORT=${API_PORT}

ARG APP_DIR="/app"
ENV APP_DIR=${APP_DIR}

ARG DATA_DIR="/var/cesium-api/"
ENV DATA_DIR=${DATA_DIR}

ARG API_PREFIX="/"
ENV API_PREFIX=${API_PREFIX}


RUN mkdir -p ${APP_DIR}

COPY --from=root pyproject.toml ${APP_DIR}
COPY --from=dist cesium_api ${APP_DIR}

EXPOSE ${API_PORT}

ENTRYPOINT cesium-api --host ${API_HOST} --port ${API_PORT} --data-dir ${DATA_DIR} --prefix ${API_PREFIX}
