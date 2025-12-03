import streamlit as st
import ollama
from PyPDF2 import PdfReader
from paddleocr import PaddleOCR
from pdf2image import convert_from_bytes
import numpy as np
import io

@st.cache_resource
def init_paddle_ocr():
    """Initialize PaddleOCR, ensuring it only runs once and handles potential errors."""
    try:
    
        ocr = PaddleOCR(use_angle_cls=True, lang='en') 
        st.success("🤖 PaddleOCR initialized successfully.")
        return ocr
    except Exception as e:
        
        st.error(f"Error initializing PaddleOCR. Ensure Poppler is installed for pdf2image on Windows/Linux. Error: {e}")
        return None

ocr = init_paddle_ocr()


st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")
st.title("💬 Chatbot with File Upload & Chat History")
st.caption("Now with **PaddleOCR** support for scanned PDFs!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! I'm your assistant. How can I help you today? Try uploading a text or PDF file!"}
    ]

if "file_content" not in st.session_state:
    st.session_state["file_content"] = ""

def process_pdf_for_ocr(uploaded_file, ocr_engine):
    """
    Attempts text extraction using PyPDF2, falls back to PaddleOCR if needed.
    """
    st.info("Starting PDF extraction...")
    
    try:
 
        uploaded_file.seek(0)
        pdf_reader = PdfReader(uploaded_file)

        pypdf_content = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        
        if len(pypdf_content) > 50:
            st.success("✅ Extracted text using **PyPDF2** (Native text found).")
            return pypdf_content

    except Exception as e:
    
        st.warning(f"PyPDF2 failed or extracted minimal content. Falling back to OCR. Error: {e}")
        

    if ocr_engine is None:
        return ""
        
    st.warning("🚨 Falling back to **PaddleOCR** (OCR) for image-based PDF.")
    
    try:
       
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        
     
        images = convert_from_bytes(pdf_bytes)
        
        file_content = []
        progress_bar = st.progress(0, text="Performing OCR...")
        
        for i, image in enumerate(images):
    
            img_np = np.array(image.convert('RGB')) 
            
            result = ocr_engine.ocr(img_np, cls=True)
           
            page_text = ""
            if result and result[0]:
                for line in result[0]:
                   
                    text = line[1][0]
                    page_text += text + " "
            
            file_content.append(f"\n--- PAGE {i+1} ---\n" + page_text)
            progress_bar.progress((i + 1) / len(images), text=f"Performing OCR on page {i + 1} of {len(images)}...")

        progress_bar.empty()
        st.success("✅ OCR completed successfully!")
        return "\n".join(file_content)

    except Exception as e:
        st.error(f"An error occurred during OCR processing: {e}")
        return ""

with st.sidebar:
    st.header("⚙️ Options")

   
    uploaded_file = st.file_uploader("📁 Upload a file", type=["txt", "pdf"])
    
  
    file_status = st.empty()

    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            file_content = uploaded_file.read().decode("utf-8")
        
        elif uploaded_file.type == "application/pdf":
        
            file_content = process_pdf_for_ocr(uploaded_file, ocr)
        
        else:
            file_content = ""
            
        st.session_state["file_content"] = file_content
        
 
        if st.session_state["file_content"]:
            file_status.success(f"✅ Content extracted successfully! ({len(st.session_state['file_content'])} characters)")
        else:
            file_status.error("❌ File uploaded, but no content could be extracted.")
            
    else:
        st.session_state["file_content"] = ""
        file_status.info("Please upload a file to start.")


    
    with st.expander("📝 View Extracted File Content"):
        if st.session_state["file_content"]:
            st.code(st.session_state["file_content"][:500] + "...", language="text")
        else:
            st.write("No file content loaded.")

    with st.expander("🕓 View Chat History"):
        for msg in st.session_state["messages"]:
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            st.write(f"{role_icon} **{msg['role'].capitalize()}:** {msg['content']}")

    st.markdown("---")
    col1, col2 = st.columns(2)
    
    
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Chat cleared. How can I assist you now?"}
            ]
            st.rerun()

    with col2:
        if st.button("🆕 New Chat"):
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Hi! I'm your assistant. Let's start a new chat!"}
            ]
            st.session_state["file_content"] = ""
            st.rerun()

for msg in st.session_state["messages"]:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

def generate_response():
    
    context_prompt = ""
    if st.session_state["file_content"]:
        context_prompt = (
            f"The user has uploaded a file. "
            f"Here is the relevant content you can refer to:\n\n"
            f"{st.session_state['file_content']}\n\n"
        )

   
    system_message = {
        "role": "system",
        "content": (
            "You are a helpful AI assistant. Respond clearly and concisely "
            "based on the user's input and context provided."
        )
    }

    messages = [system_message]
  
    messages += st.session_state["messages"]
 
    if context_prompt:
        messages += [{"role": "system", "content": context_prompt}]
        
    try:
        response = ollama.chat(
            model="phi3:mini",
            stream=True,
            messages=messages,
        )

     
        for partial_resp in response:
            token = partial_resp["message"]["content"]
            st.session_state["full_message"] += token
            yield token
            
    except Exception as e:
        st.error(f"An error occurred while communicating with Ollama. Is the 'phi3:mini' model running? Error: {e}")
        yield "An error occurred while generating the response."

if prompt := st.chat_input("Type your message here..."):
   
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)

  
    st.session_state["full_message"] = ""
    with st.chat_message("assistant", avatar="🤖"):
       
        full_response = st.write_stream(generate_response())

    st.session_state["messages"].append(
        {"role": "assistant", "content": full_response}
    )