FROM python:3-alpine AS base

FROM base AS git
RUN apk add --no-cache git
RUN git clone https://github.com/burnettk/delete-docker-registry-image /app

FROM base

RUN pip install pipenv

WORKDIR /app
COPY --from=git /app/delete_docker_registry_image.py .

# Install app dependencies
COPY Pipfile* ./
RUN pipenv install --system --deploy

# Copy rest of the app
COPY gitlab-registry-cleanup-hook.py .

EXPOSE 8000

CMD ["/app/gitlab-registry-cleanup-hook.py"]
