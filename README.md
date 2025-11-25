# Latex-BOI
A minimal Python Telegram Bot for LaTeX compilation

## Instructions
To install this on a cloud instance, follow these instructions for Debian-based distributions.
```
sudo apt update -y
sudo apt install git python3 -y
sudo apt install python3-pip python3-venv -y
sudo apt install texlive-base texlive-latex-base texlive-latex-recommended texlive-pictures texlive-latex-extra poppler-utils -y

git clone https://github.com/sumhungyee/Latex-BOI.git
python3 -m venv venv
source venv/bin/activate
cd Latex-BOI
pip install -r requirements.txt
python script.py

```
Lastly, either define `.env` with `TELEBOT_TOKEN=<YOUR_TOKEN_HERE>`
