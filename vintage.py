from PIL import Image, ImageEnhance, ImageDraw, ImageFilter, ImageFont
import os
import math
import random 
from datetime import datetime 

def apply_clarity_softening(img, strength):
    """
    Applies a subtle Gaussian blur to simulate lens softening or halation.
    For Clarity +4, we apply a negative strength (sharpening), which is approximated 
    by skipping the blur here and relying on PIL's built-in sharpening.
    """
    # If strength is positive (like the old Clarity -4), apply blur/softening.
    if strength > 0:
        # A strength of 4 (from Clarity -4) means a strong, dreamy blur
        radius = strength / 2.5 
        img = img.filter(ImageFilter.GaussianBlur(radius))
    return img

def add_timestamp(img, timestamp_text, message_text=""):
    """
    Adds the retro-style glowing date stamp (bottom-left) and an optional 
    message (top-right, both using the same font size).
    """
    width, height = img.size
    
    # --- CONFIGURATION VARIABLES ---
    # Font size multiplier (currently 0.018 for small text)
    FONT_SIZE_MULTIPLIER = 0.018 
    
    # REVERSED COLOR CONFIGURATION: Bright Core (like a light source) with a Deep Orange Halo (the burn effect)
    # Core Color (RGB): The bright center of the text (brighter, yellow-ish orange)
    CORE_COLOR = (250, 189, 90) 
    # Halo Color (RGBA): The soft glow/shadow around the text (deeper, burnt orange, semi-transparent)
    HALO_COLOR = (255, 120, 0, 120) 
    # -------------------------------
    
    # --- Combined Font (Both message and date use this) ---
    font_size = int(height * FONT_SIZE_MULTIPLIER) 
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback if 'arial.ttf' is not found
        font = ImageFont.load_default()
        font_size = int(height * (FONT_SIZE_MULTIPLIER + 0.01)) 
        font = ImageFont.load_default().font_variant(size=font_size)
    
    # Standard padding from the edge
    padding_x = int(width * 0.03)
    padding_y = int(height * 0.03)
    
    draw_temp = ImageDraw.Draw(img)
    
    # Calculate dimensions for the DATE string (for alignment)
    bbox_date = draw_temp.textbbox((0, 0), timestamp_text, font=font)
    date_text_height = bbox_date[3] - bbox_date[1]

    # --- Date Position (Bottom Left) ---
    date_x = padding_x
    date_y = height - date_text_height - padding_y
    date_position = (date_x, date_y)
    
    # Structure: (text, position, font_object)
    texts_to_draw = [(timestamp_text, date_position, font)]

    # Add message if provided (positioned to the top right of the image)
    clean_message = message_text.strip()
    if clean_message:
        # Calculate dimensions for the MESSAGE string
        bbox_message = draw_temp.textbbox((0, 0), clean_message, font=font)
        message_text_width = bbox_message[2] - bbox_message[0]
        
        # --- Message Position (TOP Right) ---
        # X position: Total width - padding_x - message_width
        message_x = width - padding_x - message_text_width
        # Y position: Set to padding_y for top alignment
        message_y = padding_y 
        message_position = (message_x, message_y)
        
        texts_to_draw.append((clean_message, message_position, font))

    # --- GLOW IMPLEMENTATION ---
    glow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    # Draw the soft halo for all texts, using the combined font
    for text, pos, current_font in texts_to_draw:
        x_pos, y_pos = pos
        for i in range(3, 0, -1):
            # Use the deeper orange halo color
            glow_draw.text((x_pos + i, y_pos + i), text, fill=HALO_COLOR, font=current_font)
            glow_draw.text((x_pos - i, y_pos - i), text, fill=HALO_COLOR, font=current_font)
            glow_draw.text((x_pos, y_pos + i), text, fill=HALO_COLOR, font=current_font)
            glow_draw.text((x_pos, y_pos - i), text, fill=HALO_COLOR, font=current_font)
    
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(1.5))

    img = Image.alpha_composite(img.convert('RGBA'), glow_layer).convert('RGB')
    
    # Draw the final bright core for all texts, using the combined font
    draw_final = ImageDraw.Draw(img)
    # Use the bright, yellow-ish orange core color
    for text, pos, current_font in texts_to_draw:
        draw_final.text(pos, text, fill=CORE_COLOR, font=current_font)
    
    return img


def apply_filter_modern_fuji_sim(img):
    """Applies a 'Modern Fuji' film simulation look (cool tones, low saturation)."""
    
    img = ImageEnhance.Contrast(img).enhance(0.95)
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = apply_clarity_softening(img, 0)
    
    width, height = img.size
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            luma = 0.299 * r + 0.587 * g + 0.114 * b
            
            new_r = r + 15
            new_g = g + 5
            new_b = b - 10
            
            blend_factor = 0.05 
            new_r = int(new_r * (1 - blend_factor) + luma * blend_factor)
            new_g = int(new_g * (1 - blend_factor) + luma * blend_factor)
            new_b = int(new_b * (1 - blend_factor) + luma * blend_factor)
            
            pixels[x, y] = (max(0, min(255, new_r)), max(0, min(255, new_g)), max(0, min(255, new_b)))
            
    return img

