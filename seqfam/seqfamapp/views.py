from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from collections import defaultdict

from .models import UniProtKBEntry, InterProEntry, PfamEntry, PfamMatch
from .serializers import UniProtKBSerializer, InterProSerializer, PfamSerializer


class UniProtKBViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UniProtKBEntry.objects.all().order_by('id')
    serializer_class = UniProtKBSerializer


class InterProViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InterProEntry.objects.all().order_by('id')
    serializer_class = InterProSerializer
    lookup_field = "accession"

    def retrieve(self, request, accession=None):
        # entry = super().retrieve(request, accession).data
        interpro_entry = self.get_object()
        data = {
            "accession": interpro_entry.accession,
            "name": interpro_entry.name,
            "description": interpro_entry.description,
            "pfam": PfamEntry.objects.filter(interpro_entry=interpro_entry).values_list('accession', flat=True),
            "uniprot": self.get_unique_protein(interpro_entry),
        }

        return Response(data)

    def get_unique_protein(self, entry):
        # list of the unique uniprotkb entry accessions
        protein_set = []
        for match in PfamMatch.objects.filter(model__interpro_entry=entry):
            pfam = PfamEntry.objects.get(pk=match.model.pk)
            if pfam and pfam.interpro_entry is not None:
                uniprot = UniProtKBEntry.objects.get(pk=match.protein.pk)
                protein_set.append(uniprot.accession)
            else:
                print(
                    "This protein entry is not attached to an interpro entry via a pfam entry", pfam.accession)

        proteins = list(set(protein_set))
        return proteins


class PfamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PfamEntry.objects.all().order_by('id')
    serializer_class = PfamSerializer


class CompressExistingDBSequencesView(APIView):
    def get(self, request):
        items_count = 0
        try:
            # Retrieve InterProEntry object by accessor
            for entry in UniProtKBEntry.objects.all():
                entry.save()
                items_count += 1
            return Response({
                "items_count": items_count,
                "message": "All sequences have been compressed successfully"
            }, status=status.HTTP_200_OK)
        except UniProtKBEntry.DoesNotExist:
            # Handle case where entry is not found
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'No UniprotKB Entry was found'})


def interpro_list(request):
    context = {"page_title": "InterPro"}
    return render(request, "list.html", context)


def pfam_list(request):
    context = {"page_title": "Pfam"}
    return render(request, "list.html", context)


def uniprot_list(request):
    context = {"page_title": "Proteins"}
    return render(request, "list.html", context)
