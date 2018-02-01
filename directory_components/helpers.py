def add_next(destination_url, current_url):
    if 'next=' in destination_url:
        return destination_url
    concatenation_character = '&' if '?' in destination_url else '?'
    return '{url}{concatenation_character}next={next}'.format(
        url=destination_url,
        concatenation_character=concatenation_character,
        next=current_url,
    )
