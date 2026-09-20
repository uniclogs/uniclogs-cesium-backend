FROM python:latest

ARG VERSION

ARG API_HOST="127.0.0.1"
ENV API_HOST=${API_HOST}

ARG API_PORT=7032
ENV API_PORT=${API_PORT}

ARG DATA_DIR="/var/cesium-api/"
ENV DATA_DIR=${DATA_DIR}

ENV TMP_DIR="/tmp"
ENV WHEEL_NAME="uniclogs_cesium_backend-${VERSION}-py3-none-any.whl"
ENV WHEEL_PATH="${TMP_DIR}/${WHEEL_NAME}"

COPY --from=dist ${WHEEL_NAME} ${WHEEL_PATH}
RUN pip install -U ${WHEEL_PATH}
RUN rm -rf ${WHEEL_PATH}

EXPOSE ${API_PORT}

ENTRYPOINT gunicorn uniclogs_cesium_backend --bind ${API_HOST}:${API_PORT}