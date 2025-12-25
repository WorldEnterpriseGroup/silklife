# Banner Ad Creation Instructions

## Overview

Banner ads for SILK Life articles are **wide promotional banners** with:
1. A unique scene for EACH article (variety matters - eyes like fresh visuals)
2. **Text integrated INTO the image** - not a separate overlay band
3. Final aspect ratio of **21:9** (wide cinematic format)
4. **AVIF format** for optimal compression (~65% smaller than WebP)

**CRITICAL:** Every article needs its OWN unique banner. Do NOT reuse generic property banners across multiple articles.

---

## Workflow

### Step 1: Generate Banner with Integrated Text

**MCP Tool:** `mcp__nanobanana__generate_image`

| Parameter | Value | Notes |
|-----------|-------|-------|
| `aspect_ratio` | `"21:9"` | Wide cinematic format |
| `model_tier` | `"pro"` | Best quality for text rendering |
| `resolution` | `"high"` | Crisp output |

Nanobanana can generate images WITH text thoughtfully integrated into the design. Include the text in your prompt and let the AI compose it beautifully.

### Step 2: Convert to AVIF

```bash
convert ~/nanobanana-images/[input].png -quality 50 /mnt/d/silk/silklife/images/ads/banner/[article-slug]-banner.avif
```

That's it. No cropping, no overlay bands, no ImageMagick text annotation.

---

## Prompt Structure

### Key Principles

1. **Describe the text you want** - Include exact wording in the prompt
2. **Specify text placement** - "text in lower third", "elegant typography centered", etc.
3. **Match the article theme** - Banner should relate to the specific article content
4. **Scene spans full width** - No empty corners or unbalanced compositions

### Prompt Template

```
Wide cinematic banner for [ARTICLE TOPIC]. [Scene description spanning full width].
Elegant typography reading "[BRAND NAME]" with tagline "[TAGLINE]" integrated naturally
into the composition - [placement details like "in the lower portion with subtle shadow
for readability" or "overlaid on a darker area of the image"].
Documentary photography style, natural lighting, professional advertising quality.
```

### Example Prompts

**For a pottery article:**
```
Wide cinematic banner for a pottery studio article. Warm scene of clay pottery wheels,
ceramic vessels, and artist's hands working clay, spanning the full frame from left to right.
Elegant serif typography reading "SILK Arts" with tagline "Shape Your Story" integrated
into the lower right portion where the background is darker, with subtle text shadow for
readability. Documentary photography style, warm kiln lighting, professional advertising quality.
```

**For a yoga article:**
```
Wide cinematic banner for a morning yoga practice article. Peaceful Victorian parlor with
yoga mat, morning light streaming through tall windows, plants on windowsills, spanning
full width. Elegant typography reading "SILK Yoga" with tagline "Find Your Flow" placed
in the brighter left portion with soft drop shadow. Documentary photography style,
golden hour lighting, professional advertising quality.
```

**For a cafe article:**
```
Wide cinematic banner for a farm-to-table dining article. Rustic wooden table with
fresh vegetables, artisan bread, steaming coffee cups, herbs in terracotta pots,
spanning full frame. Elegant typography reading "SILK Cafe" with tagline "Gather Around
Good Food" integrated into a darker area of the composition. Documentary photography style,
warm morning light, professional advertising quality.
```

---

## Text Integration Tips

### Good Text Placement
- **On darker areas** - Text naturally readable without heavy effects
- **Lower third** - Classic advertising placement
- **Negative space** - Let the AI find natural areas for text
- **With subtle shadow** - Helps legibility on varied backgrounds

### Typography Guidance in Prompts
- "Elegant serif typography" - Classic, refined look
- "Clean sans-serif text" - Modern, minimal
- "Handwritten script" - Warm, personal feel
- "Bold display type" - Strong, attention-grabbing

### What NOT to Do
- Don't add text as a separate band/bar above the image
- Don't use ImageMagick to overlay text after generation
- Don't reuse the same banner across multiple articles
- Don't let text float on busy, unreadable backgrounds

---

## File Organization

### Location
```
images/ads/banner/[article-slug]-banner.avif
```

### Naming Convention
| Article | Banner File |
|---------|-------------|
| `post-yoga-beginners.html` | `yoga-beginners-banner.avif` |
| `post-cafe-farm-table.html` | `cafe-farm-table-banner.avif` |
| `post-arts-darkroom-quiet.html` | `arts-darkroom-quiet-banner.avif` |
| `articles/sculpting-dreams/` | `sculpting-dreams-banner.avif` |

### Shared Property Banners (Fallback Only)
These exist for cross-promotion but should NOT be the primary banner in articles:
```
images/ads/shared/silk-[property]-banner.avif
```

---

## Complete Workflow Example

```bash
# 1. Generate with nanobanana MCP tool
# Prompt: "Wide cinematic banner for a darkroom photography article.
# Red safelight illuminating film developing trays, hands pulling a print
# from developer, vintage equipment spanning full width. Elegant typography
# reading 'SILK Arts' with tagline 'Develop Your Vision' in the lower left
# where shadows are deeper. Documentary photography style, moody red lighting."

# Parameters: aspect_ratio="21:9", model_tier="pro", resolution="high"

# 2. Convert to AVIF (that's it!)
convert ~/nanobanana-images/gen_XXXXXX.png \
  -quality 50 \
  /mnt/d/silk/silklife/images/ads/banner/arts-darkroom-quiet-banner.avif

# 3. Verify
ls -lh /mnt/d/silk/silklife/images/ads/banner/arts-darkroom-quiet-banner.avif
identify /mnt/d/silk/silklife/images/ads/banner/arts-darkroom-quiet-banner.avif
# Should be ~60-100 KB, 21:9 aspect ratio
```

---

## HTML Integration

```html
<!-- ARTICLE-SPECIFIC BANNER AD -->
<div class="header-banner-ad" style="text-align: center; margin: 20px 0;">
    <a href="https://silkarts.org" target="_blank" rel="noopener" style="display: block;">
        <img src="images/ads/banner/arts-darkroom-quiet-banner.avif"
             alt="SILK Arts - Develop Your Vision"
             style="max-width: 100%; height: auto; border-radius: 8px;">
    </a>
    <p style="font-size: 10px; color: #A0AEC0; margin-top: 6px;">Advertisement</p>
</div>
```

---

## Quality Checklist

Before deploying a banner, verify:

- [ ] **Unique to the article** - Not a generic reused banner
- [ ] Scene spans FULL WIDTH (no empty left/right areas)
- [ ] Text is integrated INTO the image (not overlaid as a band)
- [ ] Text is readable against its background
- [ ] **AVIF format** (not WebP or PNG)
- [ ] File size 60-100 KB (AVIF q50)
- [ ] Aspect ratio is 21:9 (wide cinematic)

---

## Why This Approach?

### Variety Matters
- Eyes get bored seeing the same banner repeatedly
- Unique banners feel curated and intentional
- Each article deserves its own visual identity

### Integrated Text > Overlay Bands
- Looks more professional and designed
- AI can compose text placement thoughtfully
- No ugly cream bars covering the image
- Better visual hierarchy

### Why AVIF?

| Format | Typical Size | Browser Support (2025) |
|--------|--------------|------------------------|
| WebP | 150-200 KB | 95.3% |
| **AVIF** | **60-100 KB** | **93.8%** |

AVIF provides ~65% smaller files than WebP at equivalent quality.
