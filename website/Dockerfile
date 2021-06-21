### 1. Get Linux
FROM debian

### 2. Get python3 via the package manager
RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y python3 python3-pip 

### 3. Set working directory
WORKDIR /code

### 4. Copy requirements
ADD requirements.txt /code/requirements.txt

### 5. Install build deps and download modules
RUN pip3 install --user --no-cache-dir -r requirements.txt

### 5. Copy code
ADD . /code/
### 6. Run
CMD [ "flask", "run" ]