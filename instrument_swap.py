import argparse
import logging
import mido

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='MIDI Instrument Swap')
    parser.add_argument('--input_file', required=True, type=str, help='MIDI file to have its instruments swapped')
    parser.add_argument('--output_file', required=True, type=str, help='Output file name')
    parser.add_argument('--prog', required=True, type=int, help='New MIDI program number')
    parser.add_argument('--channel', type=int, default=0, help='MIDI channel to have the instruments swapped')

    args = parser.parse_args()
    logger.debug(args)

    # read midi file
    mid = mido.MidiFile(args.input_file, clip=True)

    # swap instruments
    for track in mid.tracks:
        cp = mido.Message('program_change', channel=args.channel, program=args.prog, time=0)
        track.insert(2, cp)

    # save the new midi file
    mid.save(args.output_file)


if __name__ == "__main__":
    main()
