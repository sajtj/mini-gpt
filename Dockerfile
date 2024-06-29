# for deployment environment
FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./ /code/

EXPOSE 80

CMD ["uvicorn", "main:app"]