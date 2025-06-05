#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ -d ".out" ]; then
  rm -r ".out"
fi

main_dir=$PWD

for dir in */ .[^.]*/; do
  if ! [ -d "$main_dir/.out" ]; then
      mkdir ".out"
      cd ".out" || return 1
  fi

  python "${SCRIPT_DIR}/../main.py" "$main_dir/$dir" &
done

wait
echo "Done"
