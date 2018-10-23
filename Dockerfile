FROM python:3.7-alpine AS base

FROM base AS git
RUN apk add --no-cache git
RUN git clone https://github.com/n0madic/gitlab-registry-images-cleaner /app

FROM base

RUN pip install pipenv

WORKDIR /app
COPY --from=git /app/gricleaner.py .

EXPOSE 8000
STOPSIGNAL SIGKILL
CMD ["/app/gitlab-registry-cleanup-hook.py"]

# Install app dependencies
COPY Pipfile* ./
RUN pipenv install --system --deploy

# Copy rest of the app
COPY gitlab-registry-cleanup-hook.py .
