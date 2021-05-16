<h1 align="center">
  &lt;INERT/&gt;
</h1>
<h6 align="center">
  A Discord bot written in python 3.8 or greater!
</h6>

<p>
  <a href="https://github.com/Blotz/inert/wiki" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://github.com/Blotz/inert/blob/main/LICENSE" target="_blank">
    <img alt="License: GPL--3.0 Licence" src="https://img.shields.io/badge/License-GPL--3.0 Licence-yellow.svg" />
  </a>
</p>

---
# Info
## Install
```sh
https://github.com/Blotz/inert#setting-up-the-bot
```

### Author
👤 **Blotz**
* Github: [@Blotz](https://github.com/Blotz)

### 🤝 Contributing
Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/Blotz/inert/issues).

---
# Setting up the bot
## Linux
Download required libraries and clone the github source code
```bash
sudo apt-get install unixodbc-dev -y && \
  pip3 install virtualenv && \
  git clone https://github.com/Blotz/inert.git
```
Download venv and activate the venv
```bash
cd inert && \
  python3 -m virtualenv venv && \
  source venv/bin/activate && \
  pip install -r requirements.txt
```


## Windows

Download required libraries and clone the github source code. <br>
You will need to install [Visual C++ Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)

```bash
pip install virtualenv && \
  git clone https://github.com/Blotz/inert.git
```
Download venv and activate the venv
```bash
cd inert && \
  python -m virtualenv venv && \
  .\venv\Scripts\activate && \
  pip install -r requirements.txt
```
## Config
Create a new file called `.env` in the inert folder
```dotenv
TOKEN=your_discord_bot_token
REDDIT_ID=reddit_application_id
REDDIT_SECRET=reddit_application_secret
```
---
# Running the code
If all steps above were successful , you should see the following (or something similar): <br>
`(venv) username@hostname:file $` <br>
When ever you want to run the code, unless your ide does this for you,
you will need to run the following commands in order to run the code <br>
**Windows**
```bash
.\venv\Scripts\activate
```
**Linux**
```bash
source venv/bin/activate
```
then run `python main.py` in the src folder

---
## 📝 License

Copyright © 2021 [Blotz](https://github.com/Blotz).<br />
This project is [GPL--3.0 Licence](https://github.com/Blotz/inert/blob/main/LICENSE) licensed.
