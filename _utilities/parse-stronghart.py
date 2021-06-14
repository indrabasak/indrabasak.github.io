# This python program parses an inventory YAML file
# an turns them into a list of markdown pages.

# To use this program, you need to install pyyaml by executing
# the following command:
# pip install pyyaml
# or
# pip3 install pyyaml

from common import create_pages

INVENTORY_YAML_FILE = "../_data/stronghart.yml"
INVENTORY_PAGES_LOCATION = "../_stronghart"
PARTITION_LENGTH = 10

create_pages(INVENTORY_YAML_FILE, INVENTORY_PAGES_LOCATION, PARTITION_LENGTH)