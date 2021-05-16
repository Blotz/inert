<h1 align="center">
  &lt;INERT/&gt;
</h1>
<h6 align="center">
  A Discord bot written in python!
</h6>

---

### Setting up the bot
#### linux
```bash
# downloading required libraries
sudo apt-get install unixodbc-dev
# clone the github source code
git clone https://github.com:Blotz/inert.git
```
```bash
# downloading venv and activating the venv
cd inert
pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
# if all steps were successful, you should see the following
# (venv) username@hostname:file $
```
```bash
# running the code
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
