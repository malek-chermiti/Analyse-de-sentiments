"""Chargement des partitions du jeu de données Allociné."""

import pandas as pd
from datasets import load_dataset


def charger() -> dict[str, pd.DataFrame]:
    """Charge train, validation et test dans des DataFrames."""
    jeu = load_dataset("tblard/allocine")
    partitions = {}

    for nom_source, nom_sortie in (
        ("train", "train"),
        ("validation", "val"),
        ("test", "test"),
    ):
        if nom_source not in jeu:
            raise ValueError(
                f"La partition « {nom_source} » est absente du jeu de données."
            )

        dataframe = jeu[nom_source].to_pandas()

        if "review" not in dataframe.columns:
            if "text" not in dataframe.columns:
                raise ValueError(
                    f"La partition « {nom_source} » doit contenir "
                    "une colonne « review » ou « text »."
                )
            dataframe = dataframe.rename(columns={"text": "review"})

        if "label" not in dataframe.columns:
            raise ValueError(
                f"La partition « {nom_source} » ne contient pas "
                "la colonne « label »."
            )

        partitions[nom_sortie] = dataframe[["review", "label"]]

    return partitions
