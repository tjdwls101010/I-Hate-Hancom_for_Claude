#!/usr/bin/env python3
"""Validate HWPX file structural integrity.

Usage:
    python3 validate_hwpx.py input.hwpx
    python3 validate_hwpx.py --section section0.xml --header header.xml
"""
import argparse, sys, xml.etree.ElementTree as ET, zipfile
from pathlib import Path

NS = {
    "hh": "http://www.hancom.co.kr/hwpml/2011/head",
    "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    "hs": "http://www.hancom.co.kr/hwpml/2011/section",
    "hc": "http://www.hancom.co.kr/hwpml/2011/core",
    "opf": "http://www.idpf.org/2007/opf/",
}
LANGS = ("hangul", "latin", "hanja", "japanese", "other", "symbol", "user")
LANG_MAP = {k.upper(): k for k in LANGS}
REQUIRED = ["mimetype", "Contents/header.xml", "Contents/section0.xml",
            "Contents/content.hpf", "META-INF/container.xml",
            "version.xml", "settings.xml"]

def _t(ns, tag):
    return f"{{{NS[ns]}}}{tag}"

# -- Result tracker ----------------------------------------------------------
_pass = _warn = _fail = 0
def report(level, msg):
    global _pass, _warn, _fail
    print(f"[{level}] {msg}")
    if level == "PASS": _pass += 1
    elif level == "WARN": _warn += 1
    else: _fail += 1

# -- Header parsing -----------------------------------------------------------
def parse_header(root):
    ids = {"charPr": set(), "paraPr": set(), "borderFill": set()}
    fonts = {g: set() for g in LANGS}
    font_refs = []  # (charPr_id, lang, ref_id)

    for el in root.iter(_t("hh", "charPr")):
        cid = el.get("id")
        if cid is not None:
            ids["charPr"].add(int(cid))
            for fr in el.iter(_t("hh", "fontRef")):
                for lang in LANGS:
                    v = fr.get(lang)
                    if v is not None:
                        font_refs.append((int(cid), lang, int(v)))
    for el in root.iter(_t("hh", "paraPr")):
        pid = el.get("id")
        if pid is not None: ids["paraPr"].add(int(pid))
    for el in root.iter(_t("hh", "borderFill")):
        bid = el.get("id")
        if bid is not None: ids["borderFill"].add(int(bid))
    for ff in root.iter(_t("hh", "fontface")):
        lk = LANG_MAP.get(ff.get("lang", ""))
        if lk is None: continue
        for fe in ff.iter(_t("hh", "font")):
            fid = fe.get("id")
            if fid is not None: fonts[lk].add(int(fid))
    return ids, fonts, font_refs

def check_header_font_refs(fonts, font_refs):
    bad = [(c, l, r) for c, l, r in font_refs if r not in fonts.get(l, set())]
    if bad:
        for c, l, r in bad[:10]:
            report("FAIL", f"charPr id={c} fontRef {l}={r} not in {l} font list")
        if len(bad) > 10:
            report("FAIL", f"... and {len(bad)-10} more invalid fontRef entries")
    else:
        report("PASS", "All charPr fontRef IDs reference valid font IDs")

# -- Section validation -------------------------------------------------------
def check_section_ids(root, ids, name):
    for tag, attr, id_key, parent_desc in [
        ("run", "charPrIDRef", "charPr", "charPrIDRef"),
        ("p", "paraPrIDRef", "paraPr", "paraPrIDRef"),
    ]:
        bad = set()
        for el in root.iter(_t("hp", tag)):
            ref = el.get(attr)
            if ref is not None and int(ref) not in ids[id_key]:
                bad.add(int(ref))
        if bad:
            report("FAIL", f"{name}: invalid {parent_desc}(s): {sorted(bad)[:10]}")
        else:
            report("PASS", f"{name}: all {parent_desc} values are valid")
    # borderFillIDRef on hp:tc
    bad = set()
    for tc in root.iter(_t("hp", "tc")):
        ref = tc.get("borderFillIDRef")
        if ref is not None and int(ref) not in ids["borderFill"]:
            bad.add(int(ref))
    if bad:
        report("FAIL", f"{name}: invalid borderFillIDRef(s) on tc: {sorted(bad)[:10]}")
    else:
        report("PASS", f"{name}: all tc borderFillIDRef values are valid")

