from django import template

register = template.Library()

def truncatelines(value, arg) :
    if value == None or value == "" :
        return ""
    try :
        lines = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
    line_list = value.rstrip().split('\n')[:lines]
    result = ""
    for line in line_list :
        result += line + "\n"
    result = result.rstrip()
    return result

register.filter('truncatelines', truncatelines)
