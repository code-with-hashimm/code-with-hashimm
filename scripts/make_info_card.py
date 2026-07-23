import os

def generate_info_card(output_path="info-card.svg"):
    # Profile details
    card_data = [
        ("OS", "Developer Workstation v2.6"),
        ("Host", "Next.js / React / Tailwind CSS"),
        ("Role", "Full-Stack Web Developer"),
        ("Stack", "TypeScript, Python, Supabase, Vercel"),
        ("Current", "Building CampusKey Platform"),
        ("Status", "Optimizing UI/UX & AI Workflows")
    ]

    width = 490
    height = 320
    line_height = 28
    start_y = 75

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <style>',
        '    .card-bg { fill: #0d1117; stroke: #30363d; stroke-width: 1px; }',
        '    .title-bar { fill: #161b22; }',
        '    .dot-red { fill: #ff5f56; }',
        '    .dot-yellow { fill: #ffbd2e; }',
        '    .dot-green { fill: #27c93f; }',
        '    .title-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 12px; fill: #8b949e; font-weight: 600; }',
        '    .key { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }',
        '    .value { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 13px; fill: #c9d1d9; }',
        '    .prompt { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 13px; fill: #79c0ff; font-weight: bold; }',
        '  </style>',
        f'  <rect width="{width}" height="{height}" class="card-bg" rx="10"/>',
        f'  <path d="M 0 10 Q 0 0 10 0 L {width-10} 0 Q {width} 0 {width} 10 L {width} 35 L 0 35 Z" class="title-bar"/>',
        '  <circle cx="20" cy="18" r="5" class="dot-red"/>',
        '  <circle cx="36" cy="18" r="5" class="dot-yellow"/>',
        '  <circle cx="52" cy="18" r="5" class="dot-green"/>',
        '  <text x="72" y="22" class="title-text">hashim@dev-box:~ (neofetch)</text>',
        '  <g transform="translate(25, 0)">'
    ]

    for i, (key, value) in enumerate(card_data):
        y_pos = start_y + (i * line_height)
        svg.append('    <g>')
        svg.append(f'      <text x="0" y="{y_pos}" class="prompt">&#10095;</text>')
        svg.append(f'      <text x="20" y="{y_pos}" class="key">{key}:</text>')
        svg.append(f'      <text x="110" y="{y_pos}" class="value">{value}</text>')
        svg.append('    </g>')

    svg.append('  </g>')
    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Success! Generated GitHub-safe info card at {output_path}")

if __name__ == "__main__":
    generate_info_card("info-card.svg")
