import os
import sys
from PIL import Image

RAMP = " .:-=+*cs#%@"  # Bright (sparse) -> Dark (dense)

def image_to_ascii_grid(image_path, width=100):
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found. Run prep_photo.py first!")
        sys.exit(1)

    img = Image.open(image_path).convert("L")
    aspect_ratio = img.height / img.width
    # Monospace font aspect ratio correction (~0.55 width-to-height ratio)
    height = int(width * aspect_ratio * 0.55)
    
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    
    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            pixel = img_resized.getpixel((x, y)) # 0 (black) -> 255 (white)
            # Invert: white background -> 0 (space), dark features -> dense char
            val = 255 - pixel 
            ramp_idx = int((val / 255) * (len(RAMP) - 1))
            line += RAMP[ramp_idx]
        lines.append(line)
    return lines

def build_svg(lines, output_path="avi-ascii.svg"):
    num_rows = len(lines)
    num_cols = len(lines[0]) if num_rows > 0 else 100
    
    # SVG Dimensions
    char_w, char_h = 7.2, 12
    padding = 20
    svg_width = int(num_cols * char_w + padding * 2)
    svg_height = int(num_rows * char_h + padding * 2)
    
    row_duration = 0.08  # Duration of wipe animation per row (seconds)
    stagger = 0.04       # Stagger start time between consecutive rows

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '  <style>',
        '    .bg { fill: #0d1117; }',
        '    .ascii { font-family: "Courier New", Courier, monospace; font-size: 11px; fill: #8b949e; white-space: pre; }',
        '  </style>',
        f'  <rect width="100%" height="100%" class="bg" rx="8"/>',
        '  <defs>'
    ]

    # Create SMIL clip-paths for staggered horizontal wiping line by line
    for i in range(num_rows):
        start_t = round(i * stagger, 2)
        svg_lines.append(f'    <clipPath id="clip-{i}">')
        svg_lines.append(f'      <rect x="0" y="0" width="0" height="{svg_height}">')
        svg_lines.append(f'        <animate attributeName="width" from="0" to="{svg_width}" dur="{row_duration}s" begin="{start_t}s" fill="freeze" />')
        svg_lines.append('      </rect>')
        svg_lines.append('    </clipPath>')
    
    svg_lines.append('  </defs>')
    svg_lines.append(f'  <g transform="translate({padding}, {padding})">')

    # Add text lines with individual clip-path animations
    for i, line in enumerate(lines):
        y_pos = int((i + 1) * char_h)
        # Escape XML characters
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_lines.append(f'    <text x="0" y="{y_pos}" class="ascii" clip-path="url(#clip-{i})">{escaped_line}</text>')

    svg_lines.append('  </g>')
    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Success! Generated self-typing ASCII portrait at {output_path}")

if __name__ == "__main__":
    ascii_grid = image_to_ascii_grid("source-prepped.png", width=95)
    build_svg(ascii_grid, "avi-ascii.svg")
