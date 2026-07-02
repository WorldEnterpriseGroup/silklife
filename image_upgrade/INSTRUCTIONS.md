# SILK Life Image Upgrade Workflow

This document provides step-by-step instructions for upgrading all SILK Life images using the Nanobanana MCP image generator (powered by Gemini 3 Pro Image).

---

## Overview

The original SILK Life images were generated with an older, lower-quality image generator. This workflow upgrades each image using the **Nanobanana MCP** with professional photography parameters.

### Files in This Folder

| File | Purpose |
|------|---------|
| `image_catalog.csv` | Source catalog of all images to upgrade |
| `new_image_catalog.csv` | Destination catalog for upgraded images |
| `INSTRUCTIONS.md` | This file |

---

## MCP Tool Reference

### Primary Tool: `mcp__nanobanana__generate_image`

This is the main tool for generating upgraded images.

**Key Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | **Yes** | Enhanced image description (see prompt template below) |
| `model_tier` | string | No | Use `"pro"` for highest quality |
| `resolution` | string | No | Use `"high"` or `"4k"` for best results |
| `aspect_ratio` | string | No | Match original dimensions (e.g., `"1:1"`, `"3:2"`) |
| `thinking_level` | string | No | Use `"high"` for complex scenes |
| `enable_grounding` | boolean | No | Set `true` for real-world accuracy |
| `negative_prompt` | string | No | Things to avoid in the image |

### Supporting Tools

| Tool | Purpose |
|------|---------|
| `mcp__nanobanana__upload_file` | Upload existing image for reference |
| `mcp__nanobanana__show_output_stats` | View generation statistics |
| `mcp__nanobanana__maintenance` | Clean up old files |

---

## Image Upgrade Workflow

### Step 1: Read Source Image from Catalog

For each row in `image_catalog.csv` where `upgraded` is `false`:

1. Extract the `path` (original image location)
2. Extract the `description` (original prompt)
3. Extract the `dimensions` (to determine aspect ratio)

### Step 2: Enhance the Prompt

Take the original `description` and enhance it with professional photography parameters:

```
PROMPT TEMPLATE:
---------------------------------------------------------
Professional documentary photography, f/11 aperture,
deep depth of field with everything in sharp focus.
[ORIGINAL DESCRIPTION]
Studio-quality lighting, cinematic composition,
photojournalistic authenticity. No text overlays.
---------------------------------------------------------
```

**Required Additions to Every Prompt:**
- `"f/11 aperture"` or `"f/11 or higher f-stop"`
- `"deep depth of field, everything in sharp focus"`
- `"professional lighting"` or `"studio-quality lighting"`
- `"cinematic composition"`
- `"documentary photography style"`
- `"no text overlays, no captions"`

### Step 3: Determine Aspect Ratio

Map the `dimensions` column to the closest aspect ratio. **This ensures proper composition before resizing.**

| Dimensions | Aspect Ratio | Notes |
|------------|--------------|-------|
| 1024x1024 | `"1:1"` | Square |
| 330x330 | `"1:1"` | Square thumbnail |
| 400x400 | `"1:1"` | Square ad |
| 200x200 | `"1:1"` | Small square |
| 330x242 | `"4:3"` | Landscape thumbnail |
| 510x187 | `"21:9"` | Wide banner |
| 1200x200 | `"21:9"` | Wide strip |
| 510x374 | `"4:3"` | Landscape |
| 100x100 | `"1:1"` | Tiny square |

**Important:** Generate at the matching aspect ratio so the image composition is correct. Then resize to exact dimensions in Step 5.

### Step 4: Generate Upgraded Image

Call the Nanobanana MCP tool with these parameters:

```json
{
  "prompt": "[ENHANCED PROMPT FROM STEP 2]",
  "model_tier": "pro",
  "resolution": "high",
  "aspect_ratio": "[FROM STEP 3]",
  "thinking_level": "high",
  "enable_grounding": true,
  "negative_prompt": "text overlays, captions, typography, blurry, shallow depth of field, bokeh, out of focus areas, amateur lighting, harsh shadows, artificial looking, stock photo aesthetic"
}
```

### Step 5: Convert, Resize, and Save the New Image

Nanobanana outputs 1024x1024 PNG. **You MUST resize AND convert to match the original exactly.**

1. The new image will be saved to the nanobanana output directory (PNG)
2. Check the `type` and `dimensions` columns in image_catalog.csv
3. Parse dimensions: `WIDTHxHEIGHT` (e.g., `330x242` → width=330, height=242)

4. **Convert AND resize to match original:**

   **If original is `.webp`:**
   ```bash
   cwebp -q 90 -resize WIDTH HEIGHT /path/to/generated.png -o /mnt/d/silk/silklife/[original-path].webp
   ```
   Example for 330x242:
   ```bash
   cwebp -q 90 -resize 330 242 /path/to/generated.png -o /mnt/d/silk/silklife/images/articles/example.webp
   ```

   **If original is `.png`:**
   ```bash
   convert /path/to/generated.png -resize WIDTHxHEIGHT! /mnt/d/silk/silklife/[original-path].png
   ```
   Example for 330x330:
   ```bash
   convert /path/to/generated.png -resize 330x330! /mnt/d/silk/silklife/images/homepage/example.png
   ```
   (The `!` forces exact dimensions, ignoring aspect ratio)

5. Save directly to the original image location (replacing it)
6. Delete the temporary file from nanobanana output directory
7. Add entry to `new_image_catalog.csv` with all metadata

**Important:** The final image MUST match the original file's format, dimensions, AND path exactly.

### Step 6: Update Source Catalog

