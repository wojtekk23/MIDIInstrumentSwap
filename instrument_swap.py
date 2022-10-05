import argparse
import logging
import mido

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)


class InstrumentSwapper:
    def __init__(self, input_file: str):
        self.mid = mido.MidiFile(input_file, clip=True)

    def swap_instrument(self, prog: int, channel: int) -> mido.MidiFile:
        new_midi = mido.MidiFile(
            type=self.mid.type,
            ticks_per_beat=self.mid.ticks_per_beat,
            charset=self.mid.charset,
            debug=self.mid.debug,
            clip=self.mid.clip,
            tracks=[track.copy() for track in self.mid.tracks]
        )
        for track in new_midi.tracks:
            cp = mido.Message(
                'program_change',
                channel=channel,
                program=prog,
                time=0
            )
            track.insert(2, cp)

        return new_midi


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='MIDI Instrument Swap')
    parser.add_argument('--input_file', required=True, type=str, help='MIDI file to have its instruments swapped')
    parser.add_argument('--output_file', required=True, type=str, help='Output file name')
    parser.add_argument('--prog', required=True, type=int, help='New MIDI program number')
    parser.add_argument('--channel', type=int, default=0, help='MIDI channel to have the instruments swapped')

    args = parser.parse_args()
    logger.debug(args)

    swapper = InstrumentSwapper(args.input_file)
    mid = swapper.swap_instrument(args.prog, args.channel)
    mid.save(args.output_file)


if __name__ == "__main__":
    main()
