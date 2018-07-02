The file parse.py contained within this directory uses textfsm to parse a text file according to a template file.

The subdirectory 'examples' contains templates and text files. Text files are to be parsed with corresponding template files.
Text files have names containing the phrase 'result'. Template files have names containing the phrase 'template'. 

Run with the following command:

python parse.py <template> <text>

Here <template> refers to a template file used for parsing and <text> refers to a text file to be parsed.
The output is a list of lists. The first list contains the column headers.

Example command:

python parse.py examples/template examples/result

