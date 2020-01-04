import pandas as pd


def load_file(file):
    return pd.read_excel(r"%s" % file)


def scrub_file(file):
    """
    Cleans the file by filling the null cells, gives the proper name to the 
    columns and make formatting changes for Date.
    """
    file = file.dropna(axis=1, how="all")
    file = file[~pd.isnull(file["Transaction Type"])]
    file = file[
        [
            "Date",
            "Transaction Type",
            "Num",
            "Name",
            "Memo/Description",
            "Split",
            "Debit",
            "Credit",
        ]
    ]
    file["Date"] = pd.to_datetime(file["Date"]).apply(lambda x: x.strftime("%m/%d/%Y"))
    file[["Debit", "Credit"]] = file[["Debit", "Credit"]].fillna(0)
    file["Net"] = file["Debit"] - file["Credit"]
    file = file.reset_index(drop=True)
    file = file.fillna("NA")
    return file


def summary(file):
    """
    Summarize the General Ledger by transaction type.
    """
    return (
        file.groupby("Transaction Type")["Debit", "Credit", "Net"].sum().round(1).abs()
    )


def check_unbalanced_entries(file, trans_type):
    """
    Returns the dataframe with unbalanced journal entries and an empty 
    dataframe in case when there is none.
    """
    df_specific = file[file["Transaction Type"] == trans_type]
    df_net = pd.DataFrame(
        df_specific.groupby("Date")["Net"].sum().round(1).abs()
    )  # net of journal entries on specific date
    if df_net[df_net.Net != 0].empty:
        return pd.DataFrame([])
    else:
        return df_net[df_net.Net == 0].index


def check_entries_weekend(file, val):
    """
    Returns the dataframe with the entries on the weekend selected.
    The most basic reason to check this is because typically people don't make
    entries on weekend.
    """
    df = file[
        (file["Transaction Type"] != "Invoice")
        & (file["Transaction Type"] != "Payment")
    ]  # invoice can be made anyday because it comes from the actual sale of the prodcuts.
    grouped = df[pd.to_datetime(df.Date).dt.dayofweek > 5].groupby(
        ["Date", "Transaction Type"]
    )
    df_transform = pd.concat([df for group, df in grouped if group[0] == val])
    df_transform = pd.DataFrame(
        df_transform.groupby(["Date", "Transaction Type"])[
            "Date", "Transaction Type", "Credit", "Debit"
        ]
        .sum()
        .round(1)
        .abs()
    ).reset_index()
    return df_transform


def check_high_dollar(file, val):
    """
    Check if the entry is higher than certain amount provided as a value. Again 
    the motive is to check the authenticity of the big dollar entries as sometimes
    people from managemnt can make these entries to hide a corrupt motive.
    """
    df = pd.DataFrame(
        file.groupby(["Date", "Transaction Type"])["Credit", "Debit"].sum().abs()
    )
    df = df.reset_index()
    return df[(df.Credit > val) | (df.Debit > val)]


def check_round_dollar(file):
    """
    returns recorded journal entries which are the exact multiple of 100s. 
    Round number testing is relevant to AU-C Section 240; AU-C Section 315, 
    Understanding the Entity and Its Environment and Assessing the Risks of 
    Material Misstatement; and AU-C Section 520, Analytical Procedures.
    """
    df = pd.DataFrame(
        file.groupby(["Date", "Transaction Type"])["Credit", "Debit"].sum()
    )
    return df[((df.Credit % 100) == 0) | ((df.Debit % 100) == 0)]


def obtain_sample(file, val):
    """
    return a dataframe with a sample of journal entries. Number of journal entries
    returned are based on the value provided.
    """
    df = pd.DataFrame(
        file.groupby(["Date", "Transaction Type"])["Credit", "Debit"].sum()
    )
    return df.sample(val).reset_index()


def check_by_month(file, val):
    """
    return a dataframe with journal entries in a particular month.
    """
    df = pd.DataFrame(
        file.groupby(["Date", "Transaction Type"])["Credit", "Debit"].sum()
    )
    df.reset_index(inplace=True)
    return df[pd.to_datetime(df["Date"]).dt.month_name() == val]


def scatter_data(file):
    """
    return the data for the scatter plot for both debits and credits. It would
    be a visual method to see the values of debits and credits. One can find out
    what is the highest dollar entry or around what value it lies.
    """
    df = pd.DataFrame(
        file.groupby(["Date", "Transaction Type"])["Credit", "Debit"].sum()
    )
    return df.Debit.tolist(), df.Credit.tolist(), list(range(1, 1+len(df)))