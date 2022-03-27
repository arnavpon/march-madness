
def format_string_for_comparison(text: str) -> str:
    """
    Reformats input string for cleaner COMPARISONS (case insensitive)
    :param text: raw input
    :return: str | formatted output
    """
    return text.lower().strip()

def format_string_for_display(text: str) -> str:
    """
    Reformats input string for cleaner DISPLAY (caps)
    :param text: raw input
    :return: str | formatted output
    """
    return text.strip().upper()