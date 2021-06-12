# This python program parses an inventory YAML file
# an turns them into a list of markdown pages.

# To use this program, you need to install pyyaml by executing
# the following command:
# pip install pyyaml
# or
# pip3 install pyyaml

import yaml
from operator import itemgetter
import os
from glob import glob

INVENTORY_YAML_FILE = "../_data/banthrico.yml"
INVENTORY_PAGES_LOCATION = "../_banthrico"
PARTITION_LENGTH = 5

def print_item(category, item, file_out):
    file_out.write("  - name: " + item["name"] + "\n")
    file_out.write("    category: " + category + "\n")
    if "manufacturer" in item.keys():
        file_out.write("    manufacturer: " + item["manufacturer"] + "\n")
    if "material" in item.keys():
        file_out.write("    material: " + item["material"] + "\n")
    if "year" in item.keys():
        file_out.write("    year: " + str(item["year"]) + "\n")
    if "issuer" in item.keys():
        file_out.write("    issuer: " + item["issuer"] + "\n")
    if "image" in item.keys():
        file_out.write("    image: " + item["image"] + "\n")
    if "note" in item.keys():
        file_out.write("    note: " + item["note"] + "\n")


def print_page(category, items, start_index, end_index, index, file_out):
    file_out.write("---\n")
    file_out.write("layout: inventory-template\n")
    if start_index == end_index - 1:
        file_out.write("title: " + category + " ~ " + items[start_index]["name"][:2] + "\n")
    else:
        file_out.write("title: " + category + " ~ " + items[start_index]["name"][:2] + " - " + items[end_index - 1]["name"][:2] + "\n")
    file_out.write("index: " + str(index) + "\n")
    file_out.write("category: " + category + "\n")
    file_out.write("items:\n")

    i = start_index
    while i < end_index:
        print_item(category, items[i], file_out)
        i = i + 1
    file_out.write("---\n")


def delete_pages():
    for f in glob(INVENTORY_PAGES_LOCATION + "/*.md"):
        os.unlink(f)


with open(INVENTORY_YAML_FILE, 'r') as stream:
    delete_pages()
    try:
        # read the inventory YAML file
        data_loaded = yaml.safe_load(stream)
        list = data_loaded["list"]
        global_page_index = 1
        for entry in list:
            category = entry["category"]
            items = entry["items"]
            sorted_items = sorted(items, key=itemgetter('name'))

            count = len(sorted_items)
            partition_count = count // PARTITION_LENGTH + (0 if count % PARTITION_LENGTH == 0 else 1)

            i = 0
            start_index = 0
            end_index = 0
            while i < partition_count:
                start_index = end_index
                if (end_index + PARTITION_LENGTH) < count:
                    end_index = end_index + PARTITION_LENGTH
                else:
                    end_index = count

                page_name = INVENTORY_PAGES_LOCATION +  "/page" + str(global_page_index) + ".md"
                file_out = open(page_name, "w")
                print_page(category, sorted_items, start_index, end_index, global_page_index, file_out)
                file_out.close()
                i = i + 1
                global_page_index = global_page_index + 1
    except yaml.YAMLError as exc:
        print(exc)