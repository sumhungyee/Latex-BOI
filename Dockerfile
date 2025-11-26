FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt ./
COPY script.py ./
RUN pip install -r requirements.txt
RUN apt update && apt install texlive-base texlive-latex-base texlive-latex-recommended texlive-pictures texlive-latex-extra poppler-utils -y

# COPY .env ./
CMD ["python", "script.py"]