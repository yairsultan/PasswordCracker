FROM python:3.9

WORKDIR /app




COPY ./Master/requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./Master/app/hashes.txt .

COPY . .


CMD ["uvicorn", "Master.app.master_server:app", "--host", "0.0.0.0" ,"--port", "8000"]