def check_tables(root, name):
    tbl_idx = 0
    for tbl in root.iter(_t("hp", "tbl")):
        tbl_idx += 1
        label = f"{name} tbl#{tbl_idx}"
        row_cnt, col_cnt = tbl.get("rowCnt"), tbl.get("colCnt")
        direct_rows = [c for c in tbl if c.tag == _t("hp", "tr")]
        # rowCnt
        if row_cnt is not None:
            exp = int(row_cnt)
            if exp != len(direct_rows):
                report("FAIL", f"{label}: rowCnt={exp} but {len(direct_rows)} <tr>")
            else:
                report("PASS", f"{label}: rowCnt={exp} matches <tr> count")
        # colCnt vs gridColItem
        gc = tbl.find(_t("hp", "gridCol"))
        if gc is not None and col_cnt is not None:
            items = list(gc.iter(_t("hp", "gridColItem")))
            exp = int(col_cnt)
            if len(items) != exp:
                report("FAIL", f"{label}: colCnt={exp} but {len(items)} gridColItem")
            else:
                report("PASS", f"{label}: colCnt={exp} matches gridColItem count")
        # cellAddr per row
        for ri, tr in enumerate(direct_rows):
            cells = [c for c in tr if c.tag == _t("hp", "tc")]
            addrs = []
            for tc in cells:
                a = tc.find(_t("hp", "cellAddr"))
                if a is None: continue
                ca, ra = a.get("colAddr"), a.get("rowAddr")
                if ca is not None: addrs.append(int(ca))
                if ra is not None and int(ra) != ri:
                    report("WARN", f"{label} row {ri}: rowAddr={ra} mismatch")
            for j in range(1, len(addrs)):
                if addrs[j] <= addrs[j-1]:
                    report("WARN", f"{label} row {ri}: colAddr not increasing: {addrs}")
                    break
    if tbl_idx == 0:
        report("PASS", f"{name}: no tables to validate")

# -- ZIP-level checks ---------------------------------------------------------
def check_zip_structure(zf):
    names = zf.namelist()
    if names and names[0] == "mimetype":
        report("PASS", "mimetype is first ZIP entry")
    else:
        report("FAIL", f"mimetype not first entry (got: {names[0] if names else 'empty'})")
    try:
        mt = zf.read("mimetype").decode("utf-8").strip()
        if mt == "application/hwp+zip":
            report("PASS", "mimetype content is correct")
        else:
            report("FAIL", f"mimetype='{mt}', expected 'application/hwp+zip'")
    except KeyError:
        report("FAIL", "mimetype file missing")
    for req in REQUIRED:
        report("PASS" if req in names else "FAIL",
               f"{'Present' if req in names else 'Missing'}: {req}")

def check_content_hpf(zf):
    try: data = zf.read("Contents/content.hpf")
    except KeyError: return
    try: root = ET.fromstring(data)
    except ET.ParseError as e:
        report("FAIL", f"content.hpf parse error: {e}"); return
    zip_names = set(zf.namelist())
    bad = []
    for item in root.iter(_t("opf", "item")):
        href = item.get("href")
        if href is None: continue
        full = href.lstrip("/")
        if full not in zip_names: bad.append(full)
    if bad:
        for b in bad[:10]: report("FAIL", f"content.hpf refs missing: {b}")
    else:
        report("PASS", "content.hpf references all resolve to ZIP entries")

