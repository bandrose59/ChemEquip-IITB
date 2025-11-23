import pandas as pd

REQUIRED_COLUMNS = ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]

def validate_and_parse_csv(file):
    df = pd.read_csv(file)

    # Validate
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df["Flowrate"] = pd.to_numeric(df["Flowrate"], errors="coerce")
    df["Pressure"] = pd.to_numeric(df["Pressure"], errors="coerce")
    df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")

    summary = {
        "total": len(df),
        "averages": {
            "flowrate": df["Flowrate"].mean(),
            "pressure": df["Pressure"].mean(),
            "temperature": df["Temperature"].mean(),
        },
        "type_distribution": df["Type"].value_counts().to_dict(),
    }

    return df, summary
