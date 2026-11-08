"""Vectorisation TF-IDF des partitions."""

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from .config import DOSSIER_MODELES


def vectoriser(
    partitions: dict[str, pd.DataFrame],
) -> tuple[TfidfVectorizer, object, object, object]:
    """Ajuste TF-IDF sur train uniquement puis transforme val et test."""
    vectoriseur = TfidfVectorizer(max_features=50000, ngram_range=(1, 2))
    # L'ajustement sur train uniquement évite toute fuite depuis validation ou test.
    matrice_train = vectoriseur.fit_transform(partitions["train"]["clean"])
    matrice_val = vectoriseur.transform(partitions["val"]["clean"])
    matrice_test = vectoriseur.transform(partitions["test"]["clean"])

    DOSSIER_MODELES.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectoriseur, DOSSIER_MODELES / "tfidf.pkl")

    return vectoriseur, matrice_train, matrice_val, matrice_test
