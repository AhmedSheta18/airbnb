from .models import Settings


def footer_context(request):
    """
    Context processor to add settings to the footer.
    """
    my_footer = Settings.objects.last() if Settings.objects.exists() else None
    return {
        'my_footer': my_footer,}