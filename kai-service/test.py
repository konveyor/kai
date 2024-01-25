#!/usr/bin/env python

import yaml

with open("kai.conf", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

solved_example = "foo"
original_source = "bar"

print(config['model_templates']['alpaca'].format(solved_example=solved_example, original_source=original_source))
