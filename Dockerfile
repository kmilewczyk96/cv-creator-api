FROM python:3.14-alpine
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_SYSTEM_PIP=1
WORKDIR /app

RUN apk add --no-cache curl ca-certificates build-base && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv

# Copy only dependency manifests first (enables better Docker layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies based on the lockfile (no dev deps)
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "api.api:api", "--host", "0.0.0.0", "--port", "8000"]
