import pandas as pd

def convert_parquet_to_csv(input_file, output_file):
    # Functie care converteste un fisier Parquet in CSV
    df = pd.read_parquet(input_file, engine="pyarrow")
    df.to_csv(output_file, index=False)
    print(f"Conversie finalizata: {output_file}")
    return df

if __name__ == "__main__":
    input_file = "logos.snappy.parquet"
    output_file = "logos2.csv"
    convert_parquet_to_csv(input_file, output_file)