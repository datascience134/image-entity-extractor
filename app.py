import io
import pandas as pd
import streamlit as st

from core.file_handler import handle_uploaded_file
from core.llm import client, llm_image
from core.output_processor import process_into_dict_sys_prompt, process_output

st.title('Receipt Entity Extraction Tool')

uploaded_file = st.file_uploader("Upload image/pdf or a ZIP file of images/pdfs", type=["png", "jpg", "jpeg", ".webp", "pdf", "zip"])

if uploaded_file:
    base64_dict = handle_uploaded_file(uploaded_file)

     # Button to trigger inference
    if st.button("Run Inference"):
        with st.spinner("Running inference..."):

            receipt_extraction_prompt = (
                "Extract the total amount paid, shop name, and receipt date from this receipt. "
                "Return as JSON. If missing, use ''. Date should be in DD/MM/YYYY."
            )

            answer_list = []

            for filename, list_of_base64 in base64_dict.items(): 
                for base64_str in list_of_base64:
                    try:
                        answer = llm_image(client, receipt_extraction_prompt, base64_str)
                        json_output = process_output(answer, process_into_dict_sys_prompt)
                        answer_list.append(json_output)
                        st.subheader("Extracted Information")
                        st.code(json_output)
                    except Exception as e:
                        st.error(f"Error during inference: {e}")
            
            df = pd.DataFrame(answer_list)

            # Show DataFrame
            st.subheader("Full Results Table")
            st.dataframe(df, use_container_width=True)

            # Convert DataFrame to CSV and Excel
            csv_data = df.to_csv(index=False)
            
            excel_buffer = io.BytesIO()

            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Extracted Info")
            excel_data = excel_buffer.getvalue()

            # Download buttons
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="extracted_data.csv",
                mime="text/csv"
            )

            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name="extracted_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

