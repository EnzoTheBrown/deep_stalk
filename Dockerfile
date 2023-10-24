FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY database.py .
COPY main.py .
COPY statistics.py .
RUN mkdir datasets
RUN mkdir templates
COPY templates/* templates
COPY datasets/lvmh.csv datasets

CMD [ "python", "./main.py" ]