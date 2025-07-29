FROM python:3.10-slim
WORKDIR /app
COPY server_predict/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "predict_server:app", "--host", "0.0.0.0", "--port", "8001"]