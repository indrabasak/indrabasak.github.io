# This python program parses an inventory YAML file
# an turns them into a list of markdown pages.

# To use this program, you need to install pyyaml by executing
# the following command:
# pip install pyyaml
# or
# pip3 install pyyaml

import os
from glob import glob
from operator import itemgetter

import yaml


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
        file_out.write("    issuer: " + str(item["issuer"]) + "\n")
    if "image" in item.keys():
        file_out.write("    image: " + item["image"] + "\n")
    if "note" in item.keys():
        notes = item["note"]
        file_out.write("    note: \n")
        for note in notes:
            # file_out.write("    note: " + item["note"] + "\n")
            file_out.write("      - " + note + "\n")


def print_page(category, home, items, start_index, end_index, index, file_out):
    file_out.write("---\n")
    file_out.write("layout: inventory-template\n")
    if start_index == end_index - 1:
        file_out.write(
            "title: " + category + " ~ " + items[start_index]["name"][
                                           :2] + "\n")
    else:
        file_out.write(
            "title: " + category + " ~ " + items[start_index]["name"][
                                           :2] + " - " + items[end_index - 1][
                                                             "name"][:2] + "\n")
    file_out.write("index: " + str(index) + "\n")
    file_out.write("category: " + category + "\n")
    file_out.write("home: " + home + "\n")
    file_out.write("items:\n")

    i = start_index
    while i < end_index:
        print_item(category, items[i], file_out)
        i = i + 1
    file_out.write("---\n")


def delete_pages(location):
    for f in glob(location + "/*.md"):
        os.unlink(f)


def create_pages(inventory_file, inventory_pages_location, partition_length, home):
    with open(inventory_file, 'r') as stream:
        delete_pages(inventory_pages_location)
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
                partition_count = count // partition_length + (0 if count % partition_length == 0 else 1)

                i = 0
                end_index = 0
                while i < partition_count:
                    start_index = end_index
                    if (end_index + partition_length) < count:
                        end_index = end_index + partition_length
                    else:
                        end_index = count

                    page_name = inventory_pages_location + "/page" + str(global_page_index) + ".md"
                    file_out = open(page_name, "w")
                    print_page(category, home, sorted_items, start_index, end_index, global_page_index, file_out)
                    file_out.close()
                    i = i + 1
                    global_page_index = global_page_index + 1
        except yaml.YAMLError as exc:
            print(exc)
