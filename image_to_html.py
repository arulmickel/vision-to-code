import cv2
import json
from pathlib import Path
from utils.webpage_handler import WebpageHandler
import argparse
import os
import numpy as np

def convert_image_to_html(image_path, output_dir="output"):
    """
    Convert a UI image to HTML code
    
    Args:
        image_path (str): Path to the input image
        output_dir (str): Directory to save the output files
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Initialize the handler
    handler = WebpageHandler()
    
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Could not read image at {image_path}")
    
    # Save the image in the output directory
    frame_path = os.path.join(output_dir, "frame.jpg")
    cv2.imwrite(frame_path, image)

    # Generate and save Grayscale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscale_path = os.path.join(output_dir, "grayscale_frame.jpg")
    cv2.imwrite(grayscale_path, gray_image)
    print(f"Grayscale image saved to: {grayscale_path}")

    # Generate and save Detected Components image (using Canny and contours)
    # First, get edges
    temp_handler = WebpageHandler() # Create a temporary handler to access detect_edges
    edges_coordinates = temp_handler.detect_edges(image)

    # Draw contours on a blank image or a copy of the original image
    detected_components_image = image.copy() # Draw on a copy of the original image
    # Convert edge coordinates to a format suitable for cv2.drawContours (list of numpy arrays)
    contours = [np.array([[p['x'], p['y']]]) for p in edges_coordinates]
    if contours: # Ensure contours are not empty
        # Reshape to match cv2.drawContours expected format: list of arrays of points
        # Need to group connected points, but for simple visualization, drawing all points is fine
        # For drawing outlines, we need actual contours from findContours, not just points.
        # Let's re-run Canny and find contours for drawing.
        gray_for_contours = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges_for_drawing = cv2.Canny(gray_for_contours, 100, 200)
        # Find contours from the binary edge image
        drawing_contours, _ = cv2.findContours(edges_for_drawing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw all found contours in a distinct color (e.g., green)
        cv2.drawContours(detected_components_image, drawing_contours, -1, (0, 255, 0), 2) # -1 draws all contours
    
    detected_components_path = os.path.join(output_dir, "detected_components.jpg")
    cv2.imwrite(detected_components_path, detected_components_image)
    print(f"Detected components image saved to: {detected_components_path}")
    
    # Process the image using direct analysis
    preprocessor = handler.preprocessor
    direct_analysis = preprocessor.direct_image_understanding(image)
    
    # Generate HTML using the analysis
    prompt = f"""
    Generate ONLY a complete, runnable HTML code for this UI design.
    DO NOT include any explanations or markdown, ONLY the HTML code.

    Analysis Data:
    {direct_analysis}

    Technical Requirements:
    1. Use Tailwind CSS (via CDN)
    2. Use Alpine.js for interactivity (via CDN)
    3. Implement:
    - Responsive layout
    - Dark/light mode toggle
    - Interactive components
    - Image display (use 'frame.jpg' as src)
    - Loading states
    - Hover effects

    The HTML must include:
    - <!DOCTYPE html> declaration
    - All necessary meta tags
    - Tailwind and Alpine.js CDN links
    - Proper viewport settings
    - All CSS and JavaScript inline
    - Error handling
    - Accessibility features
    - Touch support

    IMPORTANT: Output ONLY the complete HTML code that starts with <!DOCTYPE html>, nothing else.
    """
    
    html_result = handler.llm_util.native_chat(prompt)
    
    # Debugging: Print the raw HTML result to the console
    print("\n--- Raw HTML Result from Gemini ---")
    print(html_result)
    print("--- End of Raw HTML Result ---\n")

    # Save the HTML
    html_path = f"{output_dir}/index.html"
    with open(html_path, "w", encoding='utf-8') as f:
        f.write(html_result)
    
    print(f"HTML has been generated and saved to: {html_path}")
    print(f"Original image has been saved to: {frame_path}")
    return html_path

def main():
    parser = argparse.ArgumentParser(description='Convert UI image to HTML')
    parser.add_argument('--image', '-i', required=True, help='Path to the input image')
    parser.add_argument('--output', '-o', default='output', help='Output directory path')
    
    args = parser.parse_args()
    
    try:
        html_path = convert_image_to_html(args.image, args.output)
        print("\nTo view the result:")
        print(f"1. Open {html_path} in your web browser")
        print("2. The page will show the original image and the generated HTML implementation")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 