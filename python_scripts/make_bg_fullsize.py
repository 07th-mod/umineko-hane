import re

# matches stralias (stuff) (optional modifier) (path)
stralias_get_modifiers = re.compile(r"(;?\s*stralias\s+[^\"]*\")(:[^;]+;)?(.*)", re.DOTALL)

# only lines containing the following strings will be processed
required_strings_to_perform_replacement = ['background\\']

def getSplitStraliasImageLines(line):
	m = stralias_get_modifiers.match(line)
	if not m:
		return None

	if m:
		return m.groups()

def hasRequiredStrings(line):
	has_strings = False
	for required_string in required_strings_to_perform_replacement:
		if required_string in line:
			has_strings = True
	return has_strings

def addOrReplaceTag(modiferStringOrFalsey, modifierToAdd):
	if not modiferStringOrFalsey:
		modiferStringOrFalsey = ':;'

	strippedModifierString = modiferStringOrFalsey.lstrip(':').rstrip(';')
	if modifierToAdd not in strippedModifierString:
		strippedModifierString = modifierToAdd + strippedModifierString

	return f':{strippedModifierString};'

script = r"../0.utf"
output_script = r"../0.modified.utf"

with open(script, 'r', encoding='utf-8') as script_file:
	all_lines = script_file.readlines()

for i,line in enumerate(all_lines):
	splitLine = getSplitStraliasImageLines(line)
	if not splitLine:
		continue

	if not hasRequiredStrings(line):
		continue

	all_lines[i] = (splitLine[0] + addOrReplaceTag(splitLine[1], 'b') + splitLine[2]).replace('.bmp', '.png')

with open(output_script, 'w', encoding='utf-8') as output_script_file:
	output_script_file.writelines(all_lines)