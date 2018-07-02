------
jinja2
------

This directory serves as an environment for testing Jinja2 templates.

Provide the absolute path of the template file as a constant string in the python file template_render.py assigned to the variable ``TEMPLATE_FILE``.

Provide the data as a dictionary in the same file as ``templateVars``.

Running template_render.py will produce the output of the template when run on the data.

Example:

```
python template_render.py test.tmpl
```
This will work only if you set your ``TEMPLATE_FILE`` and ``templateVars`` correctly.
