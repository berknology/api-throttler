FROM python:3.8

WORKDIR /opt

COPY requirements /opt/requirements/

ARG env=dev
RUN pip install -r requirements/$env.txt

COPY . .

EXPOSE 80

CMD ["python", "app.py"]