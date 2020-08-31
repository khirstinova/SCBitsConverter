from django.shortcuts import render


def render_bioerosion_page(request, template_name, context=None, content_type=None, status=None, using=None):
    return render(request, template_name, context=context, content_type=content_type, status=status, using=using)
