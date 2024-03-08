from bokeh.io import show
from bokeh.models import CheckboxGroup, CustomJS

LABELS = ["Option 1", "Option 2", "Option 3"]

checkbox_group = CheckboxGroup(labels=LABELS, active=[0, 1])
checkbox_group.js_on_event('button_click', CustomJS(code="""
    console.log('checkbox_group: active=' + this.origin.active, this.toString())
"""))

show(checkbox_group)
