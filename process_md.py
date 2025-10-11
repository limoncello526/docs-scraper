from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter
import glob
import os

def load_and_split_markdown_files():
    md_folder = os.path.join(os.path.dirname(__file__), "markdown_files")
    md_files = glob.glob(os.path.join(md_folder, "*.md"))

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "Header 1"), ("##", "Header 2")]
    )

    for md_file in md_files:
        print(f"Processing: {md_file}")
        loader = UnstructuredMarkdownLoader(md_file)
        docs = loader.load()
        assert len(docs) == 1
        assert isinstance(docs[0], Document)
        chunks = header_splitter.split_text(docs[0].page_content)
        print(chunks)

if __name__ == '__main__':
    load_and_split_markdown_files()