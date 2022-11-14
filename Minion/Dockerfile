FROM python:3.9

WORKDIR /app

COPY ./Minion/requirements.txt .
RUN pip install -r ./requirements.txt

COPY . .


CMD ["uvicorn", "Minion.app.minion_server:app", "--host", "0.0.0.0" ,"--port", "80"]