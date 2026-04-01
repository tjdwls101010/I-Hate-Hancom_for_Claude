#!/usr/bin/env python3
"""
md_lint.py — Mechanical markdown linter for pre-processing.

Applies deterministic formatting rules before Claude's semantic normalization.
Modifies the file in-place.

Rules:
  1. heading-increment   — fix skipped heading levels (#→#### becomes #→##)
  2. consecutive-blanks   — collapse multiple blank lines to one
  3. list-spacing         — remove blank lines between list items
  4. multiple-spaces      — collapse consecutive spaces to one (preserves indent)
  5. trailing-spaces      — remove trailing whitespace per line
  6. eof-newline          — ensure single newline at end of file

Usage:
    python3 md_lint.py input.md              # lint in-place
    python3 md_lint.py input.md -o out.md    # lint to new file
    python3 md_lint.py input.md --dry-run    # preview changes without writing
"""

import argparse
import re
import sys


def fix_heading_increment(lines):
    """Ensure heading levels only increment by one.

    Scans top-to-bottom, tracking the previous heading level.
    If a heading jumps more than one level (e.g., # → ####),
    it is reduced to previous_level + 1.
    """
    result = []
    prev_level = 0
    for line in lines:
        m = re.match(r'^(#{1,6})\s', line)
        if m:
            current_level = len(m.group(1))
            if prev_level > 0 and current_level > prev_level + 1:
                new_level = prev_level + 1
                line = '#' * new_level + line[current_level:]
                current_level = new_level
            prev_level = current_level
        result.append(line)
    return result


def collapse_consecutive_blanks(lines):
    """Reduce multiple consecutive blank lines to a single blank line."""
    result = []
    prev_blank = False
    for line in lines:
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank
    return result


def remove_blanks_between_list_items(lines):
    """Remove blank lines between consecutive list items.

    If a list item is followed by blank line(s) then another list item,
    the blank lines are removed to keep the list compact.
    """
    result = []
    list_pattern = re.compile(r'^\s*[-*+]\s|^\s*\d+\.\s')
    i = 0
    while i < len(lines):
        result.append(lines[i])
        if list_pattern.match(lines[i]):
            # Look ahead: skip blanks if followed by another list item
            j = i + 1
            blanks = 0
            while j < len(lines) and lines[j].strip() == '':
                blanks += 1
                j += 1
            if blanks > 0 and j < len(lines) and list_pattern.match(lines[j]):
                i = j  # skip blank lines
                continue
        i += 1
    return result


def fix_multiple_spaces(lines):
    """Collapse consecutive spaces within text to a single space.

    Preserves leading indentation. Skips code fences and table separators.
    """
    result = []
    in_code = False
    for line in lines:
        stripped = line.strip()
        # Track code fences
        if stripped.startswith('```'):
            in_code = not in_code
            result.append(line)
            continue
        if in_code:
            result.append(line)
            continue
        # Skip table separator lines (|---|---|)
        if re.match(r'^\s*\|[\s:|-]+\|\s*$', stripped):
            result.append(line)
            continue
        # Preserve leading whitespace, fix interior spaces
        m = re.match(r'^(\s*)(.*)', line)
        indent = m.group(1)
        content = m.group(2)
        content = re.sub(r' {2,}', ' ', content)
        result.append(indent + content)
    return result


def strip_trailing_spaces(lines):
    """Remove trailing whitespace from each line."""
    return [line.rstrip() for line in lines]


def ensure_eof_newline(lines):
    """Ensure exactly one trailing newline (empty string at end of list)."""
    while lines and lines[-1].strip() == '':
        lines.pop()
    lines.append('')
    return lines


def lint(text):
    """Apply all lint rules to markdown text. Returns linted text."""
    lines = text.split('\n')

    # Order matters: trailing spaces first, then structural, then content
    lines = strip_trailing_spaces(lines)
    lines = fix_heading_increment(lines)
    lines = remove_blanks_between_list_items(lines)
    lines = collapse_consecutive_blanks(lines)
    lines = fix_multiple_spaces(lines)
    lines = ensure_eof_newline(lines)

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Mechanical markdown linter for pre-processing')
    parser.add_argument('input', help='Path to markdown file')
    parser.add_argument('-o', '--output', help='Output path (default: in-place)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print result to stdout without writing')
    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        original = f.read()

    result = lint(original)

    if args.dry_run:
        sys.stdout.write(result)
        return

    out_path = args.output or args.input
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result)

    # Report changes
    orig_lines = original.split('\n')
    result_lines = result.split('\n')
    if original == result:
        print(f'[LINT] {args.input}: no changes needed')
    else:
        print(f'[LINT] {args.input}: {len(orig_lines)} → {len(result_lines)} lines')


if __name__ == '__main__':
    main()
