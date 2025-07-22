import fitz  # PyMuPDF
import os
import json

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text_data = {}
    for i, page in enumerate(doc):
        text = page.get_text()
        text_data[f"page_{i+1}"] = text.strip()
    return text_data

def extract_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    os.makedirs(output_folder, exist_ok=True)

    image_paths = {}
    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)

        paths = []
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            img_path = f"{output_folder}/page{page_index+1}_img{img_index+1}.{ext}"

            with open(img_path, "wb") as f:
                f.write(image_bytes)

            paths.append(img_path)

        image_paths[f"page_{page_index+1}"] = paths
    return image_paths

def build_json(text_data, image_paths):
    result = []
    for page, text in text_data.items():
        images = image_paths.get(page, [])
        if not images:
            continue
        question = {
            "question": text.split('\n')[0],  # Take first line as question
            "images": images[0] if images else "",
            "option_images": images[1:] if len(images) > 1 else []
        }
        result.append(question)
    return result

def main():
    pdf_path = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"  # Change to your actual file
    image_folder = "images"
    json_output_path = "output.json"

    text_data = extract_text(pdf_path)
    image_paths = extract_images(pdf_path, image_folder)
    questions_json = build_json(text_data, image_paths)

    with open(json_output_path, "w") as f:
        json.dump(questions_json, f, indent=4)


    print(f"\n Extraction complete. JSON saved to: {json_output_path}")

if __name__ == "__main__":
    main()
    