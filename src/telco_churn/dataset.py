
from pathlib import Path
import hashlib
import json
import sys
from importlib.metadata import version

import pandas as pd


def inspect_dataset(source: Path) -> dict:
    """Inspecte un CSV sans modifier les données originales."""

    # calcul empreinte SHA-256 du fichier
    source_hash = hashlib.sha256(
        source.read_bytes()
    ).hexdigest()

    # charger les données
    df = pd.read_csv(source, keep_default_na=False)

    # dimensions du dataset
    rows, columns = df.shape


    column_types = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    # répartition de la variable cible Churn
    target_counts = df["Churn"].value_counts(dropna=False)
    target_proportions = df["Churn"].value_counts(
        normalize=True, dropna=False
    )

    churn_distribution = {
        str(label): {
            "count": int(count),
            "proportion": float(target_proportions[label]),
        }
        for label, count in target_counts.items()
    }

    # détection des identifiants clients en double
    duplicate_ids = int(
        df["customerID"].duplicated().sum()
    )

    # valeurs manquantes reconnues par Pandas
    missing_na = df.isna().sum().astype(int).to_dict()

    # cellules vides ou contenant uniquement des espaces
    whitespace_missing = {}

    for column in df.columns:
        values = df[column].astype("string")
        empty_values = values.str.strip().eq("").fillna(False)
        whitespace_missing[column] = int(empty_values.sum())

    # construire le rapport
    report = {
        "source": {
            "file": source.as_posix(),
            "sha256": source_hash,
        },
        "environment": {
            "python_version": sys.version,
            "pandas_version": version("pandas"),
        },
        "dataset": {
            "rows": rows,
            "columns": columns,
            "column_types": column_types,
        },
        "target": {
            "name": "Churn",
            "distribution": churn_distribution,
        },
        "duplicate_customer_ids": duplicate_ids,
        "missing_values": {
            "na_counts": missing_na,
            "empty_or_whitespace_counts": whitespace_missing,
        },
    }

    return report


def save_report(report: dict, output: Path) -> None:
    """Enregistre le rapport au format JSON."""

    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)


def main() -> None:

    project_root = Path(__file__).resolve().parents[2]

    source = project_root / "data" / "raw" / "telco.csv"
    output = project_root / "reports" / "data_overview.json"

    if not source.is_file():
        raise FileNotFoundError(
            f"Dataset introuvable : {source}"
        )

    report = inspect_dataset(source)
    save_report(report, output)

    print("Inspection terminée avec succès !")
    print(f"Lignes : {report['dataset']['rows']}")
    print(f"Colonnes : {report['dataset']['columns']}")
    print(
        "Doublons customerID :",
        report["duplicate_customer_ids"],
    )
    print(f"Rapport enregistré : {output}")


if __name__ == "__main__":
    main()
