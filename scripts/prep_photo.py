import sys
import os
import numpy as np
import cv2
from PIL import Image
from rembg import remove

def prep_photo(input_path, output_path="source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        sys.exit(1)

    print("1/3 Removing background...")
    with open(input_path, 'rb') as f:
        img_data = f.read()
    no_bg = remove(img_data)
    
    # Convert bytes to PIL Image
    pil_img = Image.open(io.BytesIO(no_bg)).convert("RGBA")
    
    # Composite over pure white background
    white_bg = Image.new("RGBA", pil_img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, pil_img).convert("L")
    
    print("2/3 Applying CLAHE contrast enhancement...")
    np_img = np.array(composited)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(np_img)
    
    print("3/3 Saving prepped photo...")
    cv2.imwrite(output_path, enhanced)
    print(f"Done! Saved prepped image to {output_path}")

if __name__ == "__main__":
    import io
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(src)