def apply_filter_terracotta_sun_sim(img):
    """
    Applies a 'Terracotta Sun' film simulation, now emphasizing a deeper, 
    more brick-red/magenta hue while integrating blue tones.
    """
    # 1. High softening/halation (Clarity -4)
    img = apply_clarity_softening(img, 4.0)
    
    # 2. Lift shadows and lower highlights (Contrast 0.85, H-2/S-1.5)
    img = ImageEnhance.Contrast(img).enhance(0.85)
    
    # 3. Increase Saturation (Color +2, Color Chrome Strong)
    img = ImageEnhance.Color(img).enhance(1.35) 
    
    width, height = img.size
    pixels = img.load()
    
    # Small / Weak Grain (Grain Amount 5)
    grain_amount = 5 
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Check if this pixel is significantly blue (e.g., sky)
            # Threshold: Blue must be much higher than the average of Red and Green
            # This ensures we only apply the selective shift to true blues.
            is_blue = b > ((r + g) / 2) + 30 

            if is_blue:
                # 4a. Conditional Blue Shift (To make the sky less vibrant blue and more dusty/integrated)
                # This shift pushes the blue tones toward magenta/purple, muting them.
                new_r = r + 15  # Small red boost
                new_g = g - 10  # Reduce green (removes cyan/green cast)
                new_b = b - 70  # Aggressively reduce blue saturation/luminance
            else:
                # 4b. Standard Terracotta Shift (for all other tones: skin, ground, reds)
                new_r = r + 40
                new_g = g - 5      
                new_b = b - 35 
            
            # 5. Add Grain
            new_r += random.randint(-grain_amount, grain_amount)
            new_g += random.randint(-grain_amount, grain_amount)
            new_b += random.randint(-grain_amount, grain_amount)
            
            pixels[x, y] = (max(0, min(255, new_r)), max(0, min(255, new_g)), max(0, min(255, new_b)))
            
    return img


def apply_filter_portra_800_sim(img):
    """Applies a 'Portra 800' style simulation (high saturation, warm reds/pinks, visible grain)."""
    
    img = ImageEnhance.Brightness(img).enhance(1.08)
    
    img = ImageEnhance.Contrast(img).enhance(0.85)
    
    img = ImageEnhance.Color(img).enhance(1.3)
    
    img = apply_clarity_softening(img, 1.5) 
    
    width, height = img.size
    pixels = img.load()
    
    grain_amount = 15 
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            new_r = r + 20 - 1 
            new_g = g + 10     
            new_b = b - 30 - 3 
            
            new_r += random.randint(-grain_amount, grain_amount)
            new_g += random.randint(-grain_amount, grain_amount)
            new_b += random.randint(-grain_amount, grain_amount)
            
            pixels[x, y] = (max(0, min(255, new_r)), max(0, min(255, new_g)), max(0, min(255, new_b)))
            
    return img


def apply_filter_reala_ace_sim(img):
    """Applies a 'Reala Ace' style simulation (balanced colors, slightly cool, medium contrast)."""
    
    img = ImageEnhance.Brightness(img).enhance(1.0) 
    
    img = ImageEnhance.Contrast(img).enhance(0.8)
    
    img = ImageEnhance.Color(img).enhance(1.2)
    
    img = apply_clarity_softening(img, 2) 
    
    width, height = img.size
    pixels = img.load()
    
    grain_amount = 5 
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            new_r = r - 10 - 1  
            new_g = g + 10      
            new_b = b + 10 + 1  
            
            new_r += random.randint(-grain_amount, grain_amount)
            new_g += random.randint(-grain_amount, grain_amount)
            new_b += random.randint(-grain_amount, grain_amount)
            
            pixels[x, y] = (max(0, min(255, new_r)), max(0, min(255, new_g)), max(0, min(255, new_b)))
            
    return img


