import re

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd

df_original = pd.read_csv("~/Desktop/clubsnap.csv", sep=",", error_bad_lines=False)

df = df_original

df['title_cleaned'] = [re.sub(r'[^\w]', ' ', str(text)) for text in df['title']]
df['title_cleaned'] = df.title_cleaned.str.lower()

df.to_csv('~/Desktop/clubsnap_cleaned.csv')
