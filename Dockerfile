FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
RUN useradd --create-home --uid 10001 appuser
USER appuser
EXPOSE 8000
CMD ["python", "-m", "fde_capstone.cli", "demo", "--db", "/tmp/fde-capstone.db"]
