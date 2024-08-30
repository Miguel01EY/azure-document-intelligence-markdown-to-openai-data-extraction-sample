import os
import openai
import functions
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
import PyPDF2

# Carga las variables de entorno desde '.env'.
load_dotenv('.env')

# Obtiene las variables de entorno necesarias.
documentIntelligenceEndpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
documentIntelligenceApiKey = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
azureConnectionString = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Crea los clientes para los servicios de Azure.
document_intelligence_client = DocumentIntelligenceClient(endpoint=documentIntelligenceEndpoint, credential=AzureKeyCredential(documentIntelligenceApiKey))

# Descargar un PDF de Blob Storage
tipo_doc = 1 # 1 es compuesto y 2 es simple
pdfName = "docs/fact_2_pag.pdf"    
try:
    if tipo_doc in [1]:
        functions.process_pdf_compuesto_pages(pdfName, document_intelligence_client)
    elif tipo_doc in [2]:
        functions.process_pdf_simple_pages(pdfName, document_intelligence_client)

except HttpResponseError as e:
    print(e)