FROM python:3.10.12
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app
COPY . /app
ENTRYPOINT [ "python3", "index.py" ]