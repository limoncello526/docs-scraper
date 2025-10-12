from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_ollama import OllamaEmbeddings
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
import glob
import os

def load_and_split_markdown_files():
    md_files = glob.glob(os.path.join("markdown_files", "*.md"))

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "Header1"), ("##", "Header2")]
    )

    with weaviate.connect_to_local() as weaviate_client:
        embeddings_model = OllamaEmbeddings(model="mxbai-embed-large")
        for md_file in md_files:
            print(f"Processing: {md_file}")
            docs = UnstructuredMarkdownLoader(md_file).load()
            chunks = header_splitter.split_text(docs[0].page_content)
            WeaviateVectorStore.from_documents(chunks, embeddings_model, client=weaviate_client, index="ccg_docs")

if __name__ == '__main__':
    load_and_split_markdown_files()