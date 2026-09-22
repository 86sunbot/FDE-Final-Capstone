FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir '.[api]'
RUN useradd --create-home --uid 10001 appuser
USER appuser
EXPOSE 8000
ENV FDE_DB=/tmp/fde-capstone.db AI_MODE=off
CMD ["uvicorn", "fde_capstone.api:app", "--host", "0.0.0.0", "--port", "8000"]
