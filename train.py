import pandas as pd
from gensim import corpora
from gensim.models import LdaMulticore, CoherenceModel
import ast
import os
import pickle
from tqdm import tqdm
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# ========== CONFIG ==========
DATA_FILE = "data/combined_data.csv"
MODEL_DIR = "models"
CHUNKSIZE = 20000
NUM_TOPICS = 7
PASSES = 10
WORKERS = 2
KEEP_N = 30000
# ============================

os.makedirs(MODEL_DIR, exist_ok=True)

DICT_PATH = os.path.join(MODEL_DIR, "dictionary.dict")
LDA_PATH = os.path.join(MODEL_DIR, "lda.model")
CORPUS_PATH = os.path.join(MODEL_DIR, "corpus.mm")
TEXTS_PATH = os.path.join(MODEL_DIR, "texts.pkl")

# Preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in word_tokenize(text) if word not in stop_words and len(word) > 2]
    return tokens

# -------- Step 1: Build Dictionary --------
def build_dictionary():
    dictionary = corpora.Dictionary()
    total_rows = sum(1 for _ in open(DATA_FILE, encoding="utf-8")) - 1
    total_chunks = (total_rows // CHUNKSIZE) + 1

    df_iter = pd.read_csv(DATA_FILE, chunksize=CHUNKSIZE)
    for chunk in tqdm(df_iter, total=total_chunks, desc="📖 Building Dictionary"):
        # Preprocess raw text if 'tokens' column is not pre-tokenized
        if 'text' in chunk.columns:  # Assuming 'text' is the raw column name
            texts = chunk['text'].apply(preprocess_text).tolist()
        else:
            texts = chunk['tokens'].apply(ast.literal_eval).tolist()
        dictionary.add_documents(texts)

    dictionary.filter_extremes(no_below=10, no_above=0.4, keep_n=KEEP_N)
    dictionary.save(DICT_PATH)
    return dictionary

# -------- Step 2: Corpus Generator --------
class CorpusGenerator:
    def __iter__(self):
        total_rows = sum(1 for _ in open(DATA_FILE, encoding="utf-8")) - 1
        total_chunks = (total_rows // CHUNKSIZE) + 1
        df_iter = pd.read_csv(DATA_FILE, chunksize=CHUNKSIZE)
        for chunk in tqdm(df_iter, total=total_chunks, desc="📦 Streaming Corpus"):
            if 'text' in chunk.columns:
                texts = chunk['text'].apply(preprocess_text).tolist()
            else:
                texts = chunk['tokens'].apply(ast.literal_eval).tolist()
            for text in texts:
                yield dictionary.doc2bow(text)

if __name__ == "__main__":
    # Step 1: Build/load dictionary
    if os.path.exists(DICT_PATH):
        print("📂 Loading existing dictionary...")
        dictionary = corpora.Dictionary.load(DICT_PATH)
    else:
        print("🔨 Building dictionary...")
        dictionary = build_dictionary()
        print(f"✅ Dictionary saved at {DICT_PATH}")

    # Step 2: Prepare Corpus & Save
    print("💾 Serializing corpus to disk...")
    corpus_generator = CorpusGenerator()
    corpora.MmCorpus.serialize(CORPUS_PATH, corpus_generator)
    print(f"✅ Corpus saved at {CORPUS_PATH}")

    # Step 3: Train LDA Model
    print("🚀 Training LDA...")
    corpus = corpora.MmCorpus(CORPUS_PATH)

    lda = LdaMulticore(
        corpus=corpus,
        num_topics=NUM_TOPICS,
        id2word=dictionary,
        passes=PASSES,
        workers=WORKERS,
        chunksize=10000,
        random_state=42
    )

    lda.save(LDA_PATH)
    print(f"✅ LDA model trained and saved at {LDA_PATH}")

    # Step 4: Save Sample Texts for Coherence
    print("📊 Collecting sample texts for evaluation...")
    sample_texts = []

    df_iter = pd.read_csv(DATA_FILE, chunksize=CHUNKSIZE)
    for chunk in tqdm(df_iter, desc="🔍 Sampling Texts"):
        if 'text' in chunk.columns:
            texts = chunk['text'].apply(preprocess_text).tolist()
        else:
            texts = chunk['tokens'].apply(ast.literal_eval).tolist()
        sample_texts.extend(texts)
        if len(sample_texts) >= 50000:  # Increased sample size
            break

    with open(TEXTS_PATH, "wb") as f:
        pickle.dump(sample_texts, f)

    print(f"✅ Sample texts saved at {TEXTS_PATH}")

    # Step 5: Quick Coherence Evaluation
    coherence_model = CoherenceModel(
        model=lda,
        texts=sample_texts,
        dictionary=dictionary,
        coherence="c_v"
    )

    coherence_score = coherence_model.get_coherence()
    print(f"🔎 Quick Coherence Score (c_v): {coherence_score:.4f}")

    # Step 6: Inspect Topics
    for topic_id in range(NUM_TOPICS):
        print(f"Topic {topic_id}: {lda.print_topic(topic_id, topn=10)}")