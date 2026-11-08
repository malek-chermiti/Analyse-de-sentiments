# Allocine sentiment-analysis data preparation

This project prepares the French Allocine movie-review dataset for a later
sentiment-classification task. It checks the source partitions, cleans review
text, creates TF-IDF features, and saves exploratory plots.

## Requirements

- Python 3.9 or newer (the code uses built-in generic type annotations; a newer
  version may be required by the latest releases of the dependencies).
- The Python packages listed in [`requirements.txt`](requirements.txt):
  `datasets`, `pandas`, `scikit-learn`, `joblib`, and `matplotlib`.
- Internet access when running the pipeline: `charger.py` loads
  [`tblard/allocine` from Hugging Face](https://huggingface.co/datasets/tblard/allocine).
  The first run downloads the dataset; the Hugging Face `datasets` library
  caches it locally for later runs.

The three original CSV partitions are also included in `data/raw/` in this
repository. **The current script does not read those local CSVs**; it loads the
dataset from Hugging Face instead. Therefore, a network connection (or a
previously populated Hugging Face cache) is still needed to run it as written.
The source dataset's provenance and terms of use are described on its Hugging
Face page.

## Setup

Run these commands from the repository root.

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the preparation pipeline

With the virtual environment activated, run:

```text
python preparation.py
```

The pipeline downloads or loads the `train`, `validation`, and `test`
partitions, keeps the review text and sentiment label, and saves the original
partitions to `data/raw/`. It then removes rows with missing reviews or labels,
exact duplicates, and reviews shorter than three words. It adds a `clean`
column by lowercasing text, removing URLs and HTML tags, decoding HTML
entities, and normalizing punctuation and whitespace. Apostrophes, negations,
and stop words are retained.

TF-IDF is fitted on the training partition only, with unigrams and bigrams and
up to 50,000 features; that fitted vectorizer is then applied to validation and
test. The script prints the resulting matrix dimensions. It does not train a
sentiment classifier.

## Generated files

Running the script creates or updates:

| Path | Contents |
| --- | --- |
| `data/raw/train.csv`, `data/raw/val.csv`, `data/raw/test.csv` | Original review and label partitions |
| `data/processed/train.csv`, `data/processed/val.csv`, `data/processed/test.csv` | Cleaned partitions, including the `clean` text column |
| `models/tfidf.pkl` | Fitted scikit-learn TF-IDF vectorizer (not a classifier) |
| `outputs/figures/repartition_labels.png` | Label counts by partition |
| `outputs/figures/longueur_avis_train.png` | Training-review word-count histogram |
| `outputs/figures/longueur_par_sentiment_train.png` | Training-review word-count comparison by label |

`data/processed/` and `models/` are excluded from Git because they are
reproducible generated artifacts. Raw CSVs, source code, and the plot PNGs are
included in the repository. The report in [`reports/rapport_phase1.md`](reports/rapport_phase1.md)
describes the project and the exploratory analysis.
