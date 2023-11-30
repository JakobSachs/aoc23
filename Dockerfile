from python:3.11.0-slim-bullseye

WORKDIR /advent-of-code-23
COPY requirements.txt /advent-of-code-23

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /advent-of-code-23

CMD ["python", "timer.py"]
