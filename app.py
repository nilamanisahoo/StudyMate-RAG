
import streamlit as st
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(
    page_title="StudyMate RAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudyMate RAG")
st.write("Upload a PDF and extract its text.")

uploaded_file = st.file_uploader(
    "Choose a study PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    try:
        pdf_bytes = BytesIO(uploaded_file.getvalue())
        reader = PdfReader(pdf_bytes)

        st.success(f"PDF loaded: {uploaded_file.name}")
        st.write(f"**Total pages:** {len(reader.pages)}")

        all_text = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                all_text.append(
                    f"Page {page_number}\n{text}"
                )

        extracted_text = "\n\n".join(all_text)

        if extracted_text.strip():
            st.subheader("Extracted PDF text")
            st.text_area(
                "PDF content",
                value=extracted_text,
                height=350
            )
            st.download_button(
                "Download extracted text",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
        else:
            st.warning(
                "No selectable text was found. "
                "This PDF may contain scanned pages or images."
            )

    except Exception as error:
        st.error(f"Could not process PDF: {error}")
