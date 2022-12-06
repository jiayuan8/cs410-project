from nltk.tokenize import word_tokenize
import gensim
import numpy as np
import pandas as pd

def recommend_materials(project_description):
    """ 
    Return list of maps of format:
        "course_link": mat["course_link"],
        "lesson_name": mat["lesson_name"]
    """
    dictionary = gensim.corpora.Dictionary.load("gensim/coursera_gensim_dict.dict")
    tf_idf = gensim.models.TfidfModel.load("gensim/coursera_gensim_tfidf.model")
    sims = gensim.similarities.Similarity.load("gensim/coursera_gensim_sims.sims")

    query_doc = [w.lower() for w in word_tokenize(project_description)]
    query_doc_bow = dictionary.doc2bow(query_doc)

    query_doc_tf_idf = tf_idf[query_doc_bow]
    ranked_lectures = np.argsort(sims[query_doc_tf_idf])[::-1]

    df = pd.read_csv("coursera_data.csv")
    best_lectures_info = df.iloc[ranked_lectures[:5]]

    return [{"course_link": row["course_link"], "lesson_name": row["lesson_name"]} for _, row in best_lectures_info.iterrows()]