from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='read_more')
def read_more(text, cutoff=500):
    try:
        cutoff = int(cutoff)
    except (ValueError, TypeError):
        cutoff = 500
    if not text:
        return ""
    if len(text) <= cutoff:
       # Replace line breaks with <br> (if required)
        return text.replace('\n', '<br>')
    else:
        visible = text[:cutoff]
        hidden = text[cutoff:]
        html = (
            f"{visible}"
            f'<span class="more-text" style="display:none;">{hidden}</span> '
            f'<a href="#" class="read-more-link">more</a>'
        )
        return mark_safe(html)
