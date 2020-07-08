"""Tesseracting images and converting them to pdf."""
from typing import Dict, List

from PIL import Image
import pytesseract
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from pdf_tools.rectangle import Rectangle


class Scanner:
    """Ocr image, create searchable pdf from images."""

    def __init__(self):
        pass

    @classmethod
    def ocr_one_image(cls,
                      im: Image.Image,
                      lang: str = "eng",
                      config: str = "--psm 12 --oem 3") -> List[Dict]:
        """Compute a dictionary with detected words and bounding boxes.

        :param im: input image
        :param lang: language code
        :param config: tesseract configuration
        :return: list of dictionaries of type {"word": word, "bb": bounding box of the word, relative to page size}
        """
        d = pytesseract.image_to_data(
            im, output_type=pytesseract.Output.DICT, lang=lang, config=config)
        result = []
        for i in range(len(d["level"])):
            word = d["text"][i]
            if word.strip():
                left, top, width, height = d["left"][i], d["top"][i], d["width"][i], d["height"][i]
                result.append({
                    "word": word,
                    "bb": Rectangle(left, top, left + width, top + height).relative_to_size(
                        width=im.size[0],
                        height=im.size[1]
                    )
                })
        return result

    @classmethod
    def image_to_one_page_ocred_pdf(cls,
                                    im: Image.Image,
                                    pdf_path: str,
                                    pdf_width: int,
                                    pdf_height: int,
                                    ocr_text: List[Dict],
                                    font_name: str = "Helvetica") -> None:
        """Convert the image into a pdf with added textual layer and store it to disc.

        Run tesseract OCR and add invisible textual content so that the pdf is searchable / clickable.
        :param im: input image
        :param pdf_path: path to output pdf
        :param pdf_width: widht of the pdf to be created
        :param pdf_height: height of the pdf to be created
        :param ocr_text: information about words and their bounding boxes in relative coordinates
        (such as the output of `ocr_one_image`)
        :param font_name
        """
        new_pdf = Canvas(pdf_path, pagesize=(pdf_width, pdf_height))
        new_pdf.drawImage(
            ImageReader(im),
            0, 0, width=pdf_width, height=pdf_height)

        for word_and_position in ocr_text:
            word = word_and_position["word"]
            bb = word_and_position["bb"].rescale(multiply_width_by=pdf_width, multiply_height_by=pdf_height)

            text = new_pdf.beginText()
            text.setFont(font_name, bb.height)
            text.setTextRenderMode(3)  # invisible
            text.setTextOrigin(bb.x_min, pdf_height - bb.y_max)  # bottom-left corner
            text.setHorizScale(100 * bb.width / new_pdf.stringWidth(word, "Helvetica", bb.height))
            text.textLine(word)
            new_pdf.drawText(text)

        new_pdf.save()
