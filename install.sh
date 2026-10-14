#!/bin/sh
set -eu

fail() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

main() {
  if [ "${1-}" = "--help" ] || [ "${1-}" = "-h" ]; then
    printf 'Usage: sh install.sh [destination]\nDefault: ~/.agents/skills/engineering-skills\nInstalls or updates the full bundle from GitHub (master).\n'
    return
  fi
  [ "$#" -le 1 ] || fail 'Expected at most one destination. Use --help for usage.'
  command -v git >/dev/null 2>&1 || fail 'Git is required.'

  repository=https://github.com/igorrendulic/engineering-skills.git
  destination=${1:-"$HOME/.agents/skills/engineering-skills"}
  # Make relative destinations safe even when they begin with a dash.
  case "$destination" in
    /*) ;;
    *) destination="$PWD/$destination" ;;
  esac
  while [ "$destination" != / ]; do
    case "$destination" in
      */) destination=${destination%/} ;;
      */.) destination=${destination%.} ;;
      *) break ;;
    esac
  done

  [ ! -L "$destination" ] || fail "$destination is a symlink. Update its source checkout manually."
  if [ -e "$destination" ]; then
    [ -e "$destination/.git" ] || fail "$destination exists but is not a Git checkout. Choose another destination or move it aside."
    origin=$(git -C "$destination" config --get remote.origin.url) || fail 'The checkout has no origin remote.'
    case "$origin" in
      https://github.com/igorrendulic/engineering-skills|https://github.com/igorrendulic/engineering-skills.git|git@github.com:igorrendulic/engineering-skills.git|ssh://git@github.com/igorrendulic/engineering-skills.git) ;;
      *) fail "$destination belongs to a different repository; expected $repository." ;;
    esac
    [ "$(git -C "$destination" symbolic-ref --quiet --short HEAD)" = master ] || fail 'Updates require the master branch. Switch branches manually when ready.'
    [ -z "$(git -C "$destination" status --porcelain --untracked-files=all)" ] || fail 'The checkout has local changes. Commit or stash them before updating.'
    printf 'Updating %s\n' "$destination"
    git -C "$destination" fetch origin master
    git -C "$destination" merge --ff-only --no-autostash --no-overwrite-ignore FETCH_HEAD
  else
    printf 'Installing into %s\n' "$destination"
    mkdir -p "$(dirname "$destination")"
    git clone --branch master "$repository" "$destination"
  fi
  printf 'Engineering Skills is ready at %s\n' "$destination"
}

# Define the whole operation before running it: updating may replace this file.
main "$@"
