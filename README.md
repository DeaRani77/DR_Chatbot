# 💬 DR_Chatbot: OCR-Enhanced Document Chatbot

DR\_Chatbot is an **interactive, local-first chatbot application** built with **Streamlit** that utilizes the **Phi-3:mini Large Language Model (LLM)** through **Ollama**. This application is designed to be **context-aware**, allowing users to upload documents (text and PDF, including scanned files) and generate responses based on the extracted content. The system is capable of extracting content using both native text parsing and **PaddleOCR** for handling scanned PDF documents.

---

## ✨ Features

* **Interactive Streamlit UI:** A user-friendly, **real-time chat interface** developed using Streamlit.
* **Local LLM Integration:** Connects an **Ollama model (Phi-3:mini)** to the Streamlit frontend for **private and fast inference**.
* **Document Processing (RAG):** Dynamically integrates extracted file content into the conversation to generate accurate, **context-aware responses** (Retrieval-Augmented Generation).
* **Intelligent Text Extraction:** Uses **PyPDF2** to extract text from digitally generated PDFs.
* **Advanced OCR Capability:** Employs **PaddleOCR** and **pdf2image** to perform **Optical Character Recognition** on scanned PDF files.
* **Session Management:** Uses Streamlit's `st.session_state` to **preserve chat history** dynamically.
* **Multi-Format Support:** Accepts both plain **Text files** and **PDF documents**.

---

## 🛠️ System Architecture Overview

The system combines a **Streamlit frontend** with a **Python backend** to manage the flow of data.

### Workflow


1.  **User Input** → **Streamlit UI**
2.  **File (optional)** → **PDF/Text**
3.  **PyPDF2** attempts to extract text.
4.  **(If extraction fails or document is scanned)** → **OCR (PaddleOCR/pdf2image)** processes the document.
5.  **Final extracted content** is appended to the prompt.
6.  **Ollama (Phi-3:mini)** generates the context-based response.
7.  **Streamlit** displays the output to the user.

### Technologies Used

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend/App Framework** | **Streamlit** | UI, user interaction, and session management (`st.session_state`). |
| **LLM Engine** | **Ollama** | Backend communication and running the local LLM. |
| **AI Model** | **Phi-3:mini** | Core model for context-based response generation. |
| **PDF Text Extraction** | **PyPDF2** | Extracts text from digitally generated PDFs. |
| **OCR** | **PaddleOCR / pdf2image** | Converts PDF pages to images for OCR on scanned documents. |

---

## ⚙️ Installation and Setup

### 1. Prerequisites

Ensure the following are installed on your system:

* **Python 3.8+**
* **Ollama:** Download and install Ollama from the [official website](https://ollama.com/).
* **Poppler:** Required by `pdf2image` for converting PDF pages to images. Install via your system's package manager (e.g., `sudo apt install poppler-utils` on Debian/Ubuntu, or using Homebrew on macOS).

### 2. Clone the Repository

Clone the project to your local machine and navigate into the directory:

```bash
git clone [https://github.com/DeaRani77/DR_Chatbot.git](https://github.com/DeaRani77/DR_Chatbot.git)
cd DR_Chatbot
