from PIL import ImageEnhance, ImageFilter,Image
import pytesseract

try:    
    

    # Open the image
    image = Image.open('temp/rotated_fixed.jpg')

    # Convert to grayscale
    gray_image = image.convert('L')

    # Enhance contrast
    enhanced_image = ImageEnhance.Contrast(gray_image).enhance(2.0)

    # Apply Gaussian blur
    blurred_image = enhanced_image.filter(ImageFilter.GaussianBlur(radius=2))

    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(blurred_image, config='--psm 6 --oem 3')

    print("image_data==>>", extracted_text)

except Exception as e:
    print(f"error: {e}")
