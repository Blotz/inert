### 1. Get Linux
FROM debian

### 2. Label
LABEL maintainer="Blotz <https://github.com/blotz>"

### 3. Get python3 via the package manager
RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y python3 python3-pip

### . Set working directory
WORKDIR /code

### . Copy requirements
COPY requirements.txt .

### . Install build deps and download modules
RUN pip3 install --user --no-cache-dir -r requirements.txt

### . Copy code
COPY src/ .
### . Run
CMD [ "python3", "-u", "./main.py" ]