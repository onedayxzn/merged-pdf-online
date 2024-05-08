import streamlit as st
import PyPDF2
import os
import tempfile


def merge_pdfs(paths):
    merger = PyPDF2.PdfMerger()
    for path in paths:
        merger.append(path)
    return merger

def save_merged_pdf(merged_pdf, output_path):
    with open(output_path, 'wb') as output_file:
        merged_pdf.write(output_file)

def delete_files_in_folder(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Iterate over each file and delete it
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path,)
            print(f"Deleted: {file_path}")


def main():
    st.title("PDF Merger")

    if st.button("Reset"):
        delete_files_in_folder('temp')
        st.success("Reset successful!")
        # restart the app
        st.experimental_rerun()
        

    st.write("Select PDF files to merge:")
    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")

    if uploaded_files:
        st.write("Files uploaded successfully!")
        
        # Create a list to store uploaded file paths and their corresponding file names
        file_info = []

        temp_files = 'temp'
        os.makedirs(temp_files, exist_ok=True)

        # Display uploaded files along with a number input for users to set the order
        for i, uploaded_file in enumerate(uploaded_files):
            with open(os.path.join(temp_files, uploaded_file.name), 'wb') as temp_file:
                temp_file.write(uploaded_file.getbuffer())
            file_info.append((os.path.join(temp_files, uploaded_file.name), uploaded_file.name))

            st.write(f"File {i+1}: {uploaded_file.name}")

        st.write("Set the order of files by entering the numbers in the desired sequence separated by commas (e.g., '3,1,2')")
        order_input = st.text_input("Order of files:")

        if st.button("Merge PDFs"):
            if order_input:
                order = [int(x.strip()) - 1 for x in order_input.split(",")]  # Convert input to a list of integers
                ordered_paths = [file_info[i][0] for i in order]  # Get paths based on the input order
                ordered_names = [file_info[i][1] for i in order]  # Get names based on the input order

                merged_pdf = merge_pdfs(ordered_paths)
            
                st.spinner("Merging PDF files...")
                with tempfile.TemporaryDirectory() as temp_dir:
                    output_path = os.path.join(temp_dir, "merged_pdf.pdf")
                    save_merged_pdf(merged_pdf, output_path)
                    st.success("PDF files merged successfully!")
                    with open(output_path, 'rb') as output_file:
                        st.download_button("Download", output_file, file_name="merged_pdf.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
