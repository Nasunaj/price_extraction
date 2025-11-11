FROM  python:3.10-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY ./src /app/src

CMD ["/bin/bash"]