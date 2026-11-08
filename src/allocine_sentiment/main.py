"""Orchestration du pipeline de préparation Allociné."""

from .charger import charger
from .config import DOSSIER_BRUT, DOSSIER_PREPARE
from .controler import controler
from .nettoyer import nettoyer
from .vectoriser import vectoriser
from .visualiser import visualiser


def main() -> None:
    """Exécute le pipeline et enregistre les données et les livrables."""
    partitions = charger()
    controler(partitions)
    DOSSIER_BRUT.mkdir(parents=True, exist_ok=True)
    for nom, dataframe in partitions.items():
        dataframe.to_csv(DOSSIER_BRUT / f"{nom}.csv", index=False)

    partitions_nettoyees = nettoyer(partitions)
    _, matrice_train, matrice_val, matrice_test = vectoriser(
        partitions_nettoyees
    )

    for nom in ("train", "val", "test"):
        partitions_nettoyees[nom].to_csv(
            DOSSIER_PREPARE / f"{nom}.csv", index=False
        )

    visualiser(partitions_nettoyees)

    print("\nDimensions des matrices TF-IDF :")
    print(f"Train : {matrice_train.shape}")
    print(f"Validation : {matrice_val.shape}")
    print(f"Test : {matrice_test.shape}")
