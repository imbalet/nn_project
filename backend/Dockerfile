FROM tensorflow/tensorflow:latest

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y\
    python3 python3-dev gcc \
    gfortran musl-dev

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./backend

EXPOSE 5000

# RUN python backend/app.py

CMD ["python3", "/usr/src/app/backend/app.py"]