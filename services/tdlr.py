import pandas as pd

tdlr_df = pd.read_csv("services/TDLR_All_Licenses_20250512.csv", low_memory=False)

def verify_license(name: str = None, license_number: str = None):
    if license_number:
        match = tdlr_df[tdlr_df["LICENSE NUMBER"] == license_number]
    elif name:
        match = tdlr_df[tdlr_df["BUSINESS NAME"].str.contains(name, case=False, na=False)]
    else:
        return False, None

    if not match.empty:
        return True, match.iloc[0]["LICENSE NUMBER"]
    return False, None