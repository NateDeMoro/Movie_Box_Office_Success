#!/bin/bash
# Sync Obsidian notes to docs folder for git commits

OBSIDIAN_FOLDER="/Users/ndemoro/Desktop/FOLDERS/Nate_Obsidian/Movie_project_folder"
DOCS_FOLDER="docs"

echo "Syncing Obsidian notes to docs folder..."

# Copy markdown files from Obsidian to docs
cp "$OBSIDIAN_FOLDER/Movie Box Office - EDA Findings.md" "$DOCS_FOLDER/"
cp "$OBSIDIAN_FOLDER/Movie Project Plan.md" "$DOCS_FOLDER/"

echo "✅ Notes synced successfully!"
echo ""
echo "Files updated:"
echo "  - Movie Box Office - EDA Findings.md"
echo "  - Movie Project Plan.md"
echo ""
echo "To commit these changes:"
echo "  git add docs/"
echo "  git commit -m 'Update Obsidian notes'"
