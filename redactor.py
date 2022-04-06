import argparse
import glob
import sys
import os

from project1.main import *


def main(args):
    # Getting list of input files
    raw_files = []
    for inp_glob in args.input:
        raw_files += glob.glob(inp_glob)

    # Redacting each file
    final_stats = ""
    for raw_file in raw_files:
        print("Processing", raw_file, "==>")
        data = ""
        try:
            with open(raw_file, 'r') as f:
                data = f.read()
        except:
            print(f"{raw_file} that is given can't be read and so it can't be redacted\n")
            continue
        
        #To count redacted ones
        redact_counts = {}
        #To collect redacted quantities
        redact_list = {}
        
        if args.concept:
            data,concept_list = redact_concept(data,args.concept)
            redact_counts["concept_count"] = len(concept_list)
            redact_list["concept_list"] = concept_list

        if args.address:
            data,address_list = redact_address(data)
            redact_counts["address_count"] = len(address_list)
            redact_list["address_list"] = address_list

        if args.names:
            data, names_list = redact_names(data)
            redact_counts["names_count"] = len(names_list)
            redact_list["names_list"] = names_list

        if args.dates:
            data,dates_list = redact_dates(data)
            redact_counts["dates_count"] = len(dates_list)
            redact_list["dates_list"] = dates_list

        if args.phones:
            data,phones_list = redact_phones(data)
            redact_counts["phones_count"] = len(phones_list)
            redact_list["phones_list"] = phones_list

        if args.genders:
            data,genders_list = redact_genders(data)
            redact_counts["genders_count"] = len(genders_list)
            redact_list["genders_list"] = genders_list
        
        if args.output == 'stdout' or args.output == 'stderr':
            if args.output == 'stdout':
                sys.stdout.write(data)
                sys.stdout.write('\n')
            
            if args.output == 'stderr':
                sys.stderr.write(data)
                sys.stderr.write('\n')
        else:
            write_to_files(raw_file, data)

        stats=redact_stats(args, redact_counts, redact_list)
        final_stats += f"------Data is redacted from {raw_file} file, below is the statistics of the redactions made in file------\n" + stats + "\n\n"

    if args.stats == 'stdout':
        sys.stdout.write("\n-----------Data is redacted from {raw_file} file, below is the statistics of the redactions made in file---------------\n")
        sys.stdout.write(final_stats)
        sys.stdout.write('\n')
    
    if args.stats == 'stderr':
        sys.stdout.write("\n-----------Data is redacted from {raw_file} file, below is the statistics of the redactions made in file---------------\n")
        sys.stderr.write(final_stats)
        sys.stderr.write('\n')
    else:
        write_to_files_stats(args.stats, final_stats)        

        
def write_to_files(raw_file, data):
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    
    out_file_name = '.'.join(raw_file.split('.')[:-1] + ['redacted'])
    sub_folders = out_file_name.split('/')[:-1]
    for sub_folder in sub_folders:
        sub_folder_path = os.path.join(args.output, sub_folder)
        if not os.path.exists(sub_folder_path):
            os.mkdir(sub_folder_path)

    with open(os.path.join(args.output, out_file_name), 'w') as f:
        f.write(data)

    print(f"Saved to {os.path.join(args.output, out_file_name)}")

def write_to_files_stats(raw_file, stats):
    raw_file_path = os.path.join(os.getcwd(), raw_file)

    with open(raw_file_path, 'w') as f:
        f.write(stats)

    print(f"Stats to {raw_file_path}")
    print("\n")

def redact_stats(args, redact_counts, redact_list):
    stats_list = []
    

    if vars(args)['names']:
        stats_list.append(f"In total {redact_counts['names_count']} names got redacted.")
        stats_list.append(f"\tThe names that got redacted are {redact_list['names_list']} ")

    if vars(args)['dates']:
        stats_list.append(f"In total {redact_counts['dates_count']} dates got redacted.")
        stats_list.append(f"\tThe dates that got redacted are {redact_list['dates_list']} ")

    if vars(args)['phones']:
        stats_list.append(f"In total {redact_counts['phones_count']} phone numbers got redacted.")
        stats_list.append(f"\tThe phones that got redacted are {redact_list['phones_list']} ")

    if vars(args)['genders']:
        stats_list.append(f"In total {redact_counts['genders_count']} genders got redacted.")
        stats_list.append(f"\tThe genders that got redacted are {redact_list['genders_list']} ")

    if vars(args)['address']:
        stats_list.append(f"In total {redact_counts['address_count']} address/es got redacted.")
        stats_list.append(f"\tThe address/es that got redacted are {redact_list['address_list']} ")
        
    if vars(args)['concept']:
        stats_list.append(f"In total {redact_counts['concept_count']} concept sentences got redacted.")
        stats_list.append(f"\tThe concept statements that got redacted are {redact_list['concept_list']} ")
    
    return "\n".join(stats_list)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required = True, type = str, action = "append", help='input file is taken through this argument')
    parser.add_argument('--names', action = "store_true", help='names from the input file gets redacted')
    parser.add_argument('--dates', action = "store_true", help='dates from the input files get redacted')
    parser.add_argument('--phones', action = "store_true", help='phone numbers from the input files get redacted')
    parser.add_argument('--genders', action = "store_true", help='gender revealing words from the input files get redacted')
    parser.add_argument('--address', action = "store_true", help='addresses in the input files get redacted')
    parser.add_argument('--concept', type = str, action = "append", help='concept statements in the input files get redacted')
    parser.add_argument('--output',required = True, help='the printing format of input file output  is specified')
    parser.add_argument('--stats', required = True, help='the printing format of input file summary is specified')

    args = parser.parse_args()
    
    
    main(args)
