FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --no-install-project
COPY . .
RUN uv sync --no-dev
EXPOSE 8000
CMD ["uv", "run", "--no-dev", "fastapi", "run", "src/__PACKAGE__/main.py", "--port", "8000"]
