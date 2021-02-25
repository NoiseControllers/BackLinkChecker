def clear_url(url: str) -> str:
    remove_words = ["http://", "https://", "www."]
    url = url

    for word in remove_words:
        url = url.replace(word, "")

    last_character = url[-1]

    if last_character == "/":
        url = url[:-1]

    return url
