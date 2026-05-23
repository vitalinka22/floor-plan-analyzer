import pdfplumber

def extract_text_with_coordinates(pdf_path):
    """Extract all words with their coordinates from a PDF file.

    Args:
        pdf_path: Path to the PDF file on disk.

    Returns:
        dict with keys:
            - "words": list of word dicts (text, x0, y0, x1, y1)
            - "page": dict with "width" and "height" of the last page
    """
        
    all_words=[]
    page_dimensions={}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()
            all_words.extend(words)
            page_dimensions = {"width": page.width, "height": page.height}

    return {"words": all_words, "page": page_dimensions}

if __name__ == "__main__":
    text = extract_text_with_coordinates("input/Floorplan_P1_Mosbach.pdf")
    print(text)