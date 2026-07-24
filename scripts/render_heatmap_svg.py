import json
import os
import sys
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def render_heatmap(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run fetch_contributions.py first!")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total", 0)

    if not days:
        print("No days data found in JSON.")
        return

    box_size = 10
    gap = 3
    stride = box_size + gap
    
    offset_x = 35
    offset_y = 35

    width = 780
    height = 180

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <style>',
        '    .bg { fill: #0d1117; stroke: #30363d; stroke-width: 1px; }',
        '    .axis-text { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 10px; fill: #7d8590; }',
        '    .footer-text { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; fill: #f0f6fc; font-weight: bold; }',
        '    @keyframes slideDown {',
        '      from { transform: translateY(-8px); opacity: 0; }',
        '      to { transform: translateY(0); opacity: 1; }',
        '    }',
        '    .box { animation: slideDown 0.3s ease-out forwards; opacity: 0; }',
        '  </style>',
        f'  <rect width="{width}" height="{height}" class="bg" rx="10"/>',
        f'  <g transform="translate({offset_x}, {offset_y})">'
    ]

    # Day labels on the left
    svg.append('    <text x="-25" y="22" class="axis-text">Mon</text>')
    svg.append('    <text x="-25" y="48" class="axis-text">Wed</text>')
    svg.append('    <text x="-25" y="74" class="axis-text">Fri</text>')

    # Group days by month string (e.g., '2025-08', '2025-09')
    month_groups = {}
    for day in days:
        dt = datetime.strptime(day["date"], "%Y-%m-%d")
        month_key = dt.strftime("%Y-%m")
        if month_key not in month_groups:
            month_groups[month_key] = []
        month_groups[month_key].append(day)

    current_col = 0

    # Render month by month sequentially
    for month_key, month_days in month_groups.items():
        dt_sample = datetime.strptime(month_days[0]["date"], "%Y-%m-%d")
        month_name = dt_sample.strftime("%b")
        
        # Place Month Label at the start column of the month
        if current_col < 52:
            x_pos = current_col * stride
            svg.append(f'    <text x="{x_pos}" y="-10" class="axis-text">{month_name}</text>')

        # Render days in 7-row columns for this month
        for i, day in enumerate(month_days):
            col_offset = i // 7
            row = i % 7
            
            col = current_col + col_offset
            if col >= 52:
                break

            x = col * stride
            y = row * stride

            level = min(day.get("level", 0), len(PALETTE) - 1)
            color = PALETTE[level]

            delay = round((col * 0.008) + (row * 0.01), 3)

            svg.append(
                f'    <rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}">'
                f'<animate attributeName="opacity" to="1" dur="0.2s" begin="{delay}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0,-6" to="0,0" dur="0.2s" begin="{delay}s" fill="freeze"/>'
                f'</rect>'
            )

        # Advance current column counter by the number of columns used by this month
        month_cols = (len(month_days) + 6) // 7
        current_col += month_cols

    svg.append('  </g>')

    # Footer total line
    footer_y = height - 20
    svg.append(f'  <text x="{offset_x}" y="{footer_y}" class="footer-text">{total:,} contributions in the last year</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Success! Generated month-grouped heatmap at {output_path}")

if __name__ == "__main__":
    render_heatmap()
