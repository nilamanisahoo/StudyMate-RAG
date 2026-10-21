
import streamlit as st
from pypdf import PdfReader
from io import BytesIO
from langchain_text_splitters import RecursiveCharacterTextSplitter

st.set_page_config(
    page_title="StudyMate RAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudyMate RAG")
st.write("Upload a PDF, extract text, and split it into chunks.")

uploaded_file = st.file_uploader(
    "Choose a study PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    try:
        reader = PdfReader(BytesIO(uploaded_file.getvalue()))

        st.success(f"PDF loaded: {uploaded_file.name}")
        st.write(f"**Total pages:** {len(reader.pages)}")

        documents = []

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""

            if page_text.strip():
                documents.append({
                    "text": page_text,
                    "page": page_number,
                    "source": uploaded_file.name
                })

        if not documents:
            st.warning("No selectable text found in this PDF.")
            st.stop()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )

        chunks = []

        for document in documents:
            page_chunks = splitter.split_text(document["text"])

            for chunk_number, chunk_text in enumerate(
                page_chunks, start=1
            ):
                chunks.append({
                    "text": chunk_text,
                    "source": document["source"],
                    "page": document["page"],
                    "chunk": chunk_number
                })

        st.subheader("Chunking results")
        st.write(f"**Pages with text:** {len(documents)}")
        st.write(f"**Total chunks:** {len(chunks)}")

        for index, chunk in enumerate(chunks, start=1):
            with st.expander(
                f"Chunk {index} | Page {chunk['page']}"
            ):
                st.write(chunk["text"])
                st.caption(
                    f"Source: {chunk['source']} | "
                    f"Page: {chunk['page']} | "
                    f"Page chunk: {chunk['chunk']}"
                )

        st.download_button(
            "Download chunks as JSON",
            data=__import__("json").dumps(
                chunks, indent=2, ensure_ascii=False
            ),
            file_name="pdf_chunks.json",
            mime="application/json"
        )

    except Exception as error:
        st.error(f"PDF processing failed: {error}")
