import numpy as np
import pandas as pd
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scipy import sparse


class Recommender():
    def __init__(self, df):
        self.df = df
        self.stop_words = get_stop_words("es")
        self.similarity = None

    def train(self):
        count = CountVectorizer(stop_words=self.stop_words)
        name_mat = count.fit_transform(self.df["name"])
        name_sim = linear_kernel(name_mat, name_mat, dense_output=False)
        name_sim = name_sim / np.max(name_sim)

        tfidf = TfidfVectorizer(stop_words=self.stop_words)
        description_mat = tfidf.fit_transform(self.df["description"])
        description_sim = linear_kernel(description_mat, description_mat, dense_output=False)

        price_sim = np.array(
            [[abs(price1 - price2) for price1 in self.df["price"]]
            for price2 in self.df["price"]]
        )
        price_sim = 1 - price_sim / self.df["price"].max()
        price_sim = sparse.csr_matrix(price_sim)

        discount_sim = [disc for disc in self.df["discount"]]
        discount_sim = np.tile(discount_sim, (self.df.shape[0], 1))
        discount_sim = discount_sim / max(self.df["discount"])
        discount_sim = sparse.csr_matrix(discount_sim)

        random_sim = sparse.csr_matrix(np.random.rand(self.df.shape[0], self.df.shape[0]))

        self.similarity = 0.3*name_sim + 0.3*description_sim + 0.3*random_sim

        return self

    def recommend(self, url):
        if self.similarity is None:
            raise AttributeError("The Recommender is not trained.")

        indexes = pd.Series(self.df.index, index=self.df["url"])
        index = indexes[url]

        scores = list(enumerate(self.similarity.toarray()[index]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = [s[0] for s in scores]
        scores.insert(0, scores.pop(scores.index(index)))

        return self.df[["url", "name_original", "image"]].iloc[scores[0:6]].values

if __name__ == "__main__":
    df = pd.read_csv("train_data.csv")
    reco = Recommender(df)

    reco.train()

    # Example
    output = reco.recommend(
        "https://www.microplay.cl/producto/llavero-dragon-ball-z-kame-symbol-3d/"
    )
    print(output)
