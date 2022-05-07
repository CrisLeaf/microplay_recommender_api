import numpy as np
import pandas as pd
import spacy
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class Recommendator():
    def __init__(self, df):
        self.df = df
        self.nlp = spacy.load("es_core_news_sm")
        self.stop_words = get_stop_words("es")
        self.similarity = None

    def _get_discount(self, value):
        try:
            output = str(value).split()[1].replace("-", "").replace("%", "")
        except:
            output = 0

        return int(output)

    def _clean_string(self, string):
        output = ""

        for letter in string.lower():
            if letter in "abcdefghijklmnñopqrstuvwxyz0123456789áéíóú ":
                output += letter
            else:
                output += " "

        return " ".join([token.lemma_ for token in self.nlp(" ".join(output.split()))])

    def train(self):
        print("Training...")
        self.df["price"].fillna(value=999999, inplace=True)
        self.df["name"].fillna(value="", inplace=True)
        self.df["description"].fillna(value="", inplace=True)

        self.df["discount"] = self.df["price"].apply(lambda x: self._get_discount(x))
        self.df["price"] = self.df["price"].apply(lambda x: int(str(x).split()[0]))
        self.df["name_cleaned"] = self.df["name"].apply(lambda x: self._clean_string(x))
        self.df["description_cleaned"] = self.df["description"].apply(lambda x: self._clean_string(x))

        tfidf = TfidfVectorizer(stop_words=self.stop_words)
        description_mat = tfidf.fit_transform(self.df["description_cleaned"])
        description_sim = linear_kernel(description_mat, description_mat, dense_output=False)

        count = CountVectorizer(stop_words=self.stop_words)
        name_mat = count.fit_transform(self.df["name_cleaned"])
        name_sim = linear_kernel(name_mat, name_mat, dense_output=False)

        self.similarity = description_sim + name_sim

        return self

    def recommend(self, url):
        if self.similarity is None:
            raise AttributeError("The Recommendator is not trained.")

        indexes = pd.Series(self.df.index, index=self.df["url"])
        index = indexes[url]
        # index = indexes["https://www.microplay.cl/producto/gta-v-grand-theft-auto-v-premium-online-edition-ps4/"]

        scores = list(enumerate(self.similarity.toarray()[index]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = [s[0] for s in scores]
        scores.remove(index)

        return {
            "urls": self.df["url"].iloc[scores[0:5]].values
        }

if __name__ == "__main__":
    df = pd.read_csv("scraper/data.csv")
    reco = Recommendator(df)

    reco.train()
    output = reco.recommend(
        "https://www.microplay.cl/producto/llavero-dragon-ball-z-kame-symbol-3d/"
    )
    print(output)
