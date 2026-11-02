# -*- coding: utf-8 -*-
"""
SovereignMLOps & Audio-IA Exploitation Hub — API FastAPI & Simulateur Web Interactif
Concepteur : Ing. Christophe WAVOEKE (Ingénieur de Conception Bac+5 — Lauréat ENSGMM / UNSTIM)
"""
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

from src.module1_supervised_services_orchestrator import get_supervised_topology, simulate_incident_recovery
from src.module2_airgap_sovereign_deployer import inspect_airgap_bundle
from src.module3_embedded_db_security_audit import simulate_aes256_gcm_envelope, build_and_verify_embedded_audit_chain
from src.module4_audio_asr_diarization_qa import run_audio_asr_diarization_pipeline
from src.module5_cicd_versioning_scaling_runbook import plan_datacenter_scaling, get_internal_operational_runbooks

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="SovereignMLOps & Audio-IA Exploitation Hub — ASIN Bénin",
    description=(
        "Plateforme industrielle de mise en production, d'exploitation souveraine hors ligne et de supervision IA : "
        "(1) Orchestration de services supervisés (Service de données, API, Traitement par lots), ordre de démarrage DAG, "
        "reprise après incident et contrôles quotidiens ; "
        "(2) Exploitation hors ligne (Air-Gapped), mises à jour atomiques par lots, RBAC et sauvegarde/restauration ; "
        "(3) Base de données embarquée SQLCipher WAL, chiffrement AES-256-GCM et journalisation d'audit par chaîne de hachage ; "
        "(4) Chaîne Audio Souveraine (Transcription Faster-Whisper Large-v3 & Diarisation Pyannote 3.1 avec contrôle qualité) ; "
        "(5) Industrialisation CI/CD hors ligne, versionnage conjoint Modèles/Configs, montée en charge multi-nœuds et Runbooks."
    ),
    version="3.2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


def _read_html(filename: str) -> str:
    target = BASE_DIR / filename
    if target.exists():
        return target.read_text(encoding="utf-8")
    return f"<h1>Fichier {filename} introuvable</h1>"


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/index.html", response_class=HTMLResponse, include_in_schema=False)
@app.get("/portal", response_class=HTMLResponse, include_in_schema=False)
def serve_index():
    return HTMLResponse(content=_read_html("index.html"))


@app.get("/docs.html", response_class=HTMLResponse, include_in_schema=False)
@app.get("/runbook", response_class=HTMLResponse, include_in_schema=False)
def serve_docs():
    return HTMLResponse(content=_read_html("docs.html"))


@app.get("/assets/{filename:path}", include_in_schema=False)
def serve_assets(filename: str):
    file_path = BASE_DIR / "assets" / filename
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return JSONResponse({"error": "Asset not found"}, status_code=404)


@app.get("/api/v1/health", tags=["Santé & Supervision Quotidienne"])
def health_check():
    return {
        "status": "operational",
        "service": "sovereign-mlops-exploitation-hub",
        "version": "3.2.0-airgap",
        "author": "Ing. Christophe WAVOEKE (Bac+5 ENSGMM/UNSTIM — Lauréat Prix Route de la Soie)",
        "modules": [
            "Module 1 : Services supervisés (Données, API, Batch), ordre de démarrage DAG, reprise après incident & contrôles quotidiens",
            "Module 2 : Exploitation souveraine hors ligne (Air-Gapped), mises à jour par lots, RBAC & sauvegarde/restauration",
            "Module 3 : Base de données embarquée SQLCipher WAL, chiffrement AES-256-GCM & journalisation d'audit infalsifiable",
            "Module 4 : Chaîne Audio Souveraine (Transcription Faster-Whisper Large-v3 & Diarisation Pyannote 3.1 + Contrôle Qualité)",
            "Module 5 : Industrialisation CI/CD hors ligne, versionnage conjoint Modèles/Configs, montée en charge & Runbook interne",
        ],
    }


@app.get("/api/v1/module1/supervised-services", tags=["Module 1 — Services Supervisés & Reprise Incident"])
def api_supervised_services(
    failure_type: str = Query("OOM_WORKER_CRASH", description="Scénario d'incident à simuler"),
    backoff_base_sec: float = Query(2.0, ge=0.5, le=10.0),
):
    return {
        "topology": get_supervised_topology(),
        "incident_recovery_simulation": simulate_incident_recovery(
            failure_type=failure_type, backoff_base_sec=backoff_base_sec
        ),
    }


@app.get("/api/v1/module2/airgap-bundle", tags=["Module 2 — Exploitation Hors Ligne (Air-Gap)"])
def api_airgap_bundle(bundle_version: str = Query("v3.2.0-sovereign")):
    return inspect_airgap_bundle(bundle_version=bundle_version)


@app.get("/api/v1/module3/embedded-db-security", tags=["Module 3 — Base Embarquée, Chiffrement & Audit"])
def api_embedded_db_security(
    sample_sensitive_data: str = Query("NPI:2026991842|Transcription_Confidentielle_ASIN"),
    tamper_test: bool = Query(False, description="Simuler une tentative d'altération du journal d'audit"),
):
    return {
        "encryption_envelope": simulate_aes256_gcm_envelope(sample_sensitive_data),
        "audit_chain_verification": build_and_verify_embedded_audit_chain(tamper_test=tamper_test),
    }


@app.get("/api/v1/module4/audio-asr-diarization", tags=["Module 4 — Chaîne Audio (ASR & Diarisation)"])
def api_audio_pipeline(
    snr_db: float = Query(21.5, ge=5.0, le=40.0, description="Rapport Signal/Bruit (SNR en dB)"),
    min_confidence: float = Query(0.80, ge=0.50, le=0.98),
):
    return run_audio_asr_diarization_pipeline(
        audio_duration_sec=42.0, snr_input_db=snr_db, min_confidence_threshold=min_confidence
    )


@app.get("/api/v1/module5/scaling-and-runbook", tags=["Module 5 — Industrialisation, Montée en Charge & Runbook"])
def api_scaling_and_runbook(
    compute_units: int = Query(4, ge=1, le=32),
    unit_type: str = Query("NODE_GPU_L4_24GB"),
    ha_n_plus_1: bool = Query(True),
):
    return {
        "datacenter_scaling": plan_datacenter_scaling(
            compute_units=compute_units, unit_type=unit_type, ha_redundancy_n_plus_1=ha_n_plus_1
        ),
        "operational_runbooks": get_internal_operational_runbooks(),
    }

