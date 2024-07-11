FROM python:alpine
WORKDIR /code
ENV FLASK_APP=app.py 
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk update && \
    apk add curl \
    rm -rf /var/cache/apk/*
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 8068
COPY . .
CMD ["flask", "run", "--debug"]
