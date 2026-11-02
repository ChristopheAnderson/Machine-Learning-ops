# -*- coding: utf-8 -*-
"""
SovereignMLOps & Audio-IA Exploitation Hub — Application Interactive Streamlit
Concepteur : Ing. Christophe WAVOEKE (Bac+5 ENSGMM / UNSTIM — Lauréat Prix Route de la Soie)
"""
import pandas as pd
import streamlit as st

from src.module1_supervised_services_orchestrator import get_supervised_topology, simulate_incident_recovery
from src.module2_airgap_sovereign_deployer import inspect_airgap_bundle
from src.module3_embedded_db_security_audit import simulate_aes256_gcm_envelope, build_and_verify_embedded_audit_chain
from src.module4_audio_asr_diarization_qa import run_audio_asr_diarization_pipeline
from src.module5_cicd_versioning_scaling_runbook import plan_datacenter_scaling, get_internal_operational_runbooks

st.set_page_config(
    page_title="SovereignMLOps & Audio-IA Hub — Ing. Christophe WAVOEKE",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 100%);color:white;padding:18px 24px;border-radius:12px;margin-bottom:16px;">
        <h2 style="margin:0;color:#ffffff;">🛡️ SovereignMLOps & Audio-IA Exploitation Hub (v3.2.0-airgap)</h2>
        <p style="margin:6px 0 0 0;color:#bae6fd;font-size:14px;">
            <strong>Ing. Christophe WAVOEKE</strong> (Ingénieur de Conception Bac+5 — Lauréat ENSGMM / UNSTIM) ·
            Déploiement, Exploitation Souveraine Hors Ligne, Sécurité SQLCipher/AES-256, Chaîne Audio (ASR Whisper & Diarisation Pyannote) & Runbooks d'Exploitation
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs([
    "1️⃣ Services Supervisés & Reprise Incident",
    "2️⃣ Exploitation Souveraine Hors Ligne",
    "3️⃣ Base Embarquée, Chiffrement & Audit",
    "4️⃣ Chaîne Audio (ASR & Diarisation)",
    "5️⃣ CI/CD, Montée en Charge & Runbooks",
])

