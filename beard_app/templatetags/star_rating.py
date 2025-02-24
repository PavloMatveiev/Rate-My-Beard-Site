from django import template
import math

register = template.Library()

@register.filter
def star_rating(value):
    try:
        rating = float(value)
    except (ValueError, TypeError):
        rating = 0
    # Round to the nearest 0.5
    rounded = round(rating * 2) / 2
    full_stars = int(math.floor(rounded))
    half_star = 1 if (rounded - full_stars) == 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    stars_html = ''
    stars_html += '<i class="fas fa-star"></i> ' * full_stars
    if half_star:
        stars_html += '<i class="fas fa-star-half-alt"></i> '
    stars_html += '<i class="far fa-star"></i> ' * empty_stars
    return stars_html