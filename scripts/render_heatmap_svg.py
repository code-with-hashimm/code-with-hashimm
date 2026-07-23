import json
import os
import sys

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run fetch_contributions.py first!")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)

    # Grid layout calculations (53 columns x 7 rows)
    box_size = 11
    gap = 4
    stride = box_size + gap
    padding_x = 25
    padding_y = 50

    width = 860
    height = 210

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <style>',
        '    .bg { fill: #0d1117; stroke: #30363d; stroke-width: 1px; }',
        '    .header-text { font-family: "Fira Code", Monaco, Consolas, monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }',
        '    .sub-text { font-family: "Fira Code", Monaco, Consolas, monospace; font-size: 11px; fill: #8b949e; }',
        '    .legend-text { font-family: "Fira Code", Monaco, Consolas, monospace; font-size: 10px; fill: #8b949e; }',
        '    @keyframes slideDown {',
        '      from { transform: translateY(-12px); opacity: 0; }',
        '      to { transform: translateY(0); opacity: 1; }',
        '    }',
        '    .box { animation: slideDown 0.4s ease-out forwards; opacity: 0; }',
        '  </style>',
        f'  <rect width="{width}" height="{height}" class="bg" rx="10"/>',
        f'  <text x="{padding_x}" y="30" class="header-text">GitHub Contribution Matrix ({data.get("username")})</text>',
        f'  <text x="{width - padding_x - 180}" y="30" class="sub-text">{total:,} contributions in last year</text>',
        f'  <g transform="translate({padding_x}, {padding_y})">'
    ]

    # Render day boxes
    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        x = col * stride
        y = row * stride

        level = min(day.get("level", 0), len(PALETTE) - 1)
        color = PALETTE[level]

        # Stagger delay diagonally across the grid
        delay = round((col * 0.012) + (row * 0.015), 3)

        svg.append(
            f'    <rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}">'
            f'<animate attributeName="opacity" to="1" dur="0.3s" begin="{delay}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0,-10" to="0,0" dur="0.3s" begin="{delay}s" fill="freeze"/>'
            f'</rect>'
        )

    svg.append('  </g>')

    # Footer stats & Legend
    footer_y = height - 20
    svg.append(f'  <text x="{padding_x}" y="{footer_y}" class="sub-text">Current Streak: {current_streak} days  |  Longest Streak: {longest_streak} days</text>')

    # Render "Less -> More" palette legend
    legend_start_x = width - padding_x - 140
    svg.append(f'  <text x="{legend_start_x - 30}" y="{footer_y}" class="legend-text">Less</text>')
    for i, p_color in enumerate(PALETTE):
        lx = legend_start_x + (i * 14)
        ly = footer_y - 9
        svg.append(f'  <rect x="{lx}" y="{ly}" width="10" height="10" rx="2" fill="{p_color}"/>')
    svg.append(f'  <text x="{legend_start_x + (len(PALETTE) * 14) + 5}" y="{footer_y}" class="legend-text">More</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Success! Generated animated contribution heatmap at {output_path}")

if __name__ == "__main__":
    render_heatmap()
