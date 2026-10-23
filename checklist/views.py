from django.shortcuts import render

from .models import Section


def checklist(request):
    """The single public page: every section with its tickable options."""
    sections = Section.objects.prefetch_related("items").all()
    return render(request, "checklist/checklist.html", {"sections": sections})
