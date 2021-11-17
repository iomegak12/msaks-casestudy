FROM python:3.7-alpine

LABEL environment=Production
LABEL author="Ramkumar J Damodaran"
LABEL company=IOMEGA

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["pymon", "main.py"]
