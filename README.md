# Latex-BOI
A minimal Python Telegram Bot for LaTeX compilation. This telebot is currently run on EC2 under the handle @latexboi.

## Instructions
To install this on a cloud instance, follow these instructions for Debian-based distributions.
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
