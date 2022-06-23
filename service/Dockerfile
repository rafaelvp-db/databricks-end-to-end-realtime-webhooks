FROM python:3.8.13-slim-buster as builder

RUN mkdir /app && mkdir /model
RUN groupadd -r mymodel && useradd -r -s /bin/false -g mymodel mymodel
WORKDIR /app

#Copy dependency lists & artifacts
COPY . /app
COPY ./requirements_api.txt /tmp/requirements_api.txt
COPY ./ml_artifacts/model/requirements.txt /tmp/requirements_model.txt
COPY ./ml_artifacts/model /model
COPY ./requirements_api.txt /tmp/requirements_api.txt
COPY ./ml_artifacts/model/requirements.txt /tmp/requirements_model.txt
RUN chown -R mymodel:mymodel /app && chown -R mymodel:mymodel /model
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements_api.txt \
    && pip install --no-cache-dir -r /tmp/requirements_model.txt

#Runtime

FROM builder as prod
USER mymodel
WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]