def check_container_rdf(zf):
    try: data = zf.read("META-INF/container.rdf")
    except KeyError:
        report("WARN", "container.rdf not found (optional)"); return
    try: root = ET.fromstring(data)
    except ET.ParseError as e:
        report("FAIL", f"container.rdf parse error: {e}"); return
    rdf_secs = set()
    for el in root.iter():
        for src in ([el.text] if el.text else []) + list(el.attrib.values()):
            if src and src.strip().startswith("Contents/section") and src.strip().endswith(".xml"):
                rdf_secs.add(src.strip())
    zip_secs = {n for n in zf.namelist()
                if n.startswith("Contents/section") and n.endswith(".xml")}
    for m in sorted(rdf_secs - zip_secs):
        report("FAIL", f"container.rdf lists {m} but not in ZIP")
    for m in sorted(zip_secs - rdf_secs):
        report("WARN", f"{m} in ZIP but not in container.rdf")
    if not (rdf_secs - zip_secs) and not (zip_secs - rdf_secs):
        report("PASS", "container.rdf section list matches ZIP contents")

# -- Entry points -------------------------------------------------------------
def _parse_sections(zf):
    return sorted(n for n in zf.namelist()
                  if n.startswith("Contents/section") and n.endswith(".xml"))

def validate_hwpx(path):
    if not zipfile.is_zipfile(path):
        report("FAIL", f"{path} is not a valid ZIP"); return
    with zipfile.ZipFile(path, "r") as zf:
        print(f"=== Validating HWPX: {path} ===\n")
        print("-- ZIP Structure --")
        check_zip_structure(zf)
        print("\n-- ID Reference Integrity --")
        try:
            hdr = ET.fromstring(zf.read("Contents/header.xml"))
        except (KeyError, ET.ParseError) as e:
            report("FAIL", f"header.xml error: {e}"); return
        ids, fonts, frefs = parse_header(hdr)
        report("PASS", f"header.xml: {len(ids['charPr'])} charPr, "
               f"{len(ids['paraPr'])} paraPr, {len(ids['borderFill'])} borderFill")
        check_header_font_refs(fonts, frefs)
        for sn in _parse_sections(zf):
            try:
                sr = ET.fromstring(zf.read(sn))
                check_section_ids(sr, ids, sn)
            except ET.ParseError as e:
                report("FAIL", f"{sn} parse error: {e}")
        print("\n-- Table Structure --")
        for sn in _parse_sections(zf):
            try: check_tables(ET.fromstring(zf.read(sn)), sn)
            except ET.ParseError: pass
        print("\n-- Content Consistency --")
        check_content_hpf(zf)
        check_container_rdf(zf)
        print()

def validate_section_header(section_path, header_path):
    print(f"=== Validating: {section_path} against {header_path} ===\n")
    print("-- ID Reference Integrity --")
    try:
        hdr = ET.parse(header_path).getroot()
    except (ET.ParseError, FileNotFoundError) as e:
        report("FAIL", f"header error: {e}"); return
    ids, fonts, frefs = parse_header(hdr)
    report("PASS", f"header.xml: {len(ids['charPr'])} charPr, "
           f"{len(ids['paraPr'])} paraPr, {len(ids['borderFill'])} borderFill")
    check_header_font_refs(fonts, frefs)
    try:
        sr = ET.parse(section_path).getroot()
        name = Path(section_path).name
    except (ET.ParseError, FileNotFoundError) as e:
        report("FAIL", f"section error: {e}"); return
    check_section_ids(sr, ids, name)
    print("\n-- Table Structure --")
    check_tables(sr, name)
    print()

def main():
    ap = argparse.ArgumentParser(description="Validate HWPX structural integrity.")
    ap.add_argument("hwpx", nargs="?", help="Path to .hwpx file")
    ap.add_argument("--section", help="Section XML file path")
    ap.add_argument("--header", help="Header XML file path")
    args = ap.parse_args()
    if args.section and args.header:
        validate_section_header(args.section, args.header)
    elif args.hwpx:
        validate_hwpx(args.hwpx)
    else:
        ap.error("Provide a .hwpx file or both --section and --header")
    print(f"\n--- Summary: {_pass} passed, {_warn} warnings, {_fail} failures ---")
    sys.exit(1 if _fail > 0 else 0)

if __name__ == "__main__":
    main()
