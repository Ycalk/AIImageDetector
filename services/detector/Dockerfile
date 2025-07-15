FROM python:3.11-slim-bookworm


# Install regular dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==2.1.3

# Add user
RUN useradd -m -s /bin/bash detector && \
    echo 'detector:detector' | chpasswd && \
    echo 'detector ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers

# Install detector dependencies
USER detector
WORKDIR /home/detector/app

COPY --chown=detector:detector pyproject.toml .
RUN poetry install --no-root

COPY --chown=detector:detector . .
RUN poetry install

CMD ["poetry", "run", "detector"]