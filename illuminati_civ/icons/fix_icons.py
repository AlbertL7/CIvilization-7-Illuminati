"""
Script to resize images and apply circular mask with transparent background
to match the style of cult_illuminati.png
"""

from PIL import Image, ImageDraw
import os

def create_circular_image(input_path, output_path, target_size):
    """
    Resize image to target size and apply circular mask with transparent background.
    """
    # Open the image
    img = Image.open(input_path)

    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Resize to target size (square, will be cropped to circle)
    # Use LANCZOS for high-quality downsampling
    img = img.resize((target_size, target_size), Image.LANCZOS)

    # Create a circular mask
    mask = Image.new('L', (target_size, target_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, target_size, target_size), fill=255)

    # Create output image with transparent background
    output = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)

    # Save the result
    output.save(output_path, 'PNG')
    print(f"Saved: {output_path}")

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Reference image to get dimensions
    reference_path = os.path.join(script_dir, 'cult_illuminati.png')

    # Get dimensions from reference image
    with Image.open(reference_path) as ref_img:
        target_size = ref_img.width  # Assuming square image
        print(f"Reference image size: {ref_img.width}x{ref_img.height}")

    # Images to process
    images_to_fix = [
        'hidden_hand_illuminati.png',
        'the_arcanum_illuminati.png',
        'grand_design_illuminati.png'
    ]

    for filename in images_to_fix:
        input_path = os.path.join(script_dir, filename)

        if os.path.exists(input_path):
            # Create backup
            backup_path = os.path.join(script_dir, f"backup_{filename}")
            if not os.path.exists(backup_path):
                img = Image.open(input_path)
                img.save(backup_path)
                print(f"Backup created: {backup_path}")

            # Process the image
            create_circular_image(input_path, input_path, target_size)
        else:
            print(f"File not found: {input_path}")

if __name__ == '__main__':
    main()
    print("\nDone! All images have been processed.")
