# 💬 DR_Chatbot: Document-Aware Interactive Chatbot

**DR_Chatbot** is an interactive, local-first chatbot application built with **Streamlit** that utilizes the **Phi3:mini** Large Language Model (LLM) through **Ollama**. This application is designed to be context-aware, allowing users to upload documents (text and PDF, including scanned files) and generate responses based on the extracted content.

---

## ✨ Features

* **Interactive UI:** A user-friendly, real-time chat interface developed using **Streamlit**.
* **Local LLM Integration:** Powered by **Ollama**, ensuring privacy and quick inference with the lightweight **Phi3:mini** model.
* **Document Processing (RAG):** Ability to process and chat with uploaded documents to provide context-aware answers. 

[Image of Retrieval Augmented Generation RAG workflow]

* **OCR Capability:** Handles **scanned PDF files** by using Optical Character Recognition (OCR) to extract text before processing.
* **Multi-Format Support:** Accepts both plain **Text files** and **PDF documents**.

---

## 🛠️ Technologies Used

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | **Python** | Primary development language. |
| **Frontend** | **Streamlit** | Creating the interactive web application interface. |
| **LLM Engine** | **Ollama** | Running and managing the local LLM. |
| **Large Language Model** | **Phi3:mini** | The core model for generating responses. |
| **Document Handling** | **PyPDF2** | Fast extraction of native, embedded text from PDFs. |
| **OCR** | **PaddleOCR / pdf2image** | Robust fallback for text extraction from scanned or image-based PDFs. |

---

## ⚙️ Installation

Follow these steps to set up and run the DR_Chatbot locally.

### 1. Prerequisites

Before starting, ensure you have the following installed on your system:

* **Python 3.8+**
* **Ollama:** Download and install Ollama from the [official website](https://ollama.com).
* **Poppler (Crucial for PDF OCR):** The `pdf2image` library requires the Poppler utility to convert PDF pages to images.
    * **Linux/macOS:** Install via package manager (e.g., `sudo apt-get install poppler-utils` or `brew install poppler`).

### 2. Clone the Repository

Clone the project to your local machine:

```bash
git clone [https://github.com/DeaRani77/DR_Chatbot.git](https://github.com/DeaRani77/DR_Chatbot.git)
cd DR_Chatbot
