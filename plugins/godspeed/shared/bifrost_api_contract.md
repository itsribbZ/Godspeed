# BifrostPDF API Contract v1.0
<!-- Source of truth: ~/Desktop\YourProject\Tools\BifrostPDF\bifrost_pdf.py -->
<!-- Also available at: ~/Desktop\T1\your-project\your-project721\Tools\BifrostPDF\bifrost_pdf.py -->
<!-- Last verified: 2026-04-02 (confirmed all methods match bifrost_pdf.py source) -->

## Import
```python
import sys, os
# Resolve BifrostPDF path dynamically — check known locations in order
for bifrost_path in [
    os.path.expanduser(r"~\Desktop\YourProject\Tools\BifrostPDF"),
    os.path.expanduser(r"~\Desktop\T1\Tools\BifrostPDF"),
    os.path.join(os.getcwd(), "Tools", "BifrostPDF"),
]:
    if os.path.isdir(bifrost_path):
        sys.path.insert(0, bifrost_path)
        break
from bifrost_pdf import BifrostPDF, BifrostTheme as T
```

## Constructor
```python
pdf = BifrostPDF(
    title="Title",
    subtitle="Subtitle",
    output_path=r"C:\path\to\output.pdf",
    footer="Footer text"
)
```

## Core Methods (v2.0)

| Method | Signature | Notes |
|--------|-----------|-------|
| `title_page` | `(topics: List[str], context: dict)` | First page with color bars |
| `table_of_contents` | `(entries: List[Tuple[str, str]])` | Manual TOC |
| `section` | `(title: str, color=None)` | Major section header (cyan) |
| `subsection` | `(title: str, color=None)` | Subsection header (violet) |
| `body` | `(text: str, indent=0, color=None)` | Auto-wrapping paragraph |
| `body_dim` | `(text: str, indent=0)` | Dimmed body text |
| `bullet` | `(text: str, color=None, indent=0)` | Bullet point |
| `numbered` | `(number: int, text: str, color=None)` | Numbered item |
| `code` | `(lines: List[str], title=None, line_numbers=False)` | Code block (dark bg) |
| `gold_box` | `(title: str, lines: List[str])` | Gold callout |
| `cyan_box` | `(title: str, lines: List[str])` | Cyan callout |
| `magenta_box` | `(title: str, lines: List[str])` | Magenta callout |
| `green_box` | `(title: str, lines: List[str])` | Green callout |
| `red_box` | `(title: str, lines: List[str])` | Red callout |
| `table` | `(headers: List[str], rows: List[List[str]], col_widths=None)` | Styled table |
| `rating` | `(label_text: str, score: float, max_score=10.0)` | Rating bar |
| `status_badge` | `(text: str, status="info")` | Colored badge |
| `spider_chart` | `(labels: List[str], data_sets: List[List[float]])` | Radar chart |
| `bar_chart` | `(categories: List[str], data_sets: List[List[float]])` | Bar chart |
| `line_chart` | `(data_sets: List[List[Tuple[float, float]]])` | Line chart |
| `image` | `(img_path: str, width=None, height=None)` | Embed image |
| `divider` | `(color=None)` | Horizontal rule |
| `spacer` | `(amount=8)` | Vertical space |
| `page_break` | `()` | Force new page |
| `label` | `(text: str, color=None)` | Small label text |
| `gradient_bar` | `(x=None, width=None)` | Decorative gradient |
| `watermark` | `(text="DRAFT", opacity=0.08)` | Background watermark |
| `end_section` | `()` | End-of-document marker |
| `save` | `()` | Save PDF, print path+size |

## v3.0 Methods (Extended)

| Method | Signature | Notes |
|--------|-----------|-------|
| `code_highlighted` | `(lines: List[str], title=None, lang="cpp")` | Syntax-colored code |
| `dependency_graph` | `(nodes: List[Dict], edges: List[Tuple], title=None)` | Node-edge diagram |
| `heatmap_table` | `(headers: List[str], rows: List[List[Any]], thresholds=None)` | Color-coded metrics |
| `source_tier` | `(tier: int, source_text: str)` | Quality-tiered citation |
| `confidence_indicator` | `(label_text: str, level="high", detail=None)` | Confidence badge |
| `performance_budget` | `(budgets: List[Dict[str, Any]])` | Threshold-colored budget |
| `risk_matrix` | `(risks: List[Dict[str, Any]])` | Probability x Impact |
| `progress_dashboard` | `(items: List[Dict[str, Any]])` | Completion bars |
| `flow_diagram` | `(steps: List[Dict], title=None)` | Step flow chart |
| `color_tier_bar` | `(tiers: List[Dict])` | Colored tier bar |
| `quadrant_map` | `(quadrants: List[Dict], center_label="UCLAES")` | 4-quadrant map |
| `toc_entry` | `(level: int, title: str, label_key=None)` | Auto-TOC entry |
| `render_toc` | `(title="Table of Contents")` | Generate TOC with page numbers |
| `label` | `(key: str)` | Cross-reference anchor (v3.0 override) |
| `ref` | `(key: str) -> str` | Get cross-reference page |
| `ref_text` | `(text: str, key: str, color=None)` | Inline cross-reference |
| `bookmark` | `(key: str, title: str, level=0)` | PDF bookmark |
| `link_url` | `(text: str, url: str)` | External hyperlink |
| `link_bookmark` | `(text: str, bookmark_key: str)` | Internal link |

## DEPRECATED METHOD NAMES (DO NOT USE)

| Wrong Name | Correct Name |
|-----------|-------------|
| `code_block()` | `code()` |
| `callout()` | `gold_box()` / `cyan_box()` / etc. |
| `callout_box()` | `gold_box()` / `cyan_box()` / etc. |
| `add_section()` | `section()` |
| `add_text()` | `body()` |
| `add_code()` | `code()` |
| `add_table()` | `table()` |

## Quick Reference: Box Method Signatures
All box methods take the SAME signature: `(title: str, lines: List[str])`
- `lines` is a LIST of strings, not a single string
- Each string becomes one line in the box
