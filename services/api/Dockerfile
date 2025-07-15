FROM python:3.11-slim-bookworm


# Install regular dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==2.1.3

# Add user
RUN useradd -m -s /bin/bash api && \
    echo 'api:api' | chpasswd && \
    echo 'api ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers

# Install api dependencies
USER api
WORKDIR /home/api/app

COPY --chown=api:api pyproject.toml .
RUN poetry install --no-root

COPY --chown=api:api . .
RUN poetry install

CMD ["poetry", "run", "api"]