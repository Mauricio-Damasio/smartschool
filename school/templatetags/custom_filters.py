from django import template

register = template.Library()



# get_item

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
  



@register.simple_tag
def get_status(status_dict, turma_id, disciplina_id, trimestre):
    chave = (int(turma_id), int(disciplina_id), int(trimestre))
    return status_dict.get(chave, False)

  
# getattr
  
@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, '')





# split

@register.filter
def split(value, arg):
    return value.split(arg)


# int

@register.filter
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

@register.filter
def dict_get(d, key):
    return d.get(key, False)