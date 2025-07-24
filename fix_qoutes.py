# jotform_calendar_tool/scripts/fix_quotes.py
import argparse

def fix_unmatched_quotes(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as src, \
         open(output_path, 'w', encoding='utf-8') as dst:

        buffer = ''
        quote_count = 0
        line_num = 0

        for line in src:
            line_num += 1
            buffer += line
            quote_count += line.count('"')

            if quote_count % 2 == 0:
                dst.write(buffer)
                buffer = ''
                quote_count = 0

        if buffer:
            print(" Qoutes/Commas are bad, c.")
            dst.write(buffer)

    print(f" Fixed quotes saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Fix mismatched quotes in CSV")
    parser.add_argument("-i", "--input", required=True, help="Input raw CSV path")
    parser.add_argument("-o", "--output", required=True, help="Output fixed CSV path")
    args = parser.parse_args()

    fix_unmatched_quotes(args.input, args.output)

if __name__ == "__main__":
    main()
