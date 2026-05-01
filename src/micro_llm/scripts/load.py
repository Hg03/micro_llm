from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from micro_llm.scripts.utils import Document
from typing import Iterator, List
from omegaconf import DictConfig
from pathlib import Path


def get_documents(cfg: DictConfig) -> List[Document]:
    docs_path = Path(cfg.paths.docs)
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = cfg.load.do_ocr
    pipeline_options.do_table_structure = cfg.load.do_table_structure
    docs_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    pdf_files = list(docs_path.rglob("*.pdf"))
    results = docs_converter.convert_all(pdf_files)
    return convert_in_markdown(results=results, docs_path=docs_path)


def convert_in_markdown(results: Iterator, docs_path: Path) -> List[Document]:
    documents = []
    for result in results:
        source = str(result.input.file)
        documents.append(
            Document(
                content=result.document,
                doc_id=Path(source).stem,
                source=source,
            )
        )

    print(f"Loaded {len(documents)} documents from {docs_path}")
    return documents
