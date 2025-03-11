import yaml
import argparse
import pdb

class TubaFourCalc:
    def __init__(self):
        self.args = self.parse_arguments()
        self.file_path = self.args.input
        self.two_by_four_length = self.args.length
        self.blade_width = 1 / 8  # Blade width is 1/8 of a unit
        self.data = self.load_yaml()
        self.main()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Load and process a YAML file.')
        parser.add_argument('-i', '--input', type=str, required=True, help='Input YAML file path')
        parser.add_argument('-l', '--length', type=float, required=True, help='Total length of each two-by-four')
        parser.add_argument('-p', '--price', type=float, required=False, help='Price of each two-by-four')
        return parser.parse_args()

    def load_yaml(self):
        with open(self.file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data

    def process_data(self):
        total_length = self.two_by_four_length
        cuts = []

        # Collect all cuts from YAML data
        for board, dimensions in self.data.items():
            length = dimensions['length']
            mult = dimensions['mult']
            cuts.extend([length] * mult)

        # Sort cuts from longest to shortest
        cuts.sort(reverse=True)

        # Calculate number of two-by-fours needed
        num_two_by_fours = 0
        while cuts:
            remaining_length = total_length
            cuts_made = []
            index = 0
            while index < len(cuts):
                cut = cuts[index]
                if cut <= remaining_length:
                    remaining_length -= (cut + self.blade_width)
                    cuts_made.append(cut)
                    cuts.pop(index)
                else:
                    index += 1
            num_two_by_fours += 1
            # Print visual representation of cuts and leftover
            cuts_str = '|'.join(f'{cut}"' for cut in cuts_made)
            print(f"{cuts_str} | leftover: {remaining_length:.2f}\"")

        print(f"\nTotal number of two-by-fours needed: {num_two_by_fours}")
        if self.args.price != None:
            print(f"Total cost: ${num_two_by_fours*self.args.price:.2f}")

    def main(self):
        self.process_data()

if __name__ == '__main__':
    TubaFourCalc()