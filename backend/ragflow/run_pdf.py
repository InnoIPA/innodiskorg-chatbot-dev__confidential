# Added by Judy >>>>>>>>>>>>>>>>>>>>

import logging
import os
import re
from io import BytesIO
from pathlib import Path
from timeit import default_timer as timer
from typing import Any

from PIL.Image import Image
from ragflow.deepdoc.parser import PdfParser
from ragflow.rag.nlp import naive_merge, rag_tokenizer, tokenize_chunks, tokenize_table

from .constants import IMAGE_DIR

# RAGFlow logger
ragflow_logger = logging.getLogger("ragflow")


def print_message(title: str, msg: tuple | list) -> None:
    if type(msg) in [tuple, list]:
        print(f"\n\n\n============================================\n{title} [{len(msg)}] =")
        for idx, m in enumerate(msg):
            print(f"{idx + 1}) {m}\n")


class Pdf(PdfParser):
    def __init__(self):
        super().__init__()

    def __call__(
        self,
        filename,
        binary=None,
        from_page=0,
        to_page=100000,
        zoomin=3,
        callback=None,
        separate_tables_figures=False,
    ):
        # OCR
        start = timer()
        first_start = start
        ragflow_logger.info("OCR started")
        self.__images__(
            filename if not binary else binary,
            zoomin,
            from_page,
            to_page,
            callback,
        )
        ragflow_logger.info("OCR finished ({:.2f}s)".format(timer() - start))
        ragflow_logger.info("OCR({}~{}): {:.2f}s".format(from_page, to_page, timer() - start))

        # Layout recognition
        start = timer()
        self._layouts_rec(zoomin)
        ragflow_logger.info("Layout analysis ({:.2f}s)".format(timer() - start))

        # Table analysis
        start = timer()
        self._table_transformer_job(zoomin)
        ragflow_logger.info("Table analysis ({:.2f}s)".format(timer() - start))

        # Text merge
        start = timer()
        self._text_merge()
        ragflow_logger.info("Text merged ({:.2f}s)".format(timer() - start))

        # Concatenate downward
        if separate_tables_figures:
            tbls, figures = self._extract_table_figure(True, zoomin, True, True, True)
            self._concat_downward()
            ragflow_logger.info("layouts cost: {}s".format(timer() - first_start))
            return [(b["text"], self._line_tag(b, zoomin)) for b in self.boxes], tbls, figures
        else:
            tbls = self._extract_table_figure(True, zoomin, True, True)
            self._naive_vertical_merge()
            self._concat_downward()
            # self._filter_forpages()
            ragflow_logger.info("layouts cost: {}s".format(timer() - first_start))
            return [(b["text"], self._line_tag(b, zoomin)) for b in self.boxes], tbls


class KnowledgeHandler:
    """
    Data preprocessing for RAG, including `parse` and `chunk` operations.

    Currently, support file types as below:
        * PDF
    """

    @classmethod
    def parse_pdf(
        cls,
        file_path: str | Path,
        from_page: int = 0,
        to_page: int = 100000,
        callback: Any = None,
    ) -> dict[str, list | tuple | Pdf]:
        """
        Parse the PDF file.

        Args:
            file_path (str, Path): The PDF file path.
            from_page (int): The start page number. Default is `0`.
            to_page (int): The end page number. Default is `100000`.
            callback (Any): The callback function. Default is `None`.

        Returns:
            parsed_result (dict[str, list | tuple | Pdf]): The parsed result as below.
                - ["contents"]["sections"]: Parsed texts.
                - ["contents"]["tables"]: Parsed tables and figures.
                - ["parser"]: The PDF parser. You can get it for subsequent processing if needed.
        """

        pdf_parser = Pdf()
        sections, tables = pdf_parser(
            str(file_path),
            from_page=from_page,
            to_page=to_page,
            callback=callback,
        )

        # print_message("sections", sections)
        # print_message("tables", tables)

        return {
            "contents": {
                "sections": sections,
                "tables": tables,
            },
            "parser": pdf_parser,
        }

    @classmethod
    def prcoess_pdf(
        cls,
        file_path: str | Path,
        from_page: int = 0,
        to_page: int = 100000,
        callback: Any = None,
        chunk_token_num: int = 128,
        delimiter: str = "\n。；！？",
    ) -> list:
        """
        Parse and chunk the PDF file.

        Args:
            file_path (str, Path): The PDF file path.
            from_page (int): The start page number. Default is `0`.
            to_page (int): The end page number. Default is `100000`.
            callback (Any): The callback function. Default is `None`.
            chunk_token_num (int): The token number of a chunk. Default is `128`.
            delimiter (str): The accepted delimiter for chunk. Default is `\\n。；！？`.

        Returns:
            processed_result (list): The PDF chunks.
        """

        # Parse
        parsed_result = cls.parse_pdf(
            file_path,
            from_page=from_page,
            to_page=to_page,
            callback=callback,
        )
        sections = list(parsed_result["contents"]["sections"])
        tables = tuple(parsed_result["contents"]["tables"])
        parser: Pdf = parsed_result["parser"]

        # print_message("sections", sections)
        # print_message("tables", tables)

        # Chunk (for `tables`)
        lang = "Chinese" if "zh_CN" in os.getenv("LANG", "") else "English"
        is_english = lang.lower() == "english"  # is_english(cks)
        doc = {
            "docnm_kwd": str(file_path),
            "title_tks": rag_tokenizer.tokenize(re.sub(r"\.[a-zA-Z]+$", "", str(file_path))),
        }
        doc["title_sm_tks"] = rag_tokenizer.fine_grained_tokenize(doc["title_tks"])
        chunked_tables = tokenize_table(tables, doc, is_english)

        # print_message("chunked_tables", chunked_tables)

        # Chunk (for `sections`)
        st = timer()
        chunks = naive_merge(sections, chunk_token_num, delimiter)  # Merge sections previously
        chunked_sections = tokenize_chunks(chunks, doc, is_english, parser)
        ragflow_logger.info("naive_merge({}): {}".format(file_path, timer() - st))

        # print_message("chunked_sections", chunked_sections)

        # Integrate all chunks
        integrated_chunks = chunked_tables
        integrated_chunks.extend(chunked_sections)

        # Save each chunk image
        for idx, chunk in enumerate(integrated_chunks):
            chunk = dict(chunk)
            img: Image = chunk.get("image")

            # Convert to RGB JPEG in memory
            with BytesIO() as output_buffer:
                if isinstance(img, bytes):
                    output_buffer.write(img)
                    output_buffer.seek(0)
                else:
                    # Convert palette/RGBA images to RGB
                    if img.mode in ("P", "RGBA"):
                        img = img.convert("RGB")
                    try:
                        img.save(output_buffer, format='JPEG')
                    except OSError as e:
                        ragflow_logger.warning(f"Saving image of chunk got exception, ignore: {str(e)}")
                img_data = output_buffer.getvalue()

            # Determine local image file path and ensure directory exists
            img_dir = Path(
                IMAGE_DIR,
                Path(file_path).stem.split("_")[0],  # Format of `file_path`: {file_id}_{file_name}
            )
            img_path = img_dir / f"{idx + 1}.jpg"
            if not img_dir.is_dir():
                img_dir.mkdir(parents=True)

            # Write image bytes to disk
            try:
                with open(img_path, 'wb') as f:
                    f.write(img_data)
            except Exception as e:
                ragflow_logger.error(f"Writing image to {img_path} failed: {str(e)}")

            # Close PIL image if necessary
            if not isinstance(img, bytes):
                try:
                    img.close()
                except Exception:
                    pass

            # Remove `image` key and add `image_path` key
            chunk.pop("image", None)
            chunk["image_path"] = str(img_path)
            integrated_chunks[idx] = chunk

        return integrated_chunks


if __name__ == "__main__":
    args = {
        "file_path": "./EGPL_21S3.pdf",
        "from_page": 0,
        "to_page": 1,
        "callback": None,
        # "chunk_token_num": 512,
        # "delimiter": "\n!?。；！？",
    }

    chunks = KnowledgeHandler.prcoess_pdf(**args)
    print_message("parse and chunk", chunks)

# <<<<<<<<<<<<<<<<<<<< Added by Judy
