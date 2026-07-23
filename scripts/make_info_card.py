import os

def generate_info_card(output_path="info-card.svg"):
    # Toggle static mode using environment variable (STATIC=1 python scripts/make_info_card.py)
    is_static = os.environ.get("STATIC") == "1"

    # Define sections matching the author's structure
    card_title = "hashim@github: ~$ neofetch"
    
    bio_section = [
        ("Now", "Full-Stack Web Developer", "#ffa657"),
        ("Prev", "Frontend & UI/UX Specialist", "#ffa657"),
        ("Also", "Building CampusKey Platform", "#ffa657"),
        ("Edu", "Computer Science Student", "#ffa657"),
    ]

    stack_section = [
        ("Frontend", "React, Next.js, TypeScript, Tailwind CSS", "#ffa657"),
        ("Backend", "Node.js, Express, Python, Supabase", "#ffa657"),
        ("AI / ML", "Vercel AI SDK, LangChain, Local LLMs", "#ffa657"),
        ("Tools", "Git, Docker, Vercel, Cursor IDE", "#ffa657"),
    ]

    highlights = [
        "Building student-focused web apps & tools",
        "Focused on AI integration & modern UX"
    ]

    width = 480
    height = 376

    # CSS styles converting SMIL to GitHub-safe keyframes
    css = """
    .card-bg { fill: url(#ibg); }
    .border-line { fill: none; stroke: #30363d; }
    .header-line { stroke: #30363d; }
    .divider { stroke: #30363d; stroke-opacity: 0.8; }
    .title-text { fill: #7d8590; font-size: 12px; text-anchor: middle; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    .header-user { font-size: 14px; font-weight: 700; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    .section-title { fill: #58a6ff; font-size: 12.5px; font-weight: 700; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    .key-title { font-size: 12.5px; font-weight: 700; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    .val-text { fill: #c9d1d9; font-size: 12.5px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    """

    if not is_static:
        css += """
        @keyframes fadeSlide {
          0% { opacity: 0; transform: translateY(5px); }
          100% { opacity: 1; transform: translateY(0px); }
        }
        .anim-group {
          opacity: 0;
          animation: fadeSlide 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }
        """

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '  <defs>',
        '    <linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">',
        '      <stop offset="0" stop-color="#111722"/>',
        '      <stop offset="1" stop-color="#0d1117"/>',
        '    </linearGradient>',
        '  </defs>',
        '  <style>',
        css,
        '  </style>',
        f'  <rect width="{width}" height="{height}" rx="12" class="card-bg"/>',
        f'  <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="12" class="border-line"/>',
        f'  <line x1="0" y1="30" x2="{width}" y2="30" class="header-line"/>',
        '  <circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>',
        '  <circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>',
        '  <circle cx="52" cy="15.0" r="5" fill="#27c93f"/>',
        f'  <text x="{width/2}" y="19.0" class="title-text">{card_title}</text>'
    ]

    # Group animations tracker
    anim_idx = 0

    def get_group_tag():
        nonlocal anim_idx
        if is_static:
            return '  <g>'
        else:
            delay = round(0.15 + (anim_idx * 0.06), 2)
            anim_idx += 1
            return f'  <g class="anim-group" style="animation-delay: {delay}s;">'

    # Header Row
    svg.append(get_group_tag())
    svg.append('    <text x="20" y="60.0" class="header-user"><tspan fill="#3fb950">hashim</tspan><tspan fill="#7d8590">@</tspan><tspan fill="#22d3ee">github</tspan></text>')
    svg.append('    <line x1="140" y1="56.0" x2="460" y2="56.0" class="divider"/>')
    svg.append('  </g>')

    # Bio Section
    y_positions = [80.5, 101.0, 121.5, 142.0]
    for i, (key, val, color) in enumerate(bio_section):
        y = y_positions[i]
        svg.append(get_group_tag())
        svg.append(f'    <text x="20" y="{y}" fill="{color}" class="key-title">{key}</text>')
        svg.append(f'    <text x="112" y="{y}" class="val-text">{val}</text>')
        svg.append('  </g>')

    # Stack Header
    svg.append(get_group_tag())
    svg.append('    <text x="20" y="172.8" class="section-title">&#8212; Stack</text>')
    svg.append('    <line x1="85" y1="168.8" x2="460" y2="168.8" class="divider"/>')
    svg.append('  </g>')

    # Stack Items
    stack_y = [193.2, 213.8, 234.2, 254.8]
    for i, (key, val, color) in enumerate(stack_section):
        y = stack_y[i]
        svg.append(get_group_tag())
        svg.append(f'    <text x="20" y="{y}" fill="{color}" class="key-title">{key}</text>')
        svg.append(f'    <text x="112" y="{y}" class="val-text">{val}</text>')
        svg.append('  </g>')

    # Highlights Header
    svg.append(get_group_tag())
    svg.append('    <text x="20" y="285.5" class="section-title">&#8212; Highlights</text>')
    svg.append('    <line x1="112" y1="281.5" x2="460" y2="281.5" class="divider"/>')
    svg.append('  </g>')

    # Highlights Items
    hl_y = [302.0, 322.5]
    for i, text in enumerate(highlights):
        cy = hl_y[i]
        ty = cy + 4.0
        svg.append(get_group_tag())
        svg.append(f'    <circle cx="23" cy="{cy}" r="2.5" fill="#3fb950"/>')
        svg.append(f'    <text x="34" y="{ty}" class="val-text">{text}</text>')
        svg.append('  </g>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Success! Rebuilt exact info card design at {output_path}")

if __name__ == "__main__":
    generate_info_card("info-card.svg")
