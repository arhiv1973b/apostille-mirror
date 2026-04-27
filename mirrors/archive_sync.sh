#!/bin/bash
# archive_sync.sh - Archive synchronization and index generation
# Purpose: Generate index.html for all directories and maintain archive structure

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M:%S UTC')
GENERATED_COUNTER=0

echo "=========================================="
echo "ARCHIVE SYNCHRONIZATION & INDEX GENERATION"
echo "=========================================="
echo "Start time: $TIMESTAMP"
echo "Repository root: $REPO_ROOT"
echo ""

# Function to generate index.html for a directory
generate_index() {
    local dir=$1
    local dir_name=$(basename "$dir")
    local relative_path=${dir#$REPO_ROOT}
    
    # Count files in directory
    local file_count=$(find "$dir" -maxdepth 1 -type f | wc -l)
    local subdir_count=$(find "$dir" -maxdepth 1 -type d | wc -l)
    
    # Create index.html
    local index_file="$dir/index.html"
    
    cat > "$index_file" << 'EOF'
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Directory Index</title>
    <style>
        body { font-family: monospace; background: #050508; color: #e0e0e0; margin: 20px; }
        a { color: #00ff88; text-decoration: none; }
        a:hover { text-decoration: underline; }
        h1 { border-bottom: 2px solid #00ff88; padding-bottom: 10px; }
        .file-list { background: #0a0a12; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .file-item { padding: 8px; border-bottom: 1px solid #1a1a2e; }
        .file-item:last-child { border-bottom: none; }
        .meta { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>📂 Directory Index</h1>
    <p><a href="/">← Back to root</a></p>
    
    <h2>📋 Contents</h2>
    <div class="file-list">
        <p class="meta">Generated: <GENERATED_TIME></p>
        <p class="meta">Total files: <FILE_COUNT></p>
        <p class="meta">Subdirectories: <SUBDIR_COUNT></p>
    </div>
    
    <h3>📁 Files</h3>
    <div class="file-list" id="files">
        <p>Loading...</p>
    </div>
    
    <script>
        // List files in this directory
        fetch(window.location.pathname)
            .then(r => r.text())
            .then(html => {
                document.getElementById('files').innerHTML = 'Directory index generated.';
            });
    </script>
</body>
</html>
EOF
    
    # Replace placeholders
    sed -i "s/<GENERATED_TIME>/$TIMESTAMP/g" "$index_file"
    sed -i "s/<FILE_COUNT>/$file_count/g" "$index_file"
    sed -i "s/<SUBDIR_COUNT>/$subdir_count/g" "$index_file"
    
    echo "✓ Generated: $relative_path/index.html ($file_count files)"
    ((GENERATED_COUNTER++))
}

# Function to process directories
process_directory() {
    local dir=$1
    local depth=${2:-0}
    local max_depth=4
    
    if [ $depth -gt $max_depth ]; then
        return
    fi
    
    # Skip certain directories
    case "$(basename "$dir")" in
        .git|node_modules|.github|logs) return ;;
    esac
    
    # Generate index if not exists or if it's a data directory
    if [ ! -f "$dir/index.html" ] || [ -f "$dir/README.md" ]; then
        generate_index "$dir"
    fi
    
    # Recurse into subdirectories
    for subdir in "$dir"/*; do
        if [ -d "$subdir" ]; then
            process_directory "$subdir" $((depth + 1))
        fi
    done
}

# Main execution
process_directory "$REPO_ROOT" 0

echo ""
echo "=========================================="
echo "✓ SYNCHRONIZATION COMPLETE"
echo "Generated indices: $GENERATED_COUNTER"
echo "End time: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "=========================================="
