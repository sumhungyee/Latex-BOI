# Latex-BOI
<img width="575" height="180" alt="image" src="https://github.com/user-attachments/assets/2119f632-75e1-4beb-88a2-dab71cc0dd24" />

A minimal Python Telegram Bot for LaTeX compilation. This telebot is currently run under the handle @latexboiboibotbot.

## Functionality
1. Accomodates multiple users (each message creates a unique job)
2. Displays compilation error messages
3. Dynamic (but simple) resizing of canvas


## Instructions
### Docker Guide
Define `.env` with `TELEBOT_TOKEN` as an environment variable key with the value being your telegram bot token. Uncomment `RUN cp .env ./` in `Dockerfile` and run with `docker build -t <name> .`

### Minimal Installation Guide
To install this on a cloud instance (such as AWS EC2) without docker, follow these instructions for Debian-based distributions.
```
sudo apt update -y
sudo apt install git python3 -y
sudo apt install python3-pip python3-venv -y
# EITHER
sudo apt install texlive-base texlive-latex-base texlive-latex-recommended texlive-pictures texlive-latex-extra poppler-utils tmux -y
# OR
sudo apt-get install texlive-full poppler-utils tmux -y

git clone https://github.com/sumhungyee/Latex-BOI.git
python3 -m venv venv
pip install -r requirements.txt
```
## Tmux to run script in background
```
tmux new -s session
source venv/bin/activate
cd Latex-BOI

```
Then, either define `.env` with `TELEBOT_TOKEN=<YOUR_TOKEN_HERE>`.
Lastly, run `python script.py`. Also, one may detach from the session with `ctrl` + `B`, then `D`.
