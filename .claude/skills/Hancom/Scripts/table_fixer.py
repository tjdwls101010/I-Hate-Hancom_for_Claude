#!/usr/bin/env python3
"""Fix table structure in HWPX section XML files.

Corrects rowCnt/colCnt, cellAddr, cellSpan, cellSz, cellMargin, and subList
issues that commonly arise when generating HWPX tables programmatically.

Usage:
    python3 table_fixer.py section0.xml [--output fixed_section0.xml]
    python3 table_fixer.py input.hwpx   [--output fixed.hwpx]
"""
from __future__ import annotations

import argparse, copy, re, sys, xml.etree.ElementTree as ET, zipfile
from io import BytesIO
from pathlib import Path

# -- Namespace setup ----------------------------------------------------------
NS = {
    "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    "hs": "http://www.hancom.co.kr/hwpml/2011/section",
    "hc": "http://www.hancom.co.kr/hwpml/2011/core",
    "hh": "http://www.hancom.co.kr/hwpml/2011/head",
    "hp10": "http://www.hancom.co.kr/hwpml/2016/paragraph",
    "hm": "http://www.hancom.co.kr/hwpml/2011/master-page",
    "hv": "http://www.hancom.co.kr/hwpml/2011/version",
    "ha": "http://www.hancom.co.kr/hwpml/2011/app",
    "hwpunitchar": "http://www.hancom.co.kr/hwpml/2016/HwpUnitChar",
    "opf": "http://www.idpf.org/2007/opf/",
    "ocf": "urn:oasis:names:tc:opendocument:xmlns:container",
    "odf": "urn:oasis:names:tc:opendocument:xmlns:manifest:1.0",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

def _t(local: str) -> str:
    """Clark-notation tag in the hp namespace."""
    return f"{{{NS['hp']}}}{local}"

TBL, GRIDCOL, GRIDCOLITEM = _t("tbl"), _t("gridCol"), _t("gridColItem")
TR, TC = _t("tr"), _t("tc")
CELLADDR, CELLSPAN, CELLSZ = _t("cellAddr"), _t("cellSpan"), _t("cellSz")
CELLMARGIN, SUBLIST, P = _t("cellMargin"), _t("subList"), _t("p")

# -- Fix stats ----------------------------------------------------------------
class FixStats:
    def __init__(self):
        self.counts = {"rowCnt": 0, "colCnt": 0, "cellAddr": 0,
                       "cellSpan": 0, "cellSz": 0, "cellMargin": 0, "subList": 0}

    @property
    def total(self) -> int:
        return sum(self.counts.values())

    def __iadd__(self, other: FixStats) -> FixStats:
        for k in self.counts:
            self.counts[k] += other.counts[k]
        return self

    def __str__(self) -> str:
        parts = [f"{k}: {v}" for k, v in self.counts.items() if v]
        return ", ".join(parts) if parts else "no fixes needed"

# -- Helpers ------------------------------------------------------------------
def _child_idx(parent: ET.Element, tag: str) -> int:
    """Index of first child with tag, or len(children) if absent."""
    for i, ch in enumerate(parent):
        if ch.tag == tag:
            return i
    return len(list(parent))

def _ensure(parent: ET.Element, tag: str, attribs: dict,
            idx: int | None = None) -> tuple[ET.Element, bool]:
    """Ensure parent has a child with tag. Returns (element, was_created)."""
    el = parent.find(tag)
    if el is not None:
        return el, False
    el = ET.Element(tag)
    el.attrib.update(attribs)
    if idx is not None:
        parent.insert(idx, el)
    else:
        parent.append(el)
    return el, True

# -- Core fix logic -----------------------------------------------------------
def fix_table(tbl: ET.Element, stats: FixStats) -> None:
    """Fix a single hp:tbl element in-place (non-recursive)."""
    rows = tbl.findall(TR)
    gridcol = tbl.find(GRIDCOL)
    grid_w = [int(it.get("width", "7000")) for it in gridcol.findall(GRIDCOLITEM)] if gridcol is not None else []
    n_rows, n_cols = len(rows), len(grid_w)

    # 1. rowCnt / colCnt
    if tbl.get("rowCnt") != str(n_rows):
        tbl.set("rowCnt", str(n_rows)); stats.counts["rowCnt"] += 1
    if tbl.get("colCnt") != str(n_cols):
        tbl.set("colCnt", str(n_cols)); stats.counts["colCnt"] += 1

    # Track cells covered by rowSpan from above: covered[row] = set of col indices
    covered: dict[int, set[int]] = {i: set() for i in range(n_rows)}

    for ri, tr in enumerate(rows):
        col = 0
        for tc in tr.findall(TC):
            # Advance past columns covered by rowSpan from above
            while col in covered.get(ri, set()):
                col += 1

            # 3. cellSpan -- ensure exists
            span, made = _ensure(tc, CELLSPAN, {"colSpan": "1", "rowSpan": "1"}, 1)
            if made:
                stats.counts["cellSpan"] += 1
            cs = max(1, int(span.get("colSpan", "1")))
            rs = max(1, int(span.get("rowSpan", "1")))
            # Clamp to table bounds
            if n_cols and col + cs > n_cols:
                cs = max(1, n_cols - col)
                span.set("colSpan", str(cs))
            if ri + rs > n_rows:
                rs = max(1, n_rows - ri)
                span.set("rowSpan", str(rs))

            # 2. cellAddr
            addr, addr_new = _ensure(tc, CELLADDR,
                                     {"colAddr": str(col), "rowAddr": str(ri)}, 0)
            if addr_new:
                stats.counts["cellAddr"] += 1
            elif addr.get("colAddr") != str(col) or addr.get("rowAddr") != str(ri):
                addr.set("colAddr", str(col))
                addr.set("rowAddr", str(ri))
                stats.counts["cellAddr"] += 1

            # 4. cellSz
            w = sum(grid_w[c] for c in range(col, min(col + cs, len(grid_w)))) or 7000
            si = _child_idx(tc, CELLMARGIN)
            if si == len(list(tc)):
                si = _child_idx(tc, SUBLIST)
            _, sz_new = _ensure(tc, CELLSZ, {"width": str(w), "height": "1000"}, si)
            if sz_new:
                stats.counts["cellSz"] += 1

            # 5. cellMargin
            mi = _child_idx(tc, SUBLIST)
            _, mg_new = _ensure(tc, CELLMARGIN,
                                {"left": "510", "right": "510",
                                 "top": "141", "bottom": "141"}, mi)
            if mg_new:
                stats.counts["cellMargin"] += 1

            # 6. subList -- wrap stray <hp:p> or create empty
            sub = tc.find(SUBLIST)
            stray = [ch for ch in tc if ch.tag == P]
            if sub is None:
                sub = ET.SubElement(tc, SUBLIST)
                if stray:
                    for p in stray:
                        tc.remove(p); sub.append(p)
                else:
                    ep = ET.SubElement(sub, P)
                    ep.set("paraPrIDRef", "0"); ep.set("styleIDRef", "0")
                stats.counts["subList"] += 1
            elif stray:
                for p in stray:
                    tc.remove(p); sub.append(p)
                stats.counts["subList"] += 1

            # Mark covered cells for spans
            for dri in range(ri, min(ri + rs, n_rows)):
                for dci in range(col, col + cs):
                    if dri != ri or dci != col:
                        covered.setdefault(dri, set()).add(dci)
            col += cs

# -- XML processing -----------------------------------------------------------
def fix_section_xml(xml_bytes: bytes) -> tuple[bytes, FixStats]:
    """Fix all tables in a section XML. Returns (fixed_bytes, stats)."""
    stats = FixStats()
    text = xml_bytes.decode("utf-8")
    is_compact = text.count("\n") <= 2

    root = ET.fromstring(xml_bytes)

    # Collect tables, then fix top-down. To avoid double-processing nested
    # tables, track which elements we have already fixed.
    fixed_set: set[int] = set()
    for tbl in root.iter(TBL):
        if id(tbl) not in fixed_set:
            fix_table(tbl, stats)
            fixed_set.add(id(tbl))
            # Mark nested tables as already handled
            for nested in tbl.iter(TBL):
                if nested is not tbl:
                    fix_table(nested, stats)
                    fixed_set.add(id(nested))

    tree = ET.ElementTree(root)
    if not is_compact:
        ET.indent(tree, space="  ")
    buf = BytesIO()
    tree.write(buf, encoding="utf-8", xml_declaration=True)
    result = buf.getvalue()

    if is_compact:
        result = re.sub(rb">\s+<", b"><", result)
    return result, stats

# -- File-level processing ----------------------------------------------------
def process_xml_file(path: str, output: str | None) -> None:
    with open(path, "rb") as f:
        data = f.read()
    fixed, stats = fix_section_xml(data)
    out = output or path
    with open(out, "wb") as f:
        f.write(fixed)
    print(f"[table_fixer] {Path(path).name}: {stats}")
    if stats.total:
        print(f"[table_fixer] {stats.total} fix(es) applied -> {out}")
    else:
        print("[table_fixer] No fixes were needed.")

def process_hwpx_file(path: str, output: str | None) -> None:
    out_path = output or path
    total = FixStats()
    sec_re = re.compile(r"Contents/section\d+\.xml$", re.IGNORECASE)

    buf = BytesIO()
    with zipfile.ZipFile(path, "r") as zin, zipfile.ZipFile(buf, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if sec_re.search(info.filename):
                fixed, stats = fix_section_xml(data)
                if stats.total:
                    print(f"[table_fixer] {info.filename}: {stats}")
                    total += stats
                    data = fixed
            zout.writestr(copy.copy(info), data)

    with open(out_path, "wb") as f:
        f.write(buf.getvalue())
    if total.total:
        print(f"[table_fixer] Total: {total.total} fix(es) applied -> {out_path}")
    else:
        print("[table_fixer] No fixes were needed in any section.")

# -- Main ---------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Fix HWPX table structure.")
    ap.add_argument("input", help="Section XML or HWPX file")
    ap.add_argument("--output", "-o", help="Output path (default: overwrite)")
    args = ap.parse_args()
    if not Path(args.input).exists():
        print(f"[table_fixer] Error: {args.input} not found", file=sys.stderr)
        sys.exit(1)
    if args.input.lower().endswith(".hwpx"):
        process_hwpx_file(args.input, args.output)
    else:
        process_xml_file(args.input, args.output)

if __name__ == "__main__":
    main()
