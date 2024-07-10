#!/bin/sh

# for each .yaml file in the directory, generate a .py file with the same name
for f in *.yaml; do
	datamodel-codegen --input "${f}" --input-file-type jsonschema --output "${f%.*}".py
done
