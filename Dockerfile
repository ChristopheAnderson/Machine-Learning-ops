# ==============================================================================
# Dockerfile — SovereignMLOps & Audio-IA Exploitation Hub (Air-Gap Ready)
# Concepteur : Ing. Christophe WAVOEKE
# ==============================================================================
FROM python:3.11-slim-bookworm

LABEL maintainer="Ing. Christophe WAVOEKE <christophewavoeke18@gmail.com>"
LABEL description="Sovereign MLOps, Embedded Encrypted DB, Offline CI/CD & Audio ASR/Diarization Hub"
LABEL version="3.2.0-airgap"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SOVEREIGN_AIRGAP_MODE=1 \
    SQLCIPHER_WAL_MODE=1

WORKDIR /opt/asin-mlops-hub

# Création d'un utilisateur système non-privilégié (Moindre privilège RBAC)
RUN groupadd -g 1040 asin_ops && useradd -u 1040 -g asin_ops -m -s /bin/bash exploitant_ia_asin

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R exploitant_ia_asin:asin_ops /opt/asin-mlops-hub

USER exploitant_ia_asin
EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health')" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

