#!/bin/bash

SF2_FONTS='"/home/wojtekk23/Dokumenty/lmms/samples/soundfonts/GeneralUser GS SoftSynth v1.44/GeneralUser GS SoftSynth v1.44.sf2"'
GAIN=0.8
INPUT_DIR=$1
OUTPUT_DIR=$2

mkdir -p $OUTPUT_DIR

process_file() {
  f="$1"
  filename=$(basename "$f")
  output_file="$OUTPUT_DIR/${filename%*.mid}.wav"

  #fluidsynth -g $GAIN "$SF2_FONTS" -F $output_file -q $f
  timidity "$f" --quiet -x "soundfont $SF2_FONTS" -s 22050 --output-mode=wMsl -o "$output_file"
}

export -f process_file
export SF2_FONTS
export OUTPUT_DIR

find "$INPUT_DIR" -name '*.mid' | parallel -j 4 process_file
