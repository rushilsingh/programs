import jinja2
import json

# We load templates off the filesystem.
# For thsi, we construct a FileSystemLoader object.

# The search path can be used to make finding templates by
# relative paths easier.  

templateLoader = jinja2.FileSystemLoader( searchpath="/" )

# An environment provides the data necessary to read and
# parse our templates.  We pass in the loader object here.

templateEnv = jinja2.Environment( loader=templateLoader )

def to_json(value, **kw):
    '''
    `to_json(value, indent=None)`

    Serialize obj to a JSON formatted str.

    If `indent` is a non-negative integer, then JSON array elements and object members will be pretty-printed
    with that indent level. An indent level of 0, or negative, will only insert newlines.
    `None` (the default) selects the most compact representation.
    '''
    return json.dumps(value, **kw)

templateEnv.filters['to_json'] = to_json


# This constant string specifies the template file we will use.
TEMPLATE_FILE = "/home/username/programs/jinja2/test.tmpl"

# Read the template file using the environment object.
# This also constructs our Template object.
template = templateEnv.get_template( TEMPLATE_FILE )

# Specify any input variables to the template as a dictionary.
templateVars = {
    "properties": {
         "0": "something",
        "id": "xxxxxx",  
        "boolean": True,
        "addresses": [{
            "networkID": "123"
        }, 
        {   
            "networkID": "345"  
        }]
    }
}
# Finally, process the template to produce our final text.
outputText = template.render( templateVars )
print outputText
