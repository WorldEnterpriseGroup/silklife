# Banner Ad Creation Instructions

## Overview

Banner ads in SILK Life articles use a **21:9 ultra-wide aspect ratio** with a specific composition: the **top half is empty or contains a subtle gradient**, while the **ad content appears only in the bottom half**. This allows the banner to integrate naturally into article content without feeling intrusive.

---

## Tool & Settings

**MCP Tool:** `mcp__nanobanana__generate_image`

| Parameter | Value | Notes |
|-----------|-------|-------|
| `aspect_ratio` | `"21:9"` | Ultra-wide banner format |
| `model_tier` | `"pro"` | Best quality |
| `resolution` | `"high"` | Crisp output |

---

## Prompt Structure

### Main Prompt Template

```
[Scene description for BOTTOM HALF ONLY]. The top half of the image is completely empty - either solid color, subtle gradient, or soft blur with no objects, text, or focal points. All visual content, subjects, and points of interest are positioned in the bottom half of the frame. Documentary photography style, natural lighting.
```

### Example Prompts

**Yoga Banner:**
```
Woman doing peaceful yoga stretch on woven rug in Victorian parlor with morning light, radiator visible. The top half of the image is completely empty - soft gradient fading to cream/white with no objects or text. All visual content is positioned in the bottom half of the frame. Documentary photography style, natural lighting, cozy intimate atmosphere.
```

**Cafe Banner:**
```
Steaming coffee cup and fresh pastry on rustic wooden table in cozy cafe setting. The top half of the image is completely empty - warm gradient fading to soft cream. All visual content is positioned in the bottom half only. Documentary style, warm natural lighting.
```

**Homes Banner:**
```
Cozy Victorian cottage interior with worn hardwood floors, plants, and soft morning light through tall windows. The top half of the image is completely empty - soft white/cream gradient. All content in bottom half. Documentary photography, authentic lived-in feel.
```

---

## Negative Prompt

Always include this negative prompt to reinforce the composition:

```
text, words, logos, watermarks, anything in top half, objects in upper portion, heads or faces in top half, cluttered top, busy upper area, text overlays
```

---

## File Organization

### Location
Banner ads for enhanced articles go in the article's media folder:
```
articles/[slug]/media/banner.webp
```

For legacy articles or shared banners:
```
images/ads/banner/[article-slug]-banner.webp
```

### Naming Convention
- `yoga-morning-flow-banner.webp`
- `cafe-farm-table-banner.webp`
- `homes-sustainable-living-banner.webp`

---

## Complete Example

```python
# Using nanobanana MCP tool
mcp__nanobanana__generate_image(
    prompt="Woman in peaceful yoga pose on woven rug in Victorian parlor, morning light through tall windows, cast iron radiator. The top half of the image is completely empty - soft cream/white gradient with absolutely nothing. All visual content positioned in bottom half only. Documentary photography, natural lighting, authentic moment.",
    aspect_ratio="21:9",
    model_tier="pro",
    resolution="high",
    negative_prompt="text, logos, watermarks, anything in top half, objects in upper portion, heads in top half, busy upper area, cluttered top"
)
```

---

## Post-Processing

1. **Convert to WebP** (if PNG output):
   ```bash
   cwebp -q 90 banner.png -o banner.webp
   ```

2. **Verify dimensions** - should be ultra-wide (e.g., 2016x864 or similar 21:9)

3. **Check composition** - top half should be empty, content in bottom half

---

## HTML Integration

```html
<!-- BANNER AD inside article content -->
<div class="article-inline-ad banner-style" style="text-align: center; margin: 30px 0;">
    <a href="https://silkyoga.org" target="_blank" rel="noopener" style="display: block;">
        <img src="media/banner.webp" alt="SILK Yoga" style="max-width: 100%; height: auto; border-radius: 6px;">
    </a>
    <p style="font-size: 11px; color: #A0AEC0; margin-top: 8px;">Advertisement</p>
</div>
```

---

## Why This Composition?

1. **Non-intrusive** - Empty top half feels like breathing room in the article
2. **Text overlay friendly** - Top area can have CSS text overlays if needed
3. **Mobile friendly** - Content stays visible even when cropped
4. **Professional look** - Avoids cluttered, aggressive ad aesthetics
