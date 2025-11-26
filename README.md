# 🎞️ AuraFilm: Vectorized Film Simulations

<div align="center">

</div>

## ✨ 🌟 Project Overview

**AuraFilm** is a high-performance **Python tool** dedicated to replicating the authentic, analog look of classic film stocks. This script leverages the power of **NumPy vectorization** to apply complex color shifts, grain, and tonal adjustments directly to image arrays, resulting in beautiful and highly efficient film simulation effects.

> ℹ️ This script contains the core image filter functions that are also used in the related `camcorder-revival-tool` project.

## 🚀 Core Features & Simulations

The library is built for speed and authenticity:

* **⚡ Vectorized Speed:** All core logic (color shifts, contrast, grain) is implemented using **NumPy** arrays, ensuring superior performance over traditional pixel-by-pixel loops.

* **🧪 Procedural Grain:** Highly realistic noise addition, applied directly in the NumPy domain for speed and an organic film look.

* **Minimal Dependencies:** Focused solely on two essential packages: `numpy` and `Pillow (PIL)`.

### 🎨 Included Film Aesthetic Simulations

| Simulation Name | Aesthetic Summary | Key Characteristics | 
 | ----- | ----- | ----- | 
| `modern_fuji_sim` | **Cool & Saturated** | Cool greens, strong blues, high fidelity. | 
| `terracotta_sun_sim` | **Warm & High Contrast** | Deep reds, crushed shadows, cinematic warmth. | 
| `portra_800_sim` | **Soft & Fine Grain** | Soft colors, high saturation, distinct grain. | 
| `reala_ace_sim** | **Smooth & Punchy** | Low grain, clear blacks, punchy highlights. | 
| `dreamy_negative_sim` | **Muted & Shadow Lift** | Lifted shadows, soft contrast, dreamy mood. | 

## ⚙️ How to Use (As a Standalone Script)

The tool processes an input image file and saves the filtered result.

### 1️⃣ Setup

You only need to download the Python file (e.g., `aura_film_script.py`) and install the necessary packages using `pip`:
pip install numpy pillow

### 2️⃣ Applying a Filter

You can run the script directly from your terminal. Replace `input_photo.jpg` with your file and choose one of the filters from the table above.

## 🧩 Filter Processing Structure

All filters follow a structured, multi-step process to maximize performance by minimizing repeated type conversions:

1. **PIL Pre-Adjustment:** Use PIL's `ImageEnhance` for efficient global control (Contrast, Brightness).

2. **Clarity/Softening:** Apply light Gaussian blur using `ImageFilter` (Simulating Halation/Light-Spill).

3. **NumPy Conversion:** Convert the PIL image to a **NumPy array** (`np.array(img, dtype=np.int16)`).

4. **Vectorized Color Shift:** Apply RGB channel offsets and tonal curve simulations across the entire array (e.g., `arr[..., 0] += 19`).

5. **Grain/Noise:** Add **vectorized random noise** (`add_noise_vectorized`).

6. **Final PIL Conversion:** Clip and convert the array back to a PIL image (`Image.fromarray`).

## 🤝 Contribution & Future Focus

Contributions are welcome! If you have a suggestion for a new film stock simulation or an optimization, please feel free to open an issue or submit a pull request.

**Potential Areas for Contribution:**

* **Dynamic Range:** Implementing separate shadow/highlight color control (Luma masking).

* **Film Stocks:** Adding more classic film looks (e.g., Kodachrome, Ektar 100).

* **Benchmarking:** Performance comparison against other filtering methods.
