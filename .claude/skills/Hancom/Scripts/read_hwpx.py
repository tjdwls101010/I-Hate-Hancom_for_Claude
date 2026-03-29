#!/usr/bin/env python3
"""Convert HWPX files to human-readable structured text.

Usage:  python3 read_hwpx.py input.hwpx [--format markdown|text] [--verbose]
"""
import argparse, re, sys, zipfile, xml.etree.ElementTree as ET
from pathlib import Path

NS = {
    "hh": "http://www.hancom.co.kr/hwpml/2011/head",
    "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    "hs": "http://www.hancom.co.kr/hwpml/2011/section",
    "hc": "http://www.hancom.co.kr/hwpml/2011/core",
}
ALIGN_KO = {"JUSTIFY": "양쪽정렬", "CENTER": "가운데", "LEFT": "왼쪽", "RIGHT": "오른쪽"}

# ── ZIP helpers ──────────────────────────────────────────────────────────────

def _entry(zf, suffix):
    """Find first ZIP entry ending with *suffix*."""
    return next((n for n in zf.namelist() if n.endswith(suffix)), None)

def _sections(zf):
    """Return sorted list of section XML paths inside the ZIP."""
    pat = re.compile(r"section\d+\.xml$", re.I)
    return sorted(n for n in zf.namelist() if pat.search(n))

# ── Header parsing ───────────────────────────────────────────────────────────

def _parse_fonts(root):
    fonts = {}
    for ff in root.findall(".//hh:fontface", NS):
        lang = ff.get("lang", "").upper()
        for f in ff.findall("hh:font", NS):
            fid = f.get("id")
            if fid is not None:
                fonts[(lang, fid)] = f.get("face", "?")
    return fonts

def _parse_char_pr(root, fonts):
    table = {}
    for cp in root.findall(".//hh:charPr", NS):
        cid = cp.get("id")
        if cid is None:
            continue
        pt = int(cp.get("height", "0")) / 100
        pt_s = f"{int(pt)}pt" if pt == int(pt) else f"{pt:.1f}pt"
        mods = []
        if cp.find("hh:bold", NS) is not None:
            mods.append("bold")
        if cp.find("hh:italic", NS) is not None:
            mods.append("italic")
        color = cp.get("textColor", "#000000")
        if color and color.upper() not in ("#000000", "NONE", "#00000000"):
            mods.append(color)
        face = "?"
        fref = cp.find("hh:fontRef", NS)
        if fref is not None:
            face = fonts.get(("HANGUL", fref.get("hangul", "0")), "?")
        mod_s = (" " + " ".join(mods)) if mods else ""
        table[cid] = f"{pt_s} {face}{mod_s}"
    return table

def _parse_para_pr(root):
    table = {}
    for pp in root.findall(".//hh:paraPr", NS):
        pid = pp.get("id")
        if pid is None:
            continue
        al = pp.find("hh:align", NS)
        horiz = al.get("horizontal", "JUSTIFY") if al is not None else "JUSTIFY"
        ls = pp.find("hh:lineSpacing", NS)
        if ls is not None:
            sp = f"{ls.get('value','160')}%" if ls.get("type") == "PERCENT" else ls.get("value","160")
        else:
            sp = "160%"
        parts = [ALIGN_KO.get(horiz, horiz), sp]
        mg = pp.find("hh:margin", NS)
        if mg is not None:
            indent = mg.find("hc:intent", NS)
            left = mg.find("hc:left", NS)
            if indent is not None and indent.get("value", "0") != "0":
                parts.append(f"들여쓰기{indent.get('value')}")
            if left is not None and left.get("value", "0") != "0":
                parts.append(f"왼쪽{left.get('value')}")
        table[pid] = " ".join(parts)
    return table

def _parse_borderfill(root):
    table = {}
    for bf in root.findall(".//hh:borderFill", NS):
        bid = bf.get("id")
        if bid is None:
            continue
        parts = []
        border = bf.find("hh:border", NS)
        if border is not None:
            lb = border.find("hh:left", NS)
            if lb is not None:
                bt = lb.get("type", "NONE")
                if bt != "NONE":
                    w = lb.get("width", "")
                    parts.append(f"실선 {w}" if bt == "SOLID" else bt)
        brush = bf.find(".//hh:windowBrush", NS)
        if brush is not None:
            fc = brush.get("faceColor", "none")
            if fc and fc.lower() not in ("none", "#00000000"):
                parts.append(f"배경 {fc}")
        table[bid] = ", ".join(parts) if parts else "없음"
    return table

def parse_header(zf):
    path = _entry(zf, "header.xml")
    if not path:
        return {}, {}, {}, {}
    with zf.open(path) as f:
        root = ET.parse(f).getroot()
    fonts = _parse_fonts(root)
    return _parse_char_pr(root, fonts), _parse_para_pr(root), _parse_borderfill(root), fonts

# ── Section content extraction ───────────────────────────────────────────────

def _tag(el):
    """Return local tag name without namespace."""
    t = el.tag
    return t.split("}")[-1] if "}" in t else t

def _text_from_p(p):
    """Concatenate all <hp:t> text in a paragraph."""
    return "".join(t.text for run in p.findall(".//hp:run", NS)
                   for t in run.findall("hp:t", NS) if t.text)

def _char_ids(p):
    """Unique charPrIDRef values from runs that carry text."""
    seen, ids = set(), []
    for run in p.findall(".//hp:run", NS):
        if any(t.text for t in run.findall("hp:t", NS)):
            cid = run.get("charPrIDRef")
            if cid and cid not in seen:
                seen.add(cid); ids.append(cid)
    return ids

