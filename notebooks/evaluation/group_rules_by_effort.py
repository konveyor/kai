# This is a script used to group rules by effort

import yaml
import os

def group_rules_by_effort(ifile, odir):
    with open(ifile, 'r') as file: data = yaml.safe_load(file)
    grouped_data = {}
    for rule in data:
        effort = rule.get('effort', 0)
        if effort not in grouped_data:
            grouped_data[effort] = []
        grouped_data[effort].append(rule)
    
    if not os.path.exists(odir): os.makedirs(odir)

    
    for effort, objects in grouped_data.items():
        output_file = os.path.join(odir, f"{effort}.yaml")
        print(f"dumping to {output_file}")
        with open(output_file, 'w') as file: yaml.dump(objects, file)

if __name__ == "__main__":
    # replace following path with rules in your path
    input_directory = '/home/pranav/Projects/rulesets/default/generated/quarkus/'
    output_base_directory = './data/rules/'

    for input_file in os.listdir(input_directory):
        print(f"working with {input_file}")
        if input_file.endswith('.yaml') and 'ruleset.yaml' not in input_file:
            input_file_path = os.path.join(input_directory, input_file)
            output_dir = os.path.join(output_base_directory, os.path.splitext(input_file)[0])
            group_rules_by_effort(input_file_path, output_dir)