FROM python:3.10-slim
WORKDIR /app
COPY server_train/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
RUN mkdir -p model_output
CMD ["uvicorn", "trainer_server:app", "--host", "0.0.0.0", "--port", "8000"]