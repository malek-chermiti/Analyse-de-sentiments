"""Création de graphiques exploratoires à partir des partitions nettoyées."""

from pathlib import Path

import matplotlib
import pandas as pd

from .config import DOSSIER_FIGURES

matplotlib.use("Agg")

import matplotlib.pyplot as plt


NOMS_LABELS = {0: "Négatif (0)", 1: "Positif (1)"}


def visualiser(partitions: dict[str, pd.DataFrame]) -> None:
    """Enregistre la distribution des classes et des longueurs des avis."""
    DOSSIER_FIGURES.mkdir(parents=True, exist_ok=True)

    _visualiser_repartition_labels(partitions, DOSSIER_FIGURES)
    _visualiser_longueurs(partitions["train"], DOSSIER_FIGURES)


def _visualiser_repartition_labels(
    partitions: dict[str, pd.DataFrame], dossier: Path
) -> None:
    noms_partitions = list(partitions)
    labels = sorted(
        {
            int(label)
            for dataframe in partitions.values()
            for label in dataframe["label"].unique()
        }
    )
    valeurs = [
        [
            int((partitions[nom]["label"] == label).sum())
            for nom in noms_partitions
        ]
        for label in labels
    ]

    figure, axe = plt.subplots(figsize=(8, 5))
    bas = [0] * len(noms_partitions)
    for label, comptes in zip(labels, valeurs):
        axe.bar(
            noms_partitions,
            comptes,
            bottom=bas,
            label=NOMS_LABELS.get(label, f"Label {label}"),
        )
        bas = [total + compte for total, compte in zip(bas, comptes)]

    axe.set_title("Nombre d'avis par partition et par sentiment")
    axe.set_xlabel("Partition")
    axe.set_ylabel("Nombre d'avis")
    axe.legend(title="Sentiment")
    axe.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(dossier / "repartition_labels.png", dpi=150)
    plt.close(figure)


def _visualiser_longueurs(
    dataframe: pd.DataFrame, dossier: Path
) -> None:
    longueurs = dataframe["review"].map(
        lambda texte: len(texte.split()) if isinstance(texte, str) else 0
    )
    figure, axe = plt.subplots(figsize=(8, 5))
    axe.hist(longueurs, bins=50, color="#4472C4", edgecolor="white")
    axe.set_title("Distribution du nombre de mots (train)")
    axe.set_xlabel("Nombre de mots par avis")
    axe.set_ylabel("Nombre d'avis")
    axe.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(dossier / "longueur_avis_train.png", dpi=150)
    plt.close(figure)

    figure, axe = plt.subplots(figsize=(8, 5))
    groupes = [
        dataframe.loc[dataframe["label"] == label, "review"].map(
            lambda texte: len(texte.split()) if isinstance(texte, str) else 0
        )
        for label in sorted(dataframe["label"].unique())
    ]
    noms = [
        NOMS_LABELS.get(int(label), f"Label {label}")
        for label in sorted(dataframe["label"].unique())
    ]
    axe.boxplot(groupes, tick_labels=noms, showfliers=False)
    axe.set_title("Longueur des avis par sentiment (train)")
    axe.set_xlabel("Sentiment")
    axe.set_ylabel("Nombre de mots")
    axe.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(dossier / "longueur_par_sentiment_train.png", dpi=150)
    plt.close(figure)
