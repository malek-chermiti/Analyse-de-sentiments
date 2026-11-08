"""Chemins communs du projet."""

from pathlib import Path


RACINE_PROJET = Path(__file__).resolve().parents[2]
DOSSIER_DATA = RACINE_PROJET / "data"
DOSSIER_BRUT = DOSSIER_DATA / "raw"
DOSSIER_PREPARE = DOSSIER_DATA / "processed"
DOSSIER_MODELES = RACINE_PROJET / "models"
DOSSIER_FIGURES = RACINE_PROJET / "outputs" / "figures"
