"""Filtrage des données et ajout du texte nettoyé."""

import pandas as pd

from .nettoyer_texte import nettoyer_texte


def nettoyer(
    partitions: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    """Retire doublons, valeurs manquantes et avis de moins de trois mots."""
    partitions_nettoyees = {}

    for nom, dataframe in partitions.items():
        resultat = dataframe.dropna(subset=["review", "label"]).copy()
        resultat = resultat.drop_duplicates()
        resultat = resultat[
            resultat["review"].map(lambda texte: len(texte.split()) >= 3)
        ].copy()
        resultat["clean"] = resultat["review"].map(nettoyer_texte)
        partitions_nettoyees[nom] = resultat.reset_index(drop=True)

    return partitions_nettoyees
