#!/bin/bash
# Xstar Sports — Font Bootstrap
# ================================
# 1. Writes a fallback @font-face CSS immediately (works without network)
# 2. Then tries to download actual woff2 files
# 3. If downloads succeed, overwrites CSS with local src paths
# 4. If downloads fail, fallback CSS already works — stream never breaks

set -e
FONTS_DIR="$(cd "$(dirname "$0")" && pwd)"
CSS_OUT="$FONTS_DIR/xstar-fonts.css"

echo "Xstar Sports Font Bootstrap..."

# ── STEP 1: Write fallback CSS immediately ────────────────────────────────────
# This uses local() to pick up system fonts if woff2 files are missing
# Visually close to the intended fonts on Ubuntu (GitHub Actions runner)
cat > "$CSS_OUT" << 'FALLBACK'
/* Xstar Sports — Font CSS (fallback: system fonts) */
/* Overwritten with local woff2 paths if download succeeds */

/* Oswald fallback: Impact/Arial Narrow on Ubuntu */
@font-face { font-family:'Oswald'; font-weight:300; font-display:block;
  src:local('Oswald Light'),local('Arial Narrow'),local('Impact'); }
@font-face { font-family:'Oswald'; font-weight:400; font-display:block;
  src:local('Oswald'),local('Oswald Regular'),local('Arial Narrow'),local('Impact'); }
@font-face { font-family:'Oswald'; font-weight:500; font-display:block;
  src:local('Oswald Medium'),local('Arial Narrow'),local('Impact'); }
@font-face { font-family:'Oswald'; font-weight:600; font-display:block;
  src:local('Oswald SemiBold'),local('Arial Narrow Bold'),local('Impact'); }
@font-face { font-family:'Oswald'; font-weight:700; font-display:block;
  src:local('Oswald Bold'),local('Arial Narrow Bold'),local('Impact'); }

/* Barlow Condensed fallback */
@font-face { font-family:'Barlow Condensed'; font-weight:400; font-display:block;
  src:local('Barlow Condensed'),local('Arial Narrow'),local('Liberation Sans Narrow'); }
@font-face { font-family:'Barlow Condensed'; font-weight:600; font-display:block;
  src:local('Barlow Condensed SemiBold'),local('Arial Narrow Bold'); }
@font-face { font-family:'Barlow Condensed'; font-weight:700; font-display:block;
  src:local('Barlow Condensed Bold'),local('Arial Narrow Bold'); }
@font-face { font-family:'Barlow Condensed'; font-weight:800; font-display:block;
  src:local('Barlow Condensed ExtraBold'),local('Arial Narrow Bold'); }

/* Rajdhani fallback: DejaVu Sans on Ubuntu */
@font-face { font-family:'Rajdhani'; font-weight:400; font-display:block;
  src:local('Rajdhani'),local('DejaVu Sans'),local('Liberation Sans'); }
@font-face { font-family:'Rajdhani'; font-weight:500; font-display:block;
  src:local('Rajdhani Medium'),local('DejaVu Sans'),local('Liberation Sans'); }
@font-face { font-family:'Rajdhani'; font-weight:600; font-display:block;
  src:local('Rajdhani SemiBold'),local('DejaVu Sans Bold'),local('Liberation Sans Bold'); }
@font-face { font-family:'Rajdhani'; font-weight:700; font-display:block;
  src:local('Rajdhani Bold'),local('DejaVu Sans Bold'),local('Liberation Sans Bold'); }
FALLBACK

echo "  ✅ Fallback CSS written"

# ── STEP 2: Try to download woff2 files ───────────────────────────────────────
DOWNLOAD_OK=0
DOWNLOAD_FAIL=0

dl() {
    local name="$1" url="$2" out="$3"
    if curl -sL --max-time 15 --retry 2 -o "$out" "$url" 2>/dev/null && \
       [ -f "$out" ] && [ "$(wc -c < "$out")" -gt 1000 ]; then
        echo "  ✅ $name"
        DOWNLOAD_OK=$((DOWNLOAD_OK + 1))
    else
        rm -f "$out"
        echo "  ⚠️  $name — skipped"
        DOWNLOAD_FAIL=$((DOWNLOAD_FAIL + 1))
    fi
}

# Oswald
dl "Oswald-300" "https://fonts.gstatic.com/s/oswald/v53/TK3_WkUHHAIjg75-b78.woff2"         "$FONTS_DIR/oswald-300.woff2"
dl "Oswald-400" "https://fonts.gstatic.com/s/oswald/v53/TK3_WkUHHAIjg75cbrFZ.woff2"         "$FONTS_DIR/oswald-400.woff2"
dl "Oswald-500" "https://fonts.gstatic.com/s/oswald/v53/TK3_WkUHHAIjg752ZL5Z.woff2"         "$FONTS_DIR/oswald-500.woff2"
dl "Oswald-600" "https://fonts.gstatic.com/s/oswald/v53/TK3_WkUHHAIjg750a75Z.woff2"         "$FONTS_DIR/oswald-600.woff2"
dl "Oswald-700" "https://fonts.gstatic.com/s/oswald/v53/TK3_WkUHHAIjg75NaL5Z.woff2"         "$FONTS_DIR/oswald-700.woff2"

# Barlow Condensed
dl "BarlowCond-400" "https://fonts.gstatic.com/s/barlowcondensed/v12/HTxwL3I-JCGChYJ8VI-L6OO_au7B43LT.woff2"    "$FONTS_DIR/barlow-condensed-400.woff2"
dl "BarlowCond-600" "https://fonts.gstatic.com/s/barlowcondensed/v12/HTxxL3I-JCGChYJ8VI-L6OO_au7B6xTrW3ZW.woff2" "$FONTS_DIR/barlow-condensed-600.woff2"
dl "BarlowCond-700" "https://fonts.gstatic.com/s/barlowcondensed/v12/HTxxL3I-JCGChYJ8VI-L6OO_au7B497SW3ZW.woff2" "$FONTS_DIR/barlow-condensed-700.woff2"
dl "BarlowCond-800" "https://fonts.gstatic.com/s/barlowcondensed/v12/HTxxL3I-JCGChYJ8VI-L6OO_au7B43DXWXZW.woff2" "$FONTS_DIR/barlow-condensed-800.woff2"

# Rajdhani
dl "Rajdhani-400" "https://fonts.gstatic.com/s/rajdhani/v17/LDI2apCSOBg7S-QT7pasEeIe.woff2"       "$FONTS_DIR/rajdhani-400.woff2"
dl "Rajdhani-500" "https://fonts.gstatic.com/s/rajdhani/v17/LDI3apCSOBg7S-QT7p4GM-aGSNip.woff2"  "$FONTS_DIR/rajdhani-500.woff2"
dl "Rajdhani-600" "https://fonts.gstatic.com/s/rajdhani/v17/LDI3apCSOBg7S-QT7p4GF-2GSNip.woff2"  "$FONTS_DIR/rajdhani-600.woff2"
dl "Rajdhani-700" "https://fonts.gstatic.com/s/rajdhani/v17/LDI3apCSOBg7S-QT7p4GK-yGSNip.woff2"  "$FONTS_DIR/rajdhani-700.woff2"

echo ""
echo "Downloads: $DOWNLOAD_OK ok, $DOWNLOAD_FAIL skipped"

# ── STEP 3: If downloads succeeded, overwrite CSS with local paths ─────────────
if [ "$DOWNLOAD_OK" -gt 0 ]; then
    echo "Writing local font CSS..."
    # Build CSS with local file paths where files exist, fallback where not
    {
        echo "/* Xstar Sports — Self-hosted fonts + system fallbacks */"
        echo ""

        # Oswald faces
        for weight in 300 400 500 600 700; do
            f="$FONTS_DIR/oswald-${weight}.woff2"
            if [ -f "$f" ]; then
                echo "@font-face { font-family:'Oswald'; font-weight:${weight}; font-display:block;"
                echo "  src:url('fonts/oswald-${weight}.woff2') format('woff2'),local('Oswald'),local('Impact'); }"
            fi
        done
        echo ""

        # Barlow Condensed faces
        for weight in 400 600 700 800; do
            f="$FONTS_DIR/barlow-condensed-${weight}.woff2"
            if [ -f "$f" ]; then
                echo "@font-face { font-family:'Barlow Condensed'; font-weight:${weight}; font-display:block;"
                echo "  src:url('fonts/barlow-condensed-${weight}.woff2') format('woff2'),local('Barlow Condensed'),local('Arial Narrow'); }"
            fi
        done
        echo ""

        # Rajdhani faces
        for weight in 400 500 600 700; do
            f="$FONTS_DIR/rajdhani-${weight}.woff2"
            if [ -f "$f" ]; then
                echo "@font-face { font-family:'Rajdhani'; font-weight:${weight}; font-display:block;"
                echo "  src:url('fonts/rajdhani-${weight}.woff2') format('woff2'),local('Rajdhani'),local('DejaVu Sans'); }"
            fi
        done
    } > "$CSS_OUT"

    WOFF2_COUNT=$(ls "$FONTS_DIR"/*.woff2 2>/dev/null | wc -l)
    echo "✅ Local font CSS written ($WOFF2_COUNT woff2 files)"
else
    echo "ℹ️  All downloads failed — using system font fallbacks (CSS already written)"
fi

echo "Font bootstrap complete."
