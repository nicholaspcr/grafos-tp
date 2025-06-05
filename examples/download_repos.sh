#!/usr/bin/env bash

function split() {
  IFS='/' read -ra RES <<< "$1"
  echo "${RES[@]}"
}

repos=(
  "spf13/cobra"
  "charmbracelet/huh"
  "charmbracelet/pop"
  "charmbracelet/bubbletea"
  "charmbracelet/wish"
  "charmbracelet/lipgloss"
  "charmbracelet/glamour"
  "charmbracelet/bubbles"
  "charmbracelet/log"
  "charmbracelet/harmonica"
  "charmbracelet/mods"
  "charmbracelet/gum"
  "charmbracelet/glow"
  "charmbracelet/skate"
  "twitchdev/twitch-cli"
  "jroimartin/gocui"
  "cosiner/argv"
  "posener/cmd"
  "maypok86/otter"
  "gotk3/gotk3"
  "webview/webview_go"
  "SimonWaldherr/golang-benchmarks"
)

for repoPath in "${repos[@]}" ; do
  if ! [ -d ".$repoPath" ]; then
    # shellcheck disable=SC2207
    repo=($(split "$repoPath"))
    echo "Downloading $repoPath"
    git clone --quiet "https://github.com/${repo[0]}/${repo[1]}.git" ".${repo[0]}_${repo[1]}" &
  fi
done

wait
