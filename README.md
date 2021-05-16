<h1 align="center">
  &lt;INERT/&gt;
</h1>
<h6 align="center">
  A Discord bot written in python 3.8 or greater!
</h6>

---
# Setting up the bot
## Linux
<p>
Downloading required libraries and cloning the github source code
</p>

```bash
sudo apt-get install unixodbc-dev -y && \
  pip3 install virtualenv && \
  git clone https://github.com/Blotz/inert.git
```
<p>
Downloading venv and activating the venv
</p>

```bash
cd inert && \
  python3 -m virtualenv venv && \
  source venv/bin/activate && \
  pip install -r requirements.txt
```


## Windows
<p>
Downloading required libraries and cloning the github source code. <br>
You will need to install Visual c++ Build Tools
</p>

```bash
pip install virtualenv && \
  git clone https://github.com/Blotz/inert.git
```
<p>
Downloading venv and activating the venv
</p>

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
