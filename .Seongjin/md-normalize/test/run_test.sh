#!/bin/bash
# Test runner: regenerate HWPX from test inputs and compare with baseline
# Usage: bash run_test.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_DIR="$SCRIPT_DIR"
BASELINE_DIR="$TEST_DIR/baseline"
OUTPUT_DIR="$TEST_DIR/output"
MD2HWPX="$(cd "$SCRIPT_DIR/../../../.claude/skills/Hancom/scripts" && pwd)/md_to_hwpx.py"
VALIDATE="$(cd "$SCRIPT_DIR/../../../.claude/skills/Hancom/scripts" && pwd)/validate_hwpx.py"
HEADER="$(cd "$SCRIPT_DIR/../../../.claude/skills/Hancom/templates/base/Contents" && pwd)/header.xml"

mkdir -p "$OUTPUT_DIR"

PASS=0
FAIL=0

for name in 이상민 슬로우뉴스 08_lsi 조켄트; do
    echo "━━━ Testing: $name ━━━"

    # Generate
    python3 "$MD2HWPX" "$TEST_DIR/${name}.md" --output "$OUTPUT_DIR/${name}.hwpx" 2>/dev/null

    # Validate
    RESULT=$(python3 "$VALIDATE" --section "$OUTPUT_DIR/${name}_section0.xml" --header "$HEADER" 2>&1 | tail -1)
    echo "  Validation: $RESULT"

    if echo "$RESULT" | grep -q "0 failures"; then
        # Compare section0.xml with baseline
        BASELINE_XML="$BASELINE_DIR/${name}_section0.xml"
        OUTPUT_XML="$OUTPUT_DIR/${name}_section0.xml"

        if diff -q "$BASELINE_XML" "$OUTPUT_XML" > /dev/null 2>&1; then
            echo "  Diff: ✅ IDENTICAL to baseline"
            PASS=$((PASS + 1))
        else
            DIFF_LINES=$(diff "$BASELINE_XML" "$OUTPUT_XML" | grep -c "^[<>]")
            echo "  Diff: ⚠️  $DIFF_LINES lines differ from baseline"
            FAIL=$((FAIL + 1))
        fi
    else
        echo "  ❌ VALIDATION FAILED"
        FAIL=$((FAIL + 1))
    fi
    echo ""
done

echo "━━━ Results: $PASS passed, $FAIL failed ━━━"
