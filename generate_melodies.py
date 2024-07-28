import argparse
import mido
import os 
import pathlib
from instrument_swap import InstrumentSwapper


def main():
    parser = argparse.ArgumentParser(description='Generate midi files of the same melody for multiple instruments')
    parser.add_argument('input_file', help='list of midi files containing input melodies')
    parser.add_argument('output_dir', help='path of a directory where output files will be stored')
    parser.add_argument('--channel', default=0, help='channel id of the program change message (default: 0)')
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        midi_files = f.read().splitlines(keepends=False)

    # Melodies are generated for instruments ranging from pianos to pipe instruments
    # http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html#BMA1_4 
    for midi_file in midi_files:
        swapper = InstrumentSwapper(midi_file)
        file_path = pathlib.Path(midi_file)
        file_root = file_path.stem

        for prog in range(1, 105):
            new_midi = swapper.swap_instrument(prog, 0)
            print(new_midi)
            output_file = f'{file_root}_{prog:03}.mid'
            new_midi.save(os.path.join(args.output_dir, output_file))


if __name__ == "__main__":
    main()
