FROM python:3.8.2-buster
WORKDIR /app
COPY . .
RUN pip install flask
ENV FLASK_APP "app.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True
CMD ["flask", "run", "--host", "0.0.0.0"]
