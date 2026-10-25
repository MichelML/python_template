#!/usr/bin/env bash
# Copy this Python scaffold into an existing repo.
#
# Usage: scripts/bootstrap.sh <target-dir>
#
# - Existing files in the target are never overwritten; they are skipped with a warning.
# - README.md (preferred) or README: this repo's README content is appended to it.
#   If neither exists, README.md is copied.
# - .gitignore: appended to an existing one so the venv and tool caches stay ignored.
# - If the target already has a pyproject.toml, uv.lock is not copied and `uv sync` is skipped:
#   merge our [dependency-groups] and [tool.*] sections into it by hand first.
# - Otherwise runs `uv sync` in the target. It never runs formatters, so existing code is untouched.
set -euo pipefail

readonly SCAFFOLD_FILES=(
  .python-version
  pyproject.toml
  uv.lock
  Makefile
  CLAUDE.md
  app/__init__.py
  app/__main__.py
  app/errors.py
  app/logger.py
  tests/__init__.py
  tests/conftest.py
  tests/test_errors.py
  tests/test_logger.py
  tests/test_main.py
)
readonly APPENDED_MARKER="<!-- appended by scaffold bootstrap -->"
readonly GITIGNORE_MARKER="# --- appended by scaffold bootstrap ---"

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly SOURCE_DIR

skipped=()

usage() {
  echo "Usage: $0 <target-dir>" >&2
  exit 1
}

copy_file() {
  local relative_path="$1" target_dir="$2"
  local destination="$target_dir/$relative_path"
  if [[ -e "$destination" ]]; then
    skipped+=("$relative_path")
    return
  fi
  mkdir -p "$(dirname "$destination")"
  cp "$SOURCE_DIR/$relative_path" "$destination"
  echo "  copied    $relative_path"
}

find_readme() {
  local target_dir="$1" candidate
  for candidate in README.md README; do
    if [[ -f "$target_dir/$candidate" ]]; then
      echo "$candidate"
      return
    fi
  done
}

# Appends $source_file to $destination behind $marker, unless it was already appended or copied.
append_once() {
  local source_file="$1" destination="$2" marker="$3" label="$4"
  if grep -qF -- "$marker" "$destination" || cmp -s "$source_file" "$destination"; then
    echo "  unchanged $label (already appended)"
    return
  fi
  {
    printf '\n%s\n\n' "$marker"
    cat "$source_file"
  } >>"$destination"
  echo "  appended  $label"
}

merge_readme() {
  local target_dir="$1" readme
  readme="$(find_readme "$target_dir")"
  if [[ -z "$readme" ]]; then
    copy_file README.md "$target_dir"
    return
  fi
  append_once "$SOURCE_DIR/README.md" "$target_dir/$readme" "$APPENDED_MARKER" "$readme"
}

merge_gitignore() {
  local target_dir="$1"
  if [[ ! -e "$target_dir/.gitignore" ]]; then
    copy_file .gitignore "$target_dir"
    return
  fi
  append_once "$SOURCE_DIR/.gitignore" "$target_dir/.gitignore" "$GITIGNORE_MARKER" .gitignore
}

main() {
  [[ $# -eq 1 ]] || usage
  [[ -d "$1" ]] || { echo "error: '$1' is not a directory" >&2; exit 1; }
  local target_dir
  target_dir="$(cd "$1" && pwd)"
  if [[ "$target_dir" == "$SOURCE_DIR" ]]; then
    echo "error: target is the scaffold repo itself" >&2
    exit 1
  fi

  local has_own_pyproject=false
  if [[ -e "$target_dir/pyproject.toml" ]] \
    && ! cmp -s "$SOURCE_DIR/pyproject.toml" "$target_dir/pyproject.toml"; then
    has_own_pyproject=true
  fi

  echo "Bootstrapping $target_dir"
  local file
  for file in "${SCAFFOLD_FILES[@]}"; do
    if [[ "$file" == uv.lock && "$has_own_pyproject" == true ]]; then
      echo "  skipped   uv.lock (it would not match the existing pyproject.toml)"
      continue
    fi
    copy_file "$file" "$target_dir"
  done
  merge_readme "$target_dir"
  merge_gitignore "$target_dir"

  if [[ ${#skipped[@]} -gt 0 ]]; then
    echo "Skipped (already exist, merge by hand if needed):"
    printf '  %s\n' "${skipped[@]}"
  fi

  if [[ "$has_own_pyproject" == true ]]; then
    echo "Existing pyproject.toml kept. Merge [dependency-groups] and [tool.*] from"
    echo "  $SOURCE_DIR/pyproject.toml"
    echo "then run: cd $target_dir && uv sync && make check"
    return
  fi

  echo "Running uv sync..."
  (cd "$target_dir" && uv sync --quiet)
  echo "Done. Next: cd $target_dir && make check"
}

main "$@"
