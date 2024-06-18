import fitz
import os
import string
import shutil

def clean_up_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

def extract_text_at_coordinates(page, x1, y1, x2, y2):
    rect = fitz.Rect(x1, y1, x2, y2)
    text = page.get_text("text", clip=rect)
    return text.strip()

def export_pdf_with_custom_naming(input_pdf, output_folder, output_type, dpi=120/72):
    clean_up_output_folder(output_folder)
    pdf_document = fitz.open(input_pdf)
    
    for page_number in range(len(pdf_document)):

        page = pdf_document[page_number]
        
        x1, y1, x2, y2 = 500, 580, 567, 582 
        
        extracted_text = extract_text_at_coordinates(page, x1, y1, x2, y2)
        
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c if c in valid_chars else '_' for c in extracted_text)
        if output_type == "PDF":
            # Create a new PDF document with the current page
            pdf_output = fitz.open()
            pdf_output.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
            
            # Define the output PDF file path
            pdf_output_file = os.path.join(output_folder, f"{filename}.pdf")
            
            # Save the single-page PDF to the output PDF file
            pdf_output.save(pdf_output_file)
        elif output_type == "JPEG":
            img = page.get_pixmap(matrix=fitz.Matrix(dpi, dpi))  # Set DPI to 300 (adjust as needed)
            img_path = os.path.join(output_folder, f"{filename}.jpg")
            img.save(img_path, "JPEG")
        else:
            print("Invalid output type")
            return
    
    pdf_document.close()

if __name__ == '__main__':
    # input_pdf_file = "Bulletin 8.pdf"  
    # output_folder = "output_images"
    # DPI = 120/72
    input_pdf_file = input("Enter the name of the pdf file: ")
    output_folder = input("Enter the name of the output folder: ")
    print("Enter the DPI for x and y axis x/y example: 120/72")
    DPI_x = int(input("Enter the DPI for x axis: "))
    DPI_y = int(input("Enter the DPI for y axis: "))
    DPI = DPI_x/DPI_y
    output_type = input("Enter the output type PDF or JPEG: ").strip().upper()
    export_pdf_with_custom_naming(input_pdf_file, output_folder, output_type, DPI)