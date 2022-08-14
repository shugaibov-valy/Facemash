FROM python:3.9-slim



COPY . /Facemash/
WORKDIR /Facemash
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