def apply_filter_dreamy_negative_sim(img):
    """
    Applies a 'Dreamy Negative' film simulation based on Fuji settings: 
    Warm tones, strong color, low contrast, lifted blacks (matte look), and subtle grain.
    Settings: Classic Negative, Grain Weak/Small, Color +2, Highlight -2, Shadow -1.5, Clarity 0, WB +4 Red -7 Blue.
    """
    
    # 1. Base Adjustments: Low Contrast & High Saturation
    # Contrast (Highlight -2, Shadow -1.5): Reduces overall contrast, especially in highlights/shadows.
    img = ImageEnhance.Contrast(img).enhance(0.90) 
    # Color (+2, Color Chrome Strong): Strong color boost
    img = ImageEnhance.Color(img).enhance(1.50) 
    # Clarity (0)
    img = apply_clarity_softening(img, 0)
    
    width, height = img.size
    pixels = img.load()
    
    # Grain Effect (Weak / Small)
    grain_amount = 8 
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # 2. White Balance Shift (Warmth: +4 Red, -7 Blue)
            # We use stronger values (e.g., +20 R, -20 B) for a noticeable effect.
            new_r = r + 20
            new_g = g
            new_b = b - 20
            
            # 3. Shadow/Highlight Shaping (Highlight -2, Shadow -1.5)
            # This is key for the "Dreamy" look: lifting shadows for matte blacks
            luma = 0.299 * r + 0.587 * g + 0.114 * b
            
            # Lift Shadows (Matte Look): Add some light to dark areas (luma < 60)
            if luma < 60:
                # 20% lift in the shadows
                lift = (60 - luma) * 0.2 
                new_r += int(lift)
                new_g += int(lift)
                new_b += int(lift)

            # Darken Highlights: Reduce intensity of bright areas (luma > 200)
            if luma > 200:
                # 15% reduction in the highlights
                darken = (luma - 200) * 0.15 
                new_r -= int(darken)
                new_g -= int(darken)
                new_b -= int(darken)

            # 4. Add Grain
            noise = random.randint(-grain_amount, grain_amount)
            new_r += noise
            new_g += noise
            new_b += noise
            
            # 5. Clamp values
            pixels[x, y] = (max(0, min(255, new_r)), max(0, min(255, new_g)), max(0, min(255, new_b)))
            
    return img


def apply_selected_filter(input_path, output_path, filter_name, timestamp_text, message_text):
    """Loads an image, applies the chosen filter, and saves the final image."""
    
    filter_functions = {
        "modern_fuji_sim": apply_filter_modern_fuji_sim,
        "terracotta_sun_sim": apply_filter_terracotta_sun_sim,      
        "portra_800_sim": apply_filter_portra_800_sim,              
        "reala_ace_sim": apply_filter_reala_ace_sim,                
        "dreamy_negative_sim": apply_filter_dreamy_negative_sim, 
    }
    
    if filter_name not in filter_functions:
        print(f"Error: Unknown filter name '{filter_name}'. Please choose from: {', '.join(filter_functions.keys())}")
        return

    try:
        img = Image.open(input_path).convert("RGB")
        
        # STEP 1: Apply the filter to the original image first.
        filtered_img = filter_functions[filter_name](img)
        
        # STEP 2: Apply the date stamp and message LAST to the already filtered image.
        # This ensures the stamp is clean and only interacts with the final background color/grain.
        final_img = add_timestamp(filtered_img, timestamp_text, message_text) 
        
        final_img.save(output_path)
        print(f"Successfully applied filter '{filter_name}'. Output saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"An error occurred during image processing: {e}")

# --- Example Usage & Configuration ---

# >>> 1. CHOOSE YOUR FILTER HERE <<<
# Options: "modern_fuji_sim", "terracotta_sun_sim", "portra_800_sim", 
#          "reala_ace_sim", "dreamy_negative_sim" (NEW)
CHOSEN_FILTER = "dreamy_negative_sim"

# --- 2. GET USER INPUT ---
message = input("Enter a short message to appear on the top right (e.g., 'DAY 1', leave blank for none): ")
month = input("Enter the month (MM, press Enter for current month): ")
day = input("Enter the day (DD, press Enter for current day): ")
year = input("Enter the 2-digit year (YY, press Enter for current year): ")

# Handle blank inputs by defaulting to current date components
now = datetime.now()
m = month.strip() if month.strip() else now.strftime("%m")
d = day.strip() if day.strip() else now.strftime("%d")
y = year.strip() if year.strip() else now.strftime("%y")

custom_timestamp_text = f"{m}-{d}-'{y}"

# --- File Paths (Keep these consistent) ---
input_file = "your_input_photo.jpg"
output_file = f"retro_output_{CHOSEN_FILTER}.jpg" 

if not os.path.exists(input_file):
    print(f"Input image '{input_file}' not found. Creating a placeholder image for demonstration.")
    try:
        placeholder = Image.new('RGB', (400, 300), color = '#E0F7FA') 
        d_draw = ImageDraw.Draw(placeholder)
        try:
             font = ImageFont.truetype("arial.ttf", 18)
        except IOError:
             font = ImageFont.load_default()
        d_draw.text((20, 100), "REPLACE THIS FILE with your photo.\nRename your picture to 'your_input_photo.jpg'", fill=(0, 51, 102), font=font)
        placeholder.save(input_file)
        print("Created placeholder 'your_input_photo.jpg'. Running filter on placeholder.")
    except Exception as e:
        print(f"Could not create placeholder: {e}")
        simple_placeholder = Image.new('RGB', (400, 300), color = 'gray')
        simple_placeholder.save(input_file)
    
# Run the selected filter function with the new inputs
apply_selected_filter(input_file, output_file, CHOSEN_FILTER, custom_timestamp_text, message)