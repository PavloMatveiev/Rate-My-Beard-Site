from django import template

register = template.Library()

@register.simple_tag
def get_page_range(page_obj, max_links=7):
    total_pages = page_obj.paginator.num_pages
    current = page_obj.number
    # If the total number of pages is less than or equal to max_links – return all
    if total_pages <= max_links:
        return range(1, total_pages + 1)
    half = max_links // 2
    if current <= half:
        start = 1
        end = max_links
    elif current > total_pages - half:
        start = total_pages - max_links + 1
        end = total_pages
    else:
        start = current - half
        end = current + half
        if max_links % 2 == 0:
            end -= 1
    return range(start, end + 1)
