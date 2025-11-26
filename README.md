🎞️ AuraFilm: Vectorized Film Simulations

<div align="center">

</div>

🌟 Overview

AuraFilm is a high-performance Python tool dedicated to replicating the authentic, analog look of classic film stocks. This script leverages NumPy vectorization to apply complex, custom, and classic color shifts, grain, and tonal adjustments directly to image arrays, resulting in beautiful and efficient film simulation.

This script contains the core filter functions that are also used in the related camcorder-revival-tool.

✨ Core Features & Simulations

🚀 Vectorized Speed: All core color, brightness, and grain application logic is implemented using NumPy, offering superior performance over traditional pixel-by-pixel processing.

🔬 Procedural Grain: Highly realistic noise addition, applied directly in the NumPy domain for speed and authenticity.

📦 Minimal Dependencies: Focused solely on numpy and Pillow (PIL) for core image manipulation.

Included Film Aesthetic Simulations:

Simulation Name

Aesthetic Summary

Key Characteristics

modern_fuji_sim

Cool & Saturated

Cool greens, strong blues, high fidelity.

terracotta_sun_sim

Warm & High Contrast

Deep reds, crushed shadows, cinematic warmth.

portra_800_sim

Soft & Fine Grain

Soft colors, high saturation, distinct grain.

reala_ace_sim

Smooth & Punchy

Low grain, clear blacks, punchy highlights.

dreamy_negative_sim

Muted & Shadow Lift

Lifted shadows, soft contrast, dreamy mood.

🛠️ How to Use (As a Standalone Script)

The primary goal of this tool is to process an input image file and save the filtered result.

1. Setup

You only need to download the Python file (e.g., aura_film_script.py) and install the necessary packages:

pip install numpy pillow


2. Applying a Filter

You can run the script directly from your terminal. Assuming the single Python file is named aura_film_script.py and contains all the logic, you can adapt the script's main function to accept input/output paths:

# Example: Running the script to apply the Portra 800 simulation
python aura_film_script.py input_photo.jpg output_portra.jpg --filter portra_800_sim

# Note: You may need to edit the Python file's main execution block 
# to select the desired filter function for a run or add command-line argument parsing.


📐 Filter Processing Structure

All filters follow a simple, high-level structure to ensure maximum performance by minimizing repeated type conversions:

PIL Pre-Adjustment: Use PIL's ImageEnhance for efficient global control (Contrast, Brightness).

Clarity/Softening: Apply light Gaussian blur using ImageFilter (Softening/Halation sim).

NumPy Conversion: Convert the PIL image to a NumPy array (np.array(img, dtype=np.int16)).

Vectorized Color Shift: Apply RGB channel offsets and tonal curve simulations across the entire array (e.g., arr[..., 0] += 19).

Grain/Noise: Add vectorized random noise (add_noise_vectorized).

Final PIL Conversion: Clip and convert the array back to a PIL image (Image.fromarray).

🤝 Contribution

Contributions are welcome! If you have a suggestion for a new film stock simulation or an optimization, please feel free to open an issue or submit a pull request.

Focus areas for contribution:

Implementing Dynamic Range simulations (separate shadow/highlight control).

Adding more Classic Film Stocks (e.g., Kodachrome, Ektar 100).

Performance benchmarking against GPU-based solutions.

License

License: MIT
