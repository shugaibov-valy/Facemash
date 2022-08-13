FROM python:3.9-slim



COPY . /Facemash/

RUN pip3 install -r requirements.txt

CMD ["python3", "Facemash/run_server.py"]
