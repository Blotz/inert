### 1. Get Linux
FROM alpine:latest

### 2. Label
LABEL maintainer="Dockerfile created by Blotz <https://github.com/blotz>"

### 3. Get python3 via the package manager
RUN apk update \
&& apk upgrade \
&& apk add --no-cache python3 py3-pybind11 \
&& python3 -m ensurepip \
&& pip3 install --upgrade pip setuptools wheel \
&& rm -r /usr/lib/python*/ensurepip && \
if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi

### . Set working directory
WORKDIR /code

### . Copy requirements
COPY requirements.txt .

### . Install build deps and download modules
RUN apk add --no-cache make \
  gcc \
  g++ \
  python3-dev \
  libjpeg \
  openjpeg \
  tiff \
  libxcb \
  musl-dev \
  unixodbc-dev \
  # Pillow dependencies
  freetype-dev \
  fribidi-dev \
  harfbuzz-dev \
  jpeg-dev \
  lcms2-dev \
  openjpeg-dev \
  tcl-dev \
  tiff-dev \
  tk-dev \
  zlib-dev \
  # SQL Drivers
  libc-dev \
  libxml2 \
  mariadb-dev \
  postgresql-dev \
&& pip3 install --no-cache-dir -r requirements.txt \
&& apk del musl-dev freetype-dev fribidi-dev harfbuzz-dev jpeg-dev lcms2-dev openjpeg-dev tcl-dev tiff-dev tk-dev zlib-dev

### . Copy code
COPY src/ .
### . Run
CMD [ "python", "./main.py" ]
