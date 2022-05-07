import pandas as pd
import spacy


def get_discount(value):
    try:
        output = str(value).split()[1].replace("-", "").replace("%", "")
    except:
        output = 0

    return int(output)

def clean_string(string):
    output = ""

    for letter in string.lower():
        if letter in "abcdefghijklmnñopqrstuvwxyz0123456789áéíóú ":
            output += letter
        else:
            output += " "

    return " ".join([token.lemma_ for token in nlp(" ".join(output.split()))]) + " "


if __name__ == "__main__":
    print("Downloading nlp...")
    nlp = spacy.load("es_core_news_sm")
    print("Done.")

    print("Loading data...")
    df = pd.read_csv("scraper/data.csv")
    print("Done.")

    print("Preprocessing columns...")
    df["price"].fillna(value=-9999, inplace=True)
    df["name"].fillna(value="", inplace=True)
    df["description"].fillna(value="", inplace=True)
    df["discount"] = df["price"].apply(lambda x: get_discount(x))
    df["price"] = df["price"].apply(lambda x: int(str(x).split()[0]))
    df["name"] = df["name"].apply(lambda x: clean_string(x))
    df["description"] = df["description"].apply(lambda x: clean_string(x))
    print("Done.")

    df.to_csv("train_data.csv", index=False)
