# AI Heartbeat Disease Predictor

A fully integrated Machine Learning and Artificial Intelligence web application designed to predict the likelihood of heart-related diseases based on patient physiological features. The application also provides an AI-driven chatbot for further assistance and document analysis for automatic extraction of medical data.

## 🚀 Features

- **Heart Disease Prediction**: Uses an optimized Machine Learning model (trained with 13 key physiological features) to predict heart disease risk.
- **Top Diseases Breakdown**: Provides the top 3 most likely medical conditions with percentage probabilities based on user inputs.
- **AI Medical Assistant**: An integrated chatbot powered by the Google Gemini API to answer cardiology questions using a Retrieval-Augmented Generation (RAG) framework.
- **Medical Document Analysis**: Allows users to upload medical documents (PDFs, images) to automatically parse, extract relevant health values, and integrate them into the prediction engine.
- **Dynamic Landscape UI**: A premium, non-centralized web interface design for a better user experience.

---

## 🛠️ Architecture and Tech Stack

We have deliberately structured this application using a specific, highly-optimized tech stack. Here is *what* we used and *why*:

### 1. Frontend: Vanilla HTML, CSS, JavaScript
- **Why?**: We used vanilla web technologies to maintain a completely lightweight, dependency-free interface. By avoiding heavy frontend frameworks (like React or Angular), the tool loads instantly and avoids complex build steps. The landscape-oriented, dynamic UI with glassmorphism and modern colors provides a premium feel without bogging down the browser.

### 2. Backend API: Flask (Python)
- **Why?**: Flask is a lightweight micro-framework for Python. Because our machine learning models and AI scripts inherently run on Python, Flask provides the most seamless, frictionless way to expose these tools via REST APIs (`/predict`, `/chat`, `/upload-document`). It avoids the bloat of larger frameworks like Django while retaining robust routing.

### 3. Machine Learning: Scikit-learn, Pandas, Numpy
- **Why?**: Scikit-Learn is the industry standard for classical ML tasks over tabular data. For analyzing exactly 13 physiological features (e.g., Age, Sex, Resting Blood Pressure, Cholesterol), ensemble or linear models are highly explainable, fast to train, and execute in milliseconds on the backend, making it far superior to heavy deep learning architectures for this specific domain.

### 4. AI Engine: Google Gemini API (`google-generativeai`)
- **Why?**: We specifically migrated from local open-source LLMs (like Ollama) to Google Gemini to offload the massive compute requirements of local LLMs. Gemini provides state-of-the-art reasoning required for complex tasks like formatting the "Top 3 diseases with percentages," acting as a knowledgeable medical assistant, and handling multimodal inputs (PDF/Image document parsing/extraction) without requiring an advanced GPU on the server host.

### 5. Retrieval-Augmented Generation (RAG)
- **Why?**: We implemented a custom RAG Engine (`rag_engine.py`) with a vector store (`vector_store.py`) to inject hard-coded, reviewed medical knowledge into the AI prompts. This critically reduces LLM "hallucinations," grounding the AI's explanations and chatbot responses in factual reality before they ever reach the user.


---

## 🧠 AI & Machine Learning Models

This application leverages a hybrid AI architecture, combining classical machine learning for precision and large language models for reasoning.

### 1. Predictive ML Model: Random Forest Classifier
*   **Library**: `scikit-learn`
*   **Algorithm**: `RandomForestClassifier` (100 estimators)
*   **Task**: Binary heart disease risk classification.
*   **Preprocessing**: `StandardScaler` for normalization.

### 2. Core AI Engine: Google Gemini 2.5 Flash
*   **Library**: `google-genai`
*   **Model**: `gemini-2.5-flash`
*   **Role**: Handles top 3 disease estimations, conversational medical assistance, and multimodal document parsing.

### 3. RAG Engine: TF-IDF & Cosine Similarity
*   **Library**: `scikit-learn`
*   **Role**: High-efficiency retrieval from the localized medical knowledge base to ensure grounded AI responses.

---

## 💻 How to Run the Application Locally

### Prerequisites
- Python 3.8+
- An active `GEMINI_API_KEY` (Add this to a `.env` file in the root directory).

### Installation Steps

1. **Clone the repository and enter the directory**:
   ```bash
   git clone <repository_url>
   cd AI-Heartbeat-Disease-Predictor
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Install the required Python dependencies**:
   Run the following command to install Flask, Scikit-Learn, Generative AI tools, and data processing libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend server**:
   Start the Flask application. It automatically serves the frontend static files.
   ```bash
   python backend/app.py
   ```

5. **Open the App**:
   Navigate your web browser to:
   ```text
   http://127.0.0.1:5000/
   ```

Enjoy your AI-powered Heart Disease Predictor!
