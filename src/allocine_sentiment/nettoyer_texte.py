"""Nettoyage d'un avis sans supprimer les stop-words ni les négations."""

import html
import re
import unicodedata


def nettoyer_texte(texte: str) -> str:
    """Nettoie un avis en conservant les apostrophes."""
    texte = texte.lower()
    texte = re.sub(r"https?://\S+|www\.\S+", " ", texte)
    texte = re.sub(r"<[^>]*>", " ", texte)
    texte = html.unescape(texte)
    texte = re.sub(r"https?://\S+|www\.\S+", " ", texte)
    texte = re.sub(r"<[^>]*>", " ", texte)
    texte = "".join(
        " "
        if unicodedata.category(caractere).startswith("P")
        and caractere not in ("'", "’")
        else caractere
        for caractere in texte
    )
    return re.sub(r"\s+", " ", texte).strip()
