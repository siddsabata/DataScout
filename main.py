from langchain_community.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities.apify import ApifyWrapper
from langchain_openai import OpenAIEmbeddings
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
#APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')

if __name__ == "__main__":
    apify = ApifyWrapper()
    loader = apify.call_actor(
        actor_id="jirimoravcik/pdf-text-extractor",
        run_input={"urls": ["https://arxiv.org/pdf/2307.12856.pdf"],"chunk_size": 1000},
        dataset_mapping_function=lambda item: Document(
            page_content = item["text"], metadata={"source": item["url"]}
        ),
    )

    # Create a vector index and store all the text from the PDF
    index = VectorstoreIndexCreator().from_loaders([loader])

    #Ask questions about the pdf
    query = "What is the WebAgent"
    result = index.query_with_sources(query)
    print(result["answer"])



