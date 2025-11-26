## 📼 AuraFilm: Film and Camcorder Aesthetic Simulator

This is the **RAW** README file for the provided Python script. The script is designed to apply classic film stock simulations and retro camcorder effects to images.

---

## ✨ Project Overview

**AuraFilm** is a **Python script** that applies complex, multi-step image filters to replicate the look of classic analog film stocks and vintage video recordings. It uses the **Pillow (PIL)** library to handle all image manipulation, including color shifts, contrast adjustments, and the addition of stylistic elements like soft focus, grain, and an authentic glowing date/message stamp.

> ℹ️ This script contains the core image filter functions that are also used in the related **`camcorder-revival-tool`** project, providing a foundation for retro video aesthetics.

---

## 🚀 Core Features & Dependencies

* **Pillow-Based Processing:** Leverages the power of **PIL/Pillow** for all image loading, manipulation (contrast, brightness, blur), and final saving.
* **Pixel-Level Control:** Most film simulations are implemented using **pixel-by-pixel loops** to apply custom RGB shifts, luma-based adjustments, and procedural grain.
* **Authentic Grain:** Adds randomized noise across RGB channels for a realistic film or video grain appearance.
* **Retro Timestamp:** Includes the `add_timestamp` function to generate a distinctive, glowing, bottom-left date stamp and an optional top-right message, mimicking old video overlays.

### 🎨 Included Aesthetic Simulations

The following unique filter simulations are available in the script:

| Simulation Name | Aesthetic Summary | Key Characteristics |
| :--- | :--- | :--- |
| `modern_fuji_sim` | **Cool & Low Saturation** | Subtle cool shift, slight de-saturation, blended luma effect. |
| `terracotta_sun_sim` | **Warm, Red/Magenta, Soft** | Strong warmth with red/magenta push, conditional blue shift, high softening, visible grain. |
| `portra_800_sim` | **High Saturation & Warm** | Strong contrast reduction, high color boost, very visible grain, pronounced warm/pink shift. |
| `reala_ace_sim` | **Balanced, Cool, Medium Contrast** | Balanced color profile with a slight cool tilt, medium contrast reduction, subtle grain. |
| `dreamy_negative_sim` | **Muted, Matte & Very Warm** | Low contrast, lifted shadows (matte black), strong color boost, pronounced warm white balance. |

---

## ⚙️ How to Use (Standalone Script)

The script is configured to process a single input image and save the filtered result based on a selected filter and user-defined text inputs.

### 1️⃣ Setup

Install the single required dependency using `pip`:

```bash
pip install pillow
```
### 2️⃣ Preparing the Image

1.  **Save your input photo** in the same directory as the script.
2.  **Rename your photo** to `your_input_photo.jpg` (or the name specified in the script's `input_file` variable). The script will create a placeholder if it doesn't find the file.

### 3️⃣ Running the Filter

Run the script directly from your terminal:

```bash
python your_script_name.py
```
The script will prompt you for:
* A **short message** for the top-right corner.
* The **month, day, and 2-digit year** for the timestamp (defaults to the current date if left blank).

### 4️⃣ Reviewing the Output

The processed image will be saved to the same directory with a filename like `retro_output_CHOSEN_FILTER.jpg`.