def _cell_text(tc):
    parts = []
    for sub in tc.findall(".//hp:subList", NS):
        for p in sub.findall("hp:p", NS):
            t = _text_from_p(p)
            if t:
                parts.append(t)
    return " ".join(parts)

def _render_table(tbl):
    """Return list of markdown-table lines."""
    rows = []
    for tr in tbl.findall("hp:tr", NS):
        rows.append([_cell_text(tc) for tc in tr.findall("hp:tc", NS)])
    if not rows:
        return []
    ncols = max(len(r) for r in rows)
    for r in rows:
        r.extend([""] * (ncols - len(r)))
    widths = [max(max((len(r[c]) for r in rows), default=0), 2) for c in range(ncols)]
    lines = []
    for i, row in enumerate(rows):
        line = "|" + "|".join(f" {v:<{widths[c]}} " for c, v in enumerate(row)) + "|"
        lines.append(line)
        if i == 0:
            lines.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    return lines

def _find_images(p):
    imgs = []
    for tag_name in ("hp:img", "hp:pic"):
        for el in p.findall(f".//{tag_name}", NS):
            ref = el.get("binaryItemIDRef", "")
            if ref and ref not in imgs:
                imgs.append(ref)
    for run in p.findall(".//hp:run", NS):
        for child in run:
            if _tag(child) in ("img", "pic"):
                ref = child.get("binaryItemIDRef", "")
                if ref and ref not in imgs:
                    imgs.append(ref)
    return imgs

def process_section(zf, sec_path, char_pr, para_pr, verbose):
    with zf.open(sec_path) as f:
        root = ET.parse(f).getroot()
    lines, stats = [], {"paragraphs": 0, "tables": 0, "images": 0}

    body = root.find(".//hs:sec", NS)
    if body is None:
        body = root

    for child in body:
        if _tag(child) != "p":
            continue
        stats["paragraphs"] += 1

        # Images
        imgs = _find_images(child)
        for im in imgs:
            stats["images"] += 1
            lines.append(f"[Image: {im}]")

        # Tables
        tables = child.findall(".//hp:tbl", NS)
        if tables:
            for tbl in tables:
                stats["tables"] += 1
                lines.append("")
                lines.extend(_render_table(tbl))
                lines.append("")
            continue

        # Text
        text = _text_from_p(child)
        if not text.strip():
            lines.append("")
            continue

        line = text
        if verbose:
            pid = child.get("paraPrIDRef", "")
            cids = _char_ids(child)
            ann = []
            if cids:
                ann.append(", ".join(char_pr.get(c, f"charPr#{c}") for c in cids))
            if pid:
                ann.append(para_pr.get(pid, f"paraPr#{pid}"))
            if ann:
                line += f"  \u2190 [{'; '.join(ann)}]"
        lines.append(line)

    return lines, stats

# ── Main output ──────────────────────────────────────────────────────────────

def read_hwpx(filepath, fmt="markdown", verbose=False):
    """Read an HWPX file and return structured text."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: file not found: {filepath}", file=sys.stderr); sys.exit(1)
    if not zipfile.is_zipfile(path):
        print(f"Error: not a valid ZIP/HWPX file: {filepath}", file=sys.stderr); sys.exit(1)

    with zipfile.ZipFile(path, "r") as zf:
        char_pr, para_pr, border_fill, fonts = parse_header(zf)
        secs = _sections(zf)
        if not secs:
            print("Error: no section files found in HWPX", file=sys.stderr); sys.exit(1)

        all_lines, total = [], {"paragraphs": 0, "tables": 0, "images": 0}
        for idx, sp in enumerate(secs):
            sec_lines, st = process_section(zf, sp, char_pr, para_pr, verbose)
            for k in total:
                total[k] += st[k]
            if len(secs) > 1 or fmt == "markdown":
                all_lines.append(f"\n## Section {idx + 1}\n")
            all_lines.extend(sec_lines)

    # Build header
    out = []
    if fmt == "markdown":
        out.append("# Document Summary")
        out.append(f"- File: {path.name}")
        for k in ("Sections", "Paragraphs", "Tables", "Images"):
            v = len(secs) if k == "Sections" else total[k.lower()]
            out.append(f"- {k}: {v}")
    else:
        out.append(f"=== {path.name} ===")
        out.append(f"Sections: {len(secs)}  Paragraphs: {total['paragraphs']}  "
                    f"Tables: {total['tables']}  Images: {total['images']}")
        out.append("")
    out.extend(all_lines)

    # Collapse 3+ consecutive blank lines into 2
    cleaned, blanks = [], 0
    for ln in out:
        if not ln.strip():
            blanks += 1
            if blanks <= 2:
                cleaned.append("")
        else:
            blanks = 0
            cleaned.append(ln)
    return "\n".join(cleaned)


def main():
    ap = argparse.ArgumentParser(description="Convert HWPX to readable text.")
    ap.add_argument("input", help="Path to .hwpx file")
    ap.add_argument("--format", choices=["markdown", "text"], default="markdown",
                    help="Output format (default: markdown)")
    ap.add_argument("--verbose", action="store_true",
                    help="Include style annotations after each line")
    args = ap.parse_args()
    print(read_hwpx(args.input, fmt=args.format, verbose=args.verbose))

if __name__ == "__main__":
    main()
