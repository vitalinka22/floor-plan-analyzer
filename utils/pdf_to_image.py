import fitz
from PIL import Image
import io

def pdf_to_images(pdf_path):
    """Convert each page of a PDF to an image and return a list of images
    Args: 
        pdf_path: Path to the PDF file on a disk

    Returns:
    List of PIL Image objects, one per page, rendered at 200 DPI.
    """
    images = []

    doc = fitz.open(pdf_path)

    for page in doc:

        pix = page.get_pixmap(dpi=200)

        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        images.append(img)
    return images

if __name__ == "__main__":
    images = pdf_to_images("input/Floorplan_P1_Mosbach.pdf")
    print(f"Number of pages: {len(images)}")
    print(f"Image size: {images[0].size}")
    images[0].save("output/test_page.png")
    print("Saved to output/test_page.png!")



