# Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.


import glob
import sys
import json
import os
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--scraped_path", type=str, default=".",
        help="path where all the json files and data files are located")

    parser.add_argument("--output_file", type=str, default="merged_output_and_data.json",
        help="filename where the merged json should go")

    args = parser.parse_args()

    scraped_path = args.scraped_path
    out_file = args.output_file

    json_files = glob.glob(scraped_path + '/meta/*.json')

    counter = 0

    with open(out_file, 'w') as outfile:
        for fname in json_files:
            counter += 1

            if counter % 1024 == 0:
                print("Merging at ", counter, flush=True)

            name = os.path.split(fname)[1].split('.')[0]
            data_file = scraped_path + '/data/' + name+ '.txt'
            with open(fname, 'r') as infile:
                for jsonrow in infile:
                    each_row = json.loads(jsonrow)
                    with open(data_file, 'r') as datafile:
                        for txtrow in datafile:
                            url_json = {}
                            url_json["txt"] = txtrow
                            url_json["url"] = each_row["url"]
                            json.dump(url_json, outfile)
                            outfile.write('\n')


    print("Merged file", out_file, flush=True)

