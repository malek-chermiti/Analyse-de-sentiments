"""Point d'entrée du pipeline de préparation Allociné."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from allocine_sentiment.main import main


if __name__ == "__main__":
    main()
