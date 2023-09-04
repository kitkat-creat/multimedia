
import csv
import argparse

# Function to parse Baselight file and generate output rows
def process_baselight_file(baselight_file_location, xytech_folders):
    output_rows = []
    with open(baselight_file_location, "r") as read_baselight_file:
        for line in read_baselight_file:
            line_parse = line.split(" ")
            current_folder = line_parse.pop(0)
            sub_folder = current_folder.replace("/images1/starwars", "")
            new_location = ""

            for xytech_line in xytech_folders:
                if sub_folder in xytech_line:
                    new_location = xytech_line.strip()

            first = ""
            pointer = ""
            last = ""

            for numeral in line_parse:
                if not numeral.strip().isnumeric():
                    continue

                if first == "":
                    first = int(numeral)
                    pointer = first
                    continue

                if int(numeral) == (pointer + 1):
                    pointer = int(numeral)
                    continue
                else:
                    last = pointer
                    if first == last:
                        output_rows.append([new_location, str(first)])
                    else:
                        output_rows.append([new_location, f"{first}-{last}"])
                    first = int(numeral)
                    pointer = first
                    last = ""

            last = pointer
            if first != "":
                if first == last:
                    output_rows.append([new_location, str(first)])
                else:
                    output_rows.append([new_location, f"{first}-{last}"])
    
    return output_rows

# Main function to handle command-line arguments and write to CSV
def main():
    parser = argparse.ArgumentParser(description="Process Baselight and Xytech files and write to CSV")
    parser.add_argument("--xytech", required=True, help="Path to Xytech file")
    parser.add_argument("--baselight", required=True, help="Path to Baselight file")
    parser.add_argument("--output", required=True, help="Path to the output CSV file")

    args = parser.parse_args()

    xytech_file_location = args.xytech
    baselight_file_location = args.baselight
    output_csv_file = args.output

    xytech_folders = []

    with open(xytech_file_location, "r") as read_xytech_file:
        for line in read_xytech_file:
            if "/" in line:
                xytech_folders.append(line.strip())

    output_rows = process_baselight_file(baselight_file_location, xytech_folders)

    with open(output_csv_file, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Location", "Range"])
        csv_writer.writerows(output_rows)

    print(f"Data has been written to {output_csv_file}")

if __name__ == "__main__":
    main()


# to run: python project1.py --xytech Xytech.txt --baselight Baselight_export.txt --output output.csv

