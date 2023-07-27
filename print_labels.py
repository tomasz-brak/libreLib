import pymongo
from PIL import Image, ImageDraw, ImageFont
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import utils
import os
import subprocess
import tempfile


def generate_labels(titles: list[str], ids: list[int], add_text: str) -> Image:
    # A4

    A4 = (2480, 3508)
    X_DIV = 4
    Y_DIV = 10
    FONT_SIZE = 32

    CHAR_LIMIT = 25

    per_page = X_DIV * Y_DIV
    X_offset = A4[0] // X_DIV
    Y_offset = A4[1] // Y_DIV

    offsets = {
        "barcode": (50, 50),
        "id": (50, 0),
        "title": (30, 300),
        "add_text": (0, 0),
    }

    # page_vis = []

    # for i in range(X_DIV):
    #     row = []
    #     for j in range(Y_DIV):
    #         row.append((i, j))
    #     page_vis.append(row)

    # for row in page_vis:
    #     print(row)

    # New image
    blank_page = Image.new("RGB", A4, (255, 255, 255))
    blank_page_draw = ImageDraw.Draw(blank_page)

    # Clean the titles:

    titles = [title.replace("\n", "") for title in titles]

    for i, title in enumerate(titles):
        if len(title) > CHAR_LIMIT:
            title = title[:CHAR_LIMIT] + "..."
        titles[i] = title

    def draw_lines(to_be_drawn: Image):
    # Draw the verical lines
        to_be_drawn_draw = ImageDraw.Draw(to_be_drawn)
        A4[0] / X_DIV
        X_line_cords = []
        last = 0
        for i in range(X_DIV):
            X_line_cords.append(last)
            last += A4[0] / X_DIV

        for x in X_line_cords:
            to_be_drawn_draw.line([(x, 0), (x, A4[1])], fill=(0, 0, 0))

        # Draw the horizontal lines
        A4[1] / Y_DIV
        Y_line_cords = []
        last = 0
        for i in range(Y_DIV):
            Y_line_cords.append(last)
            last += A4[1] / Y_DIV

        for y in Y_line_cords:
            to_be_drawn_draw.line([(0, y), (A4[0], y)], fill=(0, 0, 0))

        return to_be_drawn

    how_many_full_pages = len(titles) // per_page
    additional_page = 1 if len(titles) % per_page != 0 else 0


    font = ImageFont.truetype("Roboto-Medium.ttf", FONT_SIZE)

    # draw per sticker features
    def draw_features(title, id, add_text) -> Image:
        
        image = Image.new("RGB", (A4[0] // X_DIV, A4[1] // Y_DIV), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        writer = ImageWriter()
        writer.set_options({'quiet_zone': 0, "background": "transparent"})
        barcode = Code128(str(id), writer)
        image.paste(barcode.render(), offsets["barcode"])

        draw.text(offsets["title"], title, (0, 0, 0), font)
        draw.text(offsets["add_text"], add_text, (0, 0, 0), font)


        return image

    pages = []

    feature_id = 0
    for i in range(how_many_full_pages + additional_page):
        page = Image.new("RGB", A4, (255, 255, 255))
        for x in range(X_DIV):
            for y in range(Y_DIV):
                if feature_id >= len(ids):
                    break

                cords = (x * (A4[0]//X_DIV), y * (A4[1] // Y_DIV))
                page.paste(draw_features(titles[feature_id], ids[feature_id], add_text), cords)
                print(f"F_id: {feature_id}, title: {titles[feature_id]}, ids: {ids[feature_id]}, page: {i}, x: {x}, y: {y}")
                feature_id += 1
                if len(pages) == i:
                    pages.append(page)
                else:
                    pages[i] = page

    pages = [draw_lines(page) for page in pages]

    # combine the pages in to a pdf
    pdf_temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

    pdf = canvas.Canvas(pdf_temp_file.name, pagesize=A4)

    for page in pages:
        pdf.drawImage(utils.ImageReader(page), 0, 0)
        pdf.showPage()
    pdf.save()
    


    if os.name == "nt":  # For Windows
        os.startfile(pdf_temp_file.name)
    elif os.name == "posix":  # For macOS and Linux
        subprocess.run(["xdg-open", pdf_temp_file.name], check=True)
    
    pdf_a = canvas.Canvas("test.pdf", A4)
    for page in pages:
        pdf_a.drawImage(utils.ImageReader(page), 0, 0)
        pdf_a.showPage()
    pdf_a.save()
    


if __name__ == "__main__":
    generate_labels()
