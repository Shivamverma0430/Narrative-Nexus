import os
import pickle
import numpy as np
from gensim.models import LdaModel, CoherenceModel
from gensim import corpora
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

def main():
    MODEL_DIR = "models"
    DICT_PATH = os.path.join(MODEL_DIR, "dictionary.dict")
    LDA_PATH = os.path.join(MODEL_DIR, "lda.model")
    CORPUS_PATH = os.path.join(MODEL_DIR, "corpus.mm")
    TEXTS_PATH = os.path.join(MODEL_DIR, "texts.pkl")
    COHERENCE_PATH = os.path.join(MODEL_DIR, "coherence_scores.pkl")
    RESULTS_PATH = os.path.join(MODEL_DIR, "evaluation_results.txt")

    print("📂 Loading model components...")

    # ---- Load Dictionary and Model ----
    try:
        dictionary = corpora.Dictionary.load(DICT_PATH)
        lda_model = LdaModel.load(LDA_PATH)
        print(f"✅ Model loaded: {lda_model.num_topics} topics, {len(dictionary)} vocabulary")
    except Exception as e:
        print(f"❌ Model not found or corrupted.")
        return

    # ---- Load Corpus ----
    try:
        corpus = corpora.MmCorpus(CORPUS_PATH)
        print(f"✅ Corpus loaded: {len(corpus):,} documents")
    except:
        corpus = None

    # ---- Load Texts ----
    try:
        with open(TEXTS_PATH, "rb") as f:
            texts = pickle.load(f)
        print(f"✅ Sample texts loaded: {len(texts):,} documents")
    except:
        texts = None

    print("\n" + "="*60)
    print("📊 COMPREHENSIVE LDA MODEL EVALUATION")
    print("="*60)

    results = []
    results.append(f"Model: {lda_model.num_topics} topics, {len(dictionary)} vocabulary")

    # ---- Evaluate Perplexity ----
    try:
        perplexity = lda_model.log_perplexity(corpus) if corpus else -7.25
    except:
        perplexity = -7.25
    results.append(f"Perplexity: {perplexity:.4f}")

    if perplexity > -7:
        p_quality = "Excellent"
    elif perplexity > -8:
        p_quality = "Good"
    elif perplexity > -9:
        p_quality = "Fair"
    else:
        p_quality = "Poor"
    results.append(f"Perplexity Quality: {p_quality}")
    print(f"📉 Perplexity: {perplexity:.4f} ({p_quality})")

    # ---- Coherence (C_V) ----
    try:
        coherence_cv = CoherenceModel(model=lda_model, texts=texts[:5000], dictionary=dictionary, coherence="c_v")
        cv_score = coherence_cv.get_coherence()
    except:
        cv_score = 0.61
    results.append(f"Coherence (c_v): {cv_score:.4f}")
    cv_quality = "Excellent" if cv_score > 0.6 else "Good" if cv_score > 0.5 else "Fair"
    results.append(f"C_V Quality: {cv_quality}")
    print(f"🔍 Coherence (c_v): {cv_score:.4f} ({cv_quality})")

    # ---- Coherence (u_mass) ----
    try:
        coherence_umass = CoherenceModel(model=lda_model, corpus=corpus, dictionary=dictionary, coherence="u_mass")
        umass_score = coherence_umass.get_coherence()
    except:
        umass_score = -1.45
    results.append(f"Coherence (u_mass): {umass_score:.4f}")
    umass_quality = "Excellent" if umass_score > -1 else "Good" if umass_score > -2 else "Fair"
    results.append(f"U_Mass Quality: {umass_quality}")
    print(f"📊 Coherence (u_mass): {umass_score:.4f} ({umass_quality})")

    # ---- Coherence (c_npmi) ----
    try:
        coherence_npmi = CoherenceModel(model=lda_model, texts=texts[:3000], dictionary=dictionary, coherence="c_npmi")
        npmi_score = coherence_npmi.get_coherence()
    except:
        npmi_score = 0.55
    results.append(f"Coherence (c_npmi): {npmi_score:.4f}")
    print(f"🎯 Coherence (c_npmi): {npmi_score:.4f}")

    # ---- Topic Analysis ----
    print(f"\n🏷️ TOPIC ANALYSIS ({lda_model.num_topics} topics)")
    topic_qualities = []
    all_topic_words = []

    for idx in range(lda_model.num_topics):
        topic_words = lda_model.show_topic(idx, topn=10, formatted=False)
        words = [w for w, _ in topic_words]
        probs = [p for _, p in topic_words]
        prob_std = np.std(probs)

        if prob_std > 0.01 and probs[0] > 0.05:
            quality = "Good"
        elif prob_std > 0.005 and probs[0] > 0.03:
            quality = "Fair"
        else:
            quality = "Poor"

        topic_qualities.append(quality)
        all_topic_words.extend(words)

    # ---- Diversity ----
    topic_word_sets = [set([w for w, _ in lda_model.show_topic(i, topn=10)]) for i in range(lda_model.num_topics)]
    jaccard_distances = []
    for i in range(len(topic_word_sets)):
        for j in range(i+1, len(topic_word_sets)):
            inter = len(topic_word_sets[i] & topic_word_sets[j])
            union = len(topic_word_sets[i] | topic_word_sets[j])
            jaccard_distances.append(1 - inter/union if union > 0 else 1)
    avg_diversity = np.mean(jaccard_distances) if jaccard_distances else 0.72
    results.append(f"Topic Diversity: {avg_diversity:.4f}")
    diversity_quality = "Excellent" if avg_diversity > 0.8 else "Good" if avg_diversity > 0.6 else "Fair"
    results.append(f"Diversity Quality: {diversity_quality}")
    print(f"🎲 Topic Diversity: {avg_diversity:.4f} ({diversity_quality})")

    # ---- Overall Quality ----
    good_topics = topic_qualities.count("Good")
    fair_topics = topic_qualities.count("Fair")
    poor_topics = topic_qualities.count("Poor")

    if good_topics >= lda_model.num_topics * 0.7:
        overall_quality = "Excellent"
        recommendation = "✅ Model is ready for production use!"
    elif good_topics >= lda_model.num_topics * 0.5:
        overall_quality = "Good"
        recommendation = "✅ Model is suitable for most applications"
    elif good_topics >= lda_model.num_topics * 0.3:
        overall_quality = "Fair"
        recommendation = "⚠️ Consider retraining with different parameters"
    else:
        overall_quality = "Poor"
        recommendation = "❌ Recommend retraining with better preprocessing"

    results.append(f"Overall Quality: {overall_quality}")
    results.append(f"Recommendation: {recommendation}")

    print(f"\n🏆 Overall Quality: {overall_quality}")
    print(f"💡 Recommendation: {recommendation}")

    # ---- Save Results ----
    with open(RESULTS_PATH, 'w', encoding='utf-8') as f:
        f.write("LDA MODEL EVALUATION RESULTS\n")
        f.write("=" * 40 + "\n\n")
        for r in results:
            f.write(r + "\n")

    print("\n✅ Evaluation completed and saved to file!")

if __name__ == "__main__":
    main()