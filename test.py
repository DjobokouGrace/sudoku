import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from wordcloud import WordCloud

# Charger les données
data = pd.read_excel("Discours.xlsm")

# Extraire les mots et leur fréquence pour Obama
words_obama = data["wordsObama"]
frequency_obama = data["Obama"]

# Créer un graphique en barres des mots les plus fréquents pour Obama
plt.bar(words_obama[:10], frequency_obama[:10])
plt.xlabel("Mots")
plt.ylabel("Fréquence")
plt.title("Mots les plus fréquents - Obama")
plt.xticks(rotation=45)
plt.show()


# Extraire les mots et leur fréquence pour Trump
words_trump = data["wordsTrump"]
frequency_trump = data["Trump"]

# Créer un graphique en barres des mots les plus fréquents pour Trump
plt.bar(words_trump[:10], frequency_trump[:10])
plt.xlabel("Mots")
plt.ylabel("Fréquence")
plt.title("Mots les plus fréquents - Trump")
plt.xticks(rotation=45)
plt.show()


# Filtrer les données pour exclure les valeurs booléennes
filtered_words_obama = words_obama[data["Obama"].astype(bool)]

# Concaténer les mots filtrés en une seule chaîne de caractères
text_obama = ' '.join([word for word in filtered_words_obama])

# Créer un nuage de mots pour Obama
wordcloud_obama = WordCloud(width=800, height=400).generate(text_obama)

# Afficher le nuage de mots pour Obama
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_obama, interpolation='bilinear')
plt.axis('off')
plt.title("Nuage de mots - Obama")
plt.show()


# Supprimer les lignes avec des valeurs manquantes dans les colonnes "wordsObama" et "Obama"
data_cleaned = data.dropna(subset=["wordsTrump", "Trump"])

# Concaténer les mots et leur fréquence pour Obama en une seule chaîne de caractères
text_trump = ' '.join([word for word in data_cleaned["wordsTrump"]])

# Créer un nuage de mots pour Obama
wordcloud_trump = WordCloud(width=800, height=400).generate(text_trump)

# Afficher le nuage de mots pour Obama
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_trump, interpolation='bilinear')
plt.axis('off')
plt.title("Nuage de mots - Trump")
plt.show()