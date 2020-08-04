## Tools for processing pdf files

This is a small and light-weighted library for processing pdf files in python.
One of the use-cases might be the extraction of pdf-annotations for ML / NLP.

Support for

* obtaining textual and vizual content of pdf files
* locating positions of words
* fetching pdf annotations
* adding digital layer to image-pdfs
* re-creating a clean pdf file with annotations removed


## Dependencies

Main tool for reading pdf files is the PyPDF2 library.

Apart of pip requirement, you should have [Poppler](https://poppler.freedesktop.org/), [Tesseract](https://tesseract-ocr.github.io/tessdoc/Home.html) and [OpenCV](https://opencv.org/) installed. 
We use Poppler mainly for extracting images and text from pdfs, and Tesseract is needed for pytesseract.

## How to

Some examples of usage are shown in the notebook.

## Todo

* Get rid of PyPDF2 as [it is not maintained](https://stackoverflow.com/questions/63199763/maintained-alternatives-to-pypdf2) and replace by PyMUPdf.
* Add detection of page-orientation (upside-down) based on images.
* ...
