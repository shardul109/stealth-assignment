FROM python

WORKDIR /app

# RUN apt-get update

COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt

COPY . .

EXPOSE 5002

CMD ["python", "main.py"]