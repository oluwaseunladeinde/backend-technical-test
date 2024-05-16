from django.shortcuts import render
from rest_framework import viewsets

from .models import UniProtKBEntry, InterProEntry, PfamEntry
from .serializers import SequenceSerializer, InterProSerializer, PfamSerializer


class SequenceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UniProtKBEntry.objects.all()
    serializer_class = SequenceSerializer


class InterProViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InterProEntry.objects.all()
    serializer_class = InterProSerializer


class PfamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PfamEntry.objects.all()
    serializer_class = PfamSerializer


def interpro_list(request):
    context = {"page_title": "InterPro"}
    return render(request, "list.html", context)


def pfam_list(request):
    context = {"page_title": "Pfam"}
    return render(request, "list.html", context)


def uniprot_list(request):
    context = {"page_title": "Proteins"}
    return render(request, "list.html", context)
