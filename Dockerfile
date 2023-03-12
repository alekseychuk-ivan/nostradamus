FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

#RUN pip install --no-cache
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /code

#EXPOSE 80
# http://127.0.0.1:8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]