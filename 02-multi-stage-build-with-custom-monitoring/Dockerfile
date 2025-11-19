
# Stage 1: Builder Stage
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED 1

WORKDIR /project

COPY requirements.txt /project
RUN pip3 install --no-cache-dir -r requirements.txt


# Stage 2: Final production stage
FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache shadow && groupadd -r project_group && useradd -r -g project_group project_user && apk del shadow
USER project_user

WORKDIR /project

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=project_user:project_user app.py /project

EXPOSE 5000

CMD ["python3", "app.py"]
