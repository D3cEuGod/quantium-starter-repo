from pathlib import Path
import pandas as pd

# folder containing the three csv files
data_folder = Path("data")

# read all csv files in the data folder
frames = []
for csv_file in data_folder.glob("*.csv"):
    df = pd.read_csv(csv_file)
    frames.append(df)

# combine into one dataframe
df = pd.concat(frames, ignore_index=True)

# keep only Pink Morsels rows
df = df[df["product"].astype(str).str.strip().str.lower() == "pink morsel"]

# clean quantity and price, then calculate sales
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

df["Sales"] = df["quantity"] * df["price"]

# keep only required output columns
output_df = df[["Sales", "date", "region"]].copy()
output_df.columns = ["Sales", "Date", "Region"]

# save final output file
output_df.to_csv("formatted_output.csv", index=False)

print("formatted_output.csv created successfully")