#!/bin/bash

# =============================================================================
# Vibe Continuity - Large File Chunked Reader
# Version: 2.1.0
# Purpose: Read large files in controlled chunks to avoid context overflow
# Usage: read_large_file.sh <file> [line_number] [lines_before] [lines_after]
#    If line_number provided: read chunk around that line
#    If no line_number: read header + footer
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Defaults
DEFAULT_CHUNK_SIZE=50
MAX_CHUNK_SIZE=100
HEADER_LINES=50
FOOTER_LINES=50
CONTEXT_BEFORE=20
CONTEXT_AFTER=30

# Usage
usage() {
    echo "Usage: $0 <file> [line_number] [context_before] [context_after]"
    echo ""
    echo "Read large files in controlled chunks:"
    echo ""
    echo "  $0 huge_file.py                    # Read header + footer"
    echo "  $0 huge_file.py 500                # Read around line 500"
    echo "  $0 huge_file.py 500 25 35          # Read lines 475-535"
    echo ""
    echo "Environment variables:"
    echo "  CHUNK_SIZE: lines per chunk (default: $DEFAULT_CHUNK_SIZE)"
    echo "  MAX_CHUNK: max lines to read (default: $MAX_CHUNK_SIZE)"
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

FILE="$1"
LINE_NUMBER="${2:-}"
CONTEXT_BEFORE=${3:-$CONTEXT_BEFORE}
CONTEXT_AFTER=${4:-$CONTEXT_AFTER}

# Validate file exists
if [ ! -f "$FILE" ]; then
    echo "${RED}❌ File not found: $FILE${NC}" >&2
    exit 1
fi

# Get file info
TOTAL_LINES=$(wc -l < "$FILE")
FILE_SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE")
FILE_SIZE_KB=$((FILE_SIZE / 1024))

echo "📄 File: $FILE"
echo "   Lines: $TOTAL_LINES | Size: ${FILE_SIZE_KB}KB"

# Settings from environment
CHUNK_SIZE=${CHUNK_SIZE:-$DEFAULT_CHUNK_SIZE}
MAX_CHUNK=${MAX_CHUNK:-$MAX_CHUNK_SIZE}

# If line number provided, read around it
if [ -n "$LINE_NUMBER" ]; then
    # Validate line number
    if ! [[ "$LINE_NUMBER" =~ ^[0-9]+$ ]] || [ "$LINE_NUMBER" -lt 1 ] || [ "$LINE_NUMBER" -gt "$TOTAL_LINES" ]; then
        echo "${RED}❌ Invalid line number: $LINE_NUMBER (must be 1-$TOTAL_LINES)${NC}" >&2
        exit 1
    fi
    
    # Calculate range
    START=$((LINE_NUMBER - CONTEXT_BEFORE))
    END=$((LINE_NUMBER + CONTEXT_AFTER))
    
    # Clamp to valid range
    START=$(max 1 $START)
    END=$(min $TOTAL_LINES $END)
    
    NUM_LINES=$((END - START + 1))
    
    if [ "$NUM_LINES" -gt "$MAX_CHUNK" ]; then
        echo "${YELLOW}⚠️  Requested $NUM_LINES lines exceeds max of $MAX_CHUNK, truncating${NC}" >&2
        # Center on the line number
        START=$((LINE_NUMBER - MAX_CHUNK / 2))
        END=$((LINE_NUMBER + MAX_CHUNK / 2))
        START=$(max 1 $START)
        END=$(min $TOTAL_LINES $END)
        NUM_LINES=$((END - START + 1))
    fi
    
    echo "📍 Reading lines $START-$END (around line $LINE_NUMBER):"
    echo "───────────────────────────────────────────────────"
    sed -n "${START},${END}p" "$FILE"
    echo "───────────────────────────────────────────────────"
    echo ""
    echo "📌 Line $LINE_NUMBER is at position $((LINE_NUMBER - START + 1)) in this chunk"
    
# Otherwise, read header + footer
else
    echo "📍 Reading header and footer:"
    echo ""
    
    # Header
    HEAD_LINES=$(min $HEADER_LINES $TOTAL_LINES)
    if [ "$HEAD_LINES" -gt 0 ]; then
        echo "🔝 HEADER (lines 1-$HEAD_LINES):"
        echo "───────────────────────────────────────────────────"
        head -n $HEAD_LINES "$FILE"
        echo "───────────────────────────────────────────────────"
        echo ""
    fi
    
    # Footer - only if file is large enough
    if [ "$TOTAL_LINES" -gt $((HEADER_LINES + FOOTER_LINES)) ]; then
        FOOT_START=$((TOTAL_LINES - FOOTER_LINES + 1))
        echo "🔻 FOOTER (lines $FOOT_START-$TOTAL_LINES):"
        echo "───────────────────────────────────────────────────"
        tail -n $FOOTER_LINES "$FILE"
        echo "───────────────────────────────────────────────────"
        echo ""
        echo "⏭️  ... $((TOTAL_LINES - HEADER_LINES - FOOTER_LINES)) lines not shown"
    fi
fi

echo ""
echo "✅ Chunk completed. Context used: ~$NUM_LINES lines"

# Helper functions for min/max
min() {
    if [ "$1" -lt "$2" ]; then
        echo "$1"
    else
        echo "$2"
    fi
}

max() {
    if [ "$1" -gt "$2" ]; then
        echo "$1"
    else
        echo "$2"
    fi
}