with tabs[0]:
    st.subheader("Orchestration de Services Supervisés, Ordre de Démarrage (DAG) & Contrôles Quotidiens")
    df_topo = pd.DataFrame(get_supervised_topology())
    st.dataframe(df_topo, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        scenario = st.selectbox(
            "Scénario d'incident à simuler :",
            ["OOM_WORKER_CRASH", "BATCH_INTERRUPT_POWER", "DB_LOCK_CONTENTION"],
        )
    with col2:
        backoff = st.slider("Délai initial d'Exponential Backoff (secondes)", 1.0, 5.0, 2.0, 0.5)

    sim = simulate_incident_recovery(failure_type=scenario, backoff_base_sec=backoff)
    c1, c2, c3 = st.columns(3)
    c1.metric("MTTR Mesuré", f"{sim['measured_mttr_sec']} s", "Conforme SLA (< 45s)")
    c2.metric("Service Cible", sim["affected_service"])
    c3.metric("Intégrité des Données", sim["data_integrity_guarantee"])
    st.json(sim)

with tabs[1]:
    st.subheader("Exploitation Hors Ligne (Air-Gapped), Mises à Jour par Lots, RBAC & Sauvegardes")
    bundle = inspect_airgap_bundle()
    b1, b2, b3 = st.columns(3)
    b1.metric("Taille Bundle Hors Ligne", f"{bundle['total_size_gb']} Go", "Zéro accès Internet")
    b2.metric("RPO Mesuré (Sauvegarde WAL)", f"{bundle['backup_restore_protocol']['measured_rpo_minutes']} min")
    b3.metric("RTO Mesuré (Restauration)", f"{bundle['backup_restore_protocol']['measured_rto_minutes']} min")
    st.write("**Artefacts du paquet hors ligne signés (SHA-256 / Ed25519) :**")
    st.dataframe(pd.DataFrame(bundle["artifacts"]), use_container_width=True)
    st.write("**Matrice de contrôle d'accès à moindre privilège (RBAC Linux) :**")
    st.dataframe(pd.DataFrame(bundle["rbac_access_matrix"]), use_container_width=True)

with tabs[2]:
    st.subheader("Base de Données Embarquée (SQLCipher WAL), Chiffrement AES-256-GCM & Audit Chaîné")
    sample_text = st.text_input(
        "Donnée sensible à chiffrer (Enveloppe AES-256-GCM) :",
        "NPI:2026991842 | Transcription Confidentielle Séance PSID — Cotonou",
    )
    tamper = st.checkbox("Simuler une tentative d'altération frauduleuse sur la ligne #2 du journal d'audit", value=False)
    enc = simulate_aes256_gcm_envelope(sample_text)
    audit = build_and_verify_embedded_audit_chain(tamper_test=tamper)

    if audit["hash_chain_integrity_verified"]:
        st.success("✔ Chaîne de hachage cryptographique d'audit intègre (100% des entrées HMAC-SHA256 validées).")
    else:
        st.error(f"🚨 Altération détectée par vérification HMAC sur la séquence #{audit['detected_tampered_row']} !")

    st.write("**Enveloppe Chiffrée AES-256-GCM :**")
    st.json(enc)
    st.write("**Registre d'Audit Immuable (SQLite WAL / SQLCipher) :**")
    st.dataframe(pd.DataFrame(audit["ledger_entries"]), use_container_width=True)

with tabs[3]:
    st.subheader("Chaîne Audio Souveraine : Transcription (Faster-Whisper v3) & Diarisation (Pyannote 3.1)")
    snr_val = st.slider("Rapport Signal/Bruit d'entrée (SNR en dB)", 8.0, 35.0, 21.5, 0.5)
    conf_thr = st.slider("Seuil minimal de confiance ASR (Contrôle Qualité)", 0.65, 0.95, 0.80, 0.01)
    audio_res = run_audio_asr_diarization_pipeline(snr_input_db=snr_val, min_confidence_threshold=conf_thr)
    qm = audio_res["quality_control_metrics"]

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Vitesse d'Inférence", qm["speedup_vs_realtime"], f"RTF = {qm['real_time_factor_rtf']}")
    a2.metric("Erreur Diarisation (DER)", f"{qm['estimated_diarization_error_rate_der_pct']} %")
    a3.metric("Erreur Transcription (WER)", f"{qm['estimated_word_error_rate_wer_pct']} %")
    a4.metric("Confiance Moyenne ASR", f"{qm['mean_asr_confidence'] * 100:.1f} %")

    st.dataframe(pd.DataFrame(audio_res["diarized_segments"]), use_container_width=True)

with tabs[4]:
    st.subheader("Industrialisation CI/CD Hors Ligne, Montée en Charge Multi-Nœuds & Runbooks Internes")
    u_col1, u_col2, u_col3 = st.columns(3)
    with u_col1:
        units = st.slider("Nombre d'unités de calcul en Centre de Données", 1, 16, 4)
    with u_col2:
        u_type = st.selectbox("Profil Matériel par Nœud", ["NODE_GPU_L4_24GB", "NODE_GPU_T4_16GB", "NODE_CPU_EPYC_32C"])
    with u_col3:
        ha_mode = st.checkbox("Haute Disponibilité N+1 active", value=True)

    scaling = plan_datacenter_scaling(compute_units=units, unit_type=u_type, ha_redundancy_n_plus_1=ha_mode)
    s1, s2, s3 = st.columns(3)
    s1.metric("Capacité Audio / Heure", f"{scaling['consolidated_capacity']['audio_hours_processed_per_hour']} h/h")
    s2.metric("Capacité Audio / 24h", f"{scaling['consolidated_capacity']['audio_hours_processed_per_24h']} h/jour")
    s3.metric("Débit API ML Consolidé", f"{scaling['consolidated_capacity']['ml_inference_requests_per_second']} req/s")

    st.write("**Procédures d'Exploitation Standardisées (Runbooks Internes — Livrable 2) :**")
    for rb in get_internal_operational_runbooks():
        with st.expander(f"📘 {rb['runbook_id']} — {rb['title']} (SLA : {rb['sla_target']})"):
            for step in rb["steps"]:
                st.markdown(f"- {step}")

