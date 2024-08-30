import os
from PyPDF2 import PdfReader, PdfWriter
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat

def process_pdf_compuesto_pages(pdf_path, document_intelligence_client):
    name = os.path.basename(pdf_path).split('.')[0]
    output_dir = f"txt_comp/{name}"  # Directorio de salida para los archivos .txt
    os.makedirs(output_dir, exist_ok=True)  # Crea el directorio si no existe

    # Abre el archivo PDF con PyPDF2
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_path)

        # Procesa cada página del PDF
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            writer = PdfWriter()
            writer.add_page(page)

            # Crea un archivo temporal para la página actual
            temp_pdf_path = f"temp_page_{page_number + 1}.pdf"
            with open(temp_pdf_path, "wb") as page_file:
                writer.write(page_file)

            # Lee el contenido del archivo temporal y lo convierte a base64
            with open(temp_pdf_path, "rb") as page_file:
                page_bytes = page_file.read()

            txt_name = f"{output_dir}/pag_{page_number + 1}.txt"  # Nombre del archivo txt para la página actual

            # Inicia la operación de análisis de documentos y espera a que se complete.
            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-layout",
                AnalyzeDocumentRequest(bytes_source=page_bytes),
                output_content_format=ContentFormat.MARKDOWN,
            )
            result = poller.result()

            # Extrae el contenido en formato Markdown del resultado.
            markdown = result.content

            with open(txt_name, 'w') as file:
                # Escribe el contenido de la variable 'markdown' en el archivo
                file.write(markdown)

            # Elimina el archivo temporal
            os.remove(temp_pdf_path)
            
def process_pdf_simple_pages(pdf_path, document_intelligence_client):
    name = os.path.basename(pdf_path).split('.')[0]
    output_dir = "txt_simp"  # Directorio de salida para los archivos .txt
    os.makedirs(output_dir, exist_ok=True)  # Crea el directorio si no existe
    txt_name = f"{output_dir}/{name}.txt"

    # Abre el archivo PDF con PyPDF2
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        
        poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        AnalyzeDocumentRequest(bytes_source=pdf_bytes),
        output_content_format=ContentFormat.MARKDOWN,
        )
        
        result = poller.result()
    
        # Extrae el contenido en formato Markdown del resultado.
        markdown = result.content

        with open(txt_name, 'w') as file:
            # Escribe el contenido de la variable 'markdown' en el archivo
            file.write(markdown)