After successful generation, update `image_catalog.csv`:
- Set `upgraded` column to `true` for that row

---

## Batch Processing Script

For automated processing, use this workflow:

```python
import csv

# Read catalog
with open('image_catalog.csv', 'r') as f:
    reader = csv.DictReader(f)
    images = list(reader)

for image in images:
    if image['upgraded'] == 'false':
        # 1. Build enhanced prompt
        enhanced_prompt = f"""Professional documentary photography, f/11 aperture,
deep depth of field with everything in sharp focus.
{image['description']}
Studio-quality lighting, cinematic composition,
photojournalistic authenticity. No text overlays."""

        # 2. Determine aspect ratio from dimensions
        dims = image['dimensions']
        aspect_map = {
            '1024x1024': '1:1',
            '330x330': '1:1',
            '330x242': '4:3',
            '510x187': '21:9',
            '200x200': '1:1',
            '400x400': '1:1'
        }
        aspect = aspect_map.get(dims, '1:1')

        # 3. Call mcp__nanobanana__generate_image
        # (via Claude Code MCP invocation)

        # 4. After success, mark as upgraded
        image['upgraded'] = 'true'
```

---

## Quality Checklist

Before marking an image as `upgraded = true`, verify:

- [ ] Image has deep depth of field (everything in focus)
- [ ] Professional lighting with no harsh shadows
- [ ] No text, captions, or overlays visible
- [ ] Matches documentary/photojournalistic style
- [ ] Resolution matches or exceeds original
- [ ] WebP format for web use
- [ ] Entry added to `new_image_catalog.csv`

---

## new_image_catalog.csv Format

The destination catalog should include these columns:

```csv
path,type,dimensions,date_modified,model,style,description,original_path,file_size_bytes
```

| Column | Description |
|--------|-------------|
| `path` | New image file path |
| `type` | File extension (.webp, .png) |
| `dimensions` | Width x Height |
| `date_modified` | Generation timestamp |
| `model` | Always `gemini-3-pro-image-preview` |
| `style` | `professional-documentary` or `iphone-snapshot-f11` |
| `description` | Enhanced prompt used |
| `original_path` | Path from image_catalog.csv |
| `file_size_bytes` | File size in bytes |

---

## Example Upgrade

### Original Entry (image_catalog.csv)

```csv
path,type,dimensions,date_modified,model,description,upgraded
images/articles/yoga-morning-flow.webp,.webp,1024x1024,2025-12-21,gemini-2.5-flash,"Woman in tree pose wearing athletic wear in bright minimalist studio with tall windows, plants, and macrame wall hanging.",false
```

### Enhanced Prompt

```
Professional documentary photography, f/11 aperture, deep depth of field
with everything in sharp focus. Woman in tree pose wearing athletic wear
in bright minimalist studio with tall windows, plants, and macrame wall
hanging. Studio-quality lighting, cinematic composition, photojournalistic
authenticity. No text overlays.
```

### MCP Call

```json
{
  "prompt": "Professional documentary photography, f/11 aperture, deep depth of field with everything in sharp focus. Woman in tree pose wearing athletic wear in bright minimalist studio with tall windows, plants, and macrame wall hanging. Studio-quality lighting, cinematic composition, photojournalistic authenticity. No text overlays.",
  "model_tier": "pro",
  "resolution": "high",
  "aspect_ratio": "1:1",
  "thinking_level": "high",
  "enable_grounding": true,
  "negative_prompt": "text overlays, captions, blurry, shallow depth of field, bokeh, amateur lighting"
}
```

### New Entry (new_image_catalog.csv)

```csv
images/articles/yoga-morning-flow-upgraded.webp,.webp,1024x1024,2025-12-24,gemini-3-pro-image-preview,professional-documentary,"Professional documentary photography...",images/articles/yoga-morning-flow.webp,185028
```

### Updated Original Entry

```csv
images/articles/yoga-morning-flow.webp,.webp,1024x1024,2025-12-21,gemini-2.5-flash,"Woman in tree pose...",true
```

---

## Progress Tracking

Track upgrade progress by counting:

```bash
# Total images to upgrade
grep -c "false" image_catalog.csv

# Completed upgrades
grep -c "true" image_catalog.csv

# Percentage complete
awk -F',' '{if($7=="true") a++; else if($7=="false") b++} END {print a/(a+b)*100 "%"}' image_catalog.csv
```

---

## File References (Important for Claude)

When using Gemini or Codex MCP tools, **never copy/paste file contents** into the prompt. Instead, reference files by path:

### Gemini MCP
Use `@filepath` syntax:
```
prompt: "@/mnt/d/silk/silklife/image_upgrade/image_catalog.csv - process row 5"
```

### Codex MCP
Point to the file path:
```
prompt: "Audit the file at /mnt/d/silk/silklife/image_upgrade/INSTRUCTIONS.md for clarity"
```

**Why:**
- Avoids token bloat from pasting large files
- MCP tools can read files directly
- More efficient and accurate

---

## Notes

- **Model tier:** Always use `"pro"` for highest quality output
- **Resolution:** Use `"high"` (1024px) for all images - this is 3x larger than most thumbnails
- **No masters needed:** Prompts are saved in catalog; regenerate or upscale on demand
- **F-stop:** F/11 or higher ensures everything is in sharp focus (deep DoF)
- **Processing time:** Pro model with high thinking takes 15-30 seconds per image
- **Output location:** Nanobanana saves to its configured output directory
- **Future upscaling:** If larger sizes needed later, use generative upscale (Real-ESRGAN, Topaz, etc.)

---

*Last updated: 2025-12-24*
