"""Contrôle qualité des partitions du jeu de données."""

import pandas as pd


def controler(partitions: dict[str, pd.DataFrame]) -> None:
    """Affiche les informations de qualité pour chaque partition."""
    for nom, dataframe in partitions.items():
        print(f"\n--- Contrôle qualité : {nom} ---")
        dataframe.info()
        print("\nRépartition des labels :")
        print(dataframe["label"].value_counts(dropna=False))
        longueurs = dataframe["review"].map(
            lambda texte: len(texte.split()) if isinstance(texte, str) else 0
        )
        print("\nLongueur des textes (nombre de mots) :")
        print(longueurs.describe())
        print(f"\nDoublons : {dataframe.duplicated().sum()}")
        print(f"Valeurs manquantes :\n{dataframe.isna().sum()}")
