#!/bin/bash
# ask.sh - plain English in, Linux command out, confirm, run, interpret.
# Usage:  ./ask.sh how much disk space is free

MODEL="llama3.2:3b"
REQUEST="$*"

# Find ollama even on a tarball (no-sudo) install, and start the server
# if it is not already running.
if ! command -v ollama > /dev/null && [ -x "$HOME/ollama-demo/bin/ollama" ]; then
  export PATH="$HOME/ollama-demo/bin:$PATH"
  export OLLAMA_MODELS="$HOME/ollama-demo/models"
fi
if ! curl -s --max-time 2 http://localhost:11434/ > /dev/null; then
  echo "(starting ollama server...)"
  nohup ollama serve > /dev/null 2>&1 &
  sleep 3
fi

CONTEXT='You translate a plain-English request into exactly one safe,
common Linux command. Reply with ONLY two lines: the command, then a
"# comment" explaining it. No markdown, no backticks, no other text.
Only use real Linux commands. Examples:

Request: where am I
pwd
# prints the folder you are currently in

Request: show hidden files too
ls -a
# lists all files, including hidden ones

Request: who am I logged in as
whoami
# prints your username

Request: make a folder called notes
mkdir notes
# creates a new folder named notes'

ANSWER=$(ollama run "$MODEL" "$CONTEXT

Request: $REQUEST" < /dev/null | sed 's/```//g' | sed '/^$/d')

echo ""
echo "$ANSWER"
echo ""

CMD=$(echo "$ANSWER" | head -1)
if echo "$CMD" | grep -qE '\brm\b|\bdd\b|mkfs|\bshutdown\b|\breboot\b'; then
  echo "!! careful: this command deletes data or stops the machine"
fi

read -p "Run it? [y/N] " OK
[ "$OK" = "y" ] || exit 0

echo ""
echo "\$ $CMD"
OUTPUT=$(bash -c "$CMD" 2>&1 | head -20)
echo "$OUTPUT"
echo ""

ollama run "$MODEL" "In two short sentences, interpret this output of
the command '$CMD' for a beginner:

$OUTPUT" < /dev/null
