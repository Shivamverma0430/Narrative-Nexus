# 🤖 Narrative Nexus - AI-Powered Text Analysis & Topic Intelligence Platform

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Gensim](https://img.shields.io/badge/Gensim-LDA-green?style=for-the-badge)](https://radimrehurek.com/gensim/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)

**Narrative Nexus** is an advanced, end-to-end NLP and Topic Intelligence platform. It combines Latent Dirichlet Allocation (LDA) topic modeling, VADER sentiment analysis, rule-based & statistical domain classification, extractive summarization, and multi-format document parsing inside a futuristic, high-performance web dashboard built with Streamlit.

---

## 🌟 Key Features

### 📁 Multi-Format Document Ingestion
- Upload and process **PDF**, **DOCX**, **PPTX**, and **TXT** files, or enter text manually.
- Automatic text extraction and chunk-based document streaming.

### 🧠 Smart Auto-Select Topic Analysis
- **Dynamic Routing**: Evaluates vocabulary overlap between user input and the pre-trained LDA dictionary.
- **LDA Topic Modeling**: Extracts latent topics and probability distributions when vocabulary overlap threshold is satisfied.
- **Fallback Keyword Domain Detection**: Smoothly transitions to rule-based TF-IDF/Noun term analysis if input text deviates from the training domain.

### 🌍 Domain Detection & Radar Analytics
- Categorizes text into major domains (*News & Current Affairs*, *Product Reviews*, *Entertainment & Media*, *Technology & Science*, *Business & Finance*, *Health & Medical*, *Sports*, *Education & Academic*, *Travel*, *Lifestyle*).
- Interactive **Domain Radar Charts** and **Probability Distribution Graphs** powered by Plotly.

### 💭 Sentiment Analysis & Gauge Meter
- Dual-layer VADER Sentiment Intensity Analyzer.
- Visual **Sentiment Gauge Chart** (Negative, Neutral, Positive) with compound confidence metrics.
- Detailed breakdown of sentiment components.

### 📝 Smart Summarization & Title Generation
- Extractive sentence summarization tailored to text length.
- Automatic document title synthesis based on top key noun frequencies.

### 📊 Text Characteristics & Readability Metrics
- Statistics on Word Count, Sentence Count, Vocabulary Richness (Lexical Diversity), and Content Density.

### 📄 Executive PDF Report Export
- Generate and download a sleek **PDF Report** summarizing the analysis, domain findings, summary, and optimization recommendations using ReportLab.

---

## 📊 Dataset & Download

The project relies on a consolidated text dataset for training the LDA model (`data/combined_data.csv`). 

- **Dataset File**: `combined_data.csv`
- **Location in Repository**: Place inside the `data/` folder (`data/combined_data.csv`).
- **Download Link**: 📥 [Google Drive Dataset Download](https://drive.google.com/file/d/1qYahG9-o9Op9i7g7kNSsaLrEqtjdw6N1/view?usp=drivesdk)

---

## 📁 Repository Structure

```
├── app.py                  # Main Streamlit Web Application & UI Dashboard
├── mmm.py                  # Streamlit Application variant / Core Engine Backup
├── train.py                # Pipeline script to preprocess data and train LDA model
├── evaluate.py             # Model evaluation suite (Perplexity, Coherence, Diversity)
├── requirements.txt        # Project dependencies
├── preprocessing.ipynb     # Jupyter Notebook for experimental data preprocessing
├── data/
│   └── combined_data.csv   # Training dataset (Download from link above)
├── models/
│   ├── dictionary.dict     # Gensim dictionary mapping
│   ├── corpus.mm           # Serialized Matrix Market corpus
│   ├── lda.model           # Trained Gensim LdaMulticore model
│   ├── texts.pkl           # Preprocessed sample texts for coherence evaluation
│   └── evaluation_results.txt # Exported evaluation metrics
└── test/
    └── test.txt            # Sample test text file
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.9+** installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/Shivamverma0430/Narrative-Nexus.git
cd Narrative-Nexus
```

### 3. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Download Required NLTK Data
Run the following python snippet to download required NLTK corpora:
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
```

---

## 🚀 Running the Web Application

Launch the Streamlit dashboard by running:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` to access the application.

---

## 🚀 Model Training & Evaluation

### Train a New LDA Topic Model
If you download or update `data/combined_data.csv`, you can retrain the LDA model:
```bash
python train.py
```
This will preprocess data in chunks, save `models/dictionary.dict`, `models/corpus.mm`, train an `LdaMulticore` model (`models/lda.model`), and compute initial $C_v$ coherence.

### Evaluate Model Performance
To compute comprehensive evaluation metrics ($C_v$, $U_{mass}$, $C_{npmi}$, Log-Perplexity, Topic Diversity, Topic Quality):
```bash
python evaluate.py
```
The results will be printed to stdout and saved to `models/evaluation_results.txt`.

---

## 🎨 User Interface & Aesthetics

- **Cyberpunk Dark Theme**: Custom CSS featuring gradients (`#0f0f23`, `#1a1a2e`, `#16213e`), glassmorphism cards, and glowing borders.
- **Particle Background**: Dynamic CSS floating particles effect.
- **Interactive Visualizations**: High-contrast Plotly bar, gauge, and radar charts.

---

## 📜 License
This project is open-source under the MIT License.
