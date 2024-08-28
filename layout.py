import os
import json
import openai
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

# Carga las variables de entorno desde '.env'.
load_dotenv('.env')

# Obtiene las variables de entorno necesarias.
openAIEndpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openAIApiKey = os.getenv("AZURE_OPENAI_API_KEY")
documentIntelligenceEndpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
documentIntelligenceApiKey = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

# Crea los clientes para los servicios de Azure.
document_intelligence_client = DocumentIntelligenceClient(endpoint=documentIntelligenceEndpoint, credential=AzureKeyCredential(documentIntelligenceApiKey))

# Configura el cliente de OpenAI.
openai.api_key = openAIApiKey

pdfName = "docs/fact_2_pag.pdf"

# Lee el contenido del archivo PDF y lo convierte a base64.
with open(pdfName, "rb") as pdf_file:
    pdf_bytes = pdf_file.read()

# Crea el contenido para el análisis.
analyze_document_content = {
    "base64_source": pdf_bytes
}

try:
    # Inicia la operación de análisis de documentos y espera a que se complete.
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        AnalyzeDocumentRequest(bytes_source=pdf_bytes),
        output_content_format=ContentFormat.MARKDOWN,
    )
    result = poller.result()

    # Extrae el contenido en formato Markdown del resultado.
    markdown = result.content
    
    with open('output.txt', 'w') as file:
    # Escribe el contenido de la variable 'markdown' en el archivo
        file.write(markdown)

except HttpResponseError as e:
    print(e)

# # Define la estructura JSON como un diccionario de Python.
# json_structure = {
#     "company_name": "",
#     "invoice_date": "",
#     "products": [
#         {
#             "id": "",
#             "unit_price": "",
#             "quantity": "",
#             "total": ""
#         }
#     ],
#     "total_amount": "",
#     "signatures": [
#         {
#             "type": "",
#             "has_signature": "",
#             "signed_on": ""
#         }
#     ]
# }

# # Configura las opciones para la solicitud de completaciones de chat.
# chat_options = {
#     "model": "GPT_MA_MODEL",
#     "max_tokens": 4096,
#     "temperature": 0.1,
#     "top_p": 0.1,
#     "messages": [
#         {"role": "system", "content": "You are an AI assistant that extracts data from documents and returns them as structured JSON objects. Do not return as a code block."},
#         {"role": "user", "content": f"Extract the data from this invoice. If a value is not present, provide null. Use the following structure: {json.dumps(json_structure)}"},
#         {"role": "user", "content": markdown}
#     ]
# }

# # Realiza la solicitud de completaciones de chat y espera la respuesta.
# response = openai.ChatCompletion.create(**chat_options)

# # Imprime las respuestas recibidas.
# for message in response['messages']:
#     if message['role'] == 'assistant':
#         print(message['content'])
