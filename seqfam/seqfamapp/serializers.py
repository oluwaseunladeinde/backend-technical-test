from rest_framework import serializers
from .models import UniProtKBEntry, InterProEntry, PfamEntry, PfamMatch
from collections import defaultdict


class UniProtKBSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniProtKBEntry
        fields = ["id", "name", "accession", "sequence_length"]


class InterProSerializer(serializers.ModelSerializer):
    protein_count = serializers.SerializerMethodField()
    protein_count_old = serializers.SerializerMethodField()
    unique_protein_count = serializers.SerializerMethodField()

    class Meta:
        model = InterProEntry
        fields = '__all__'

    def get_protein_count(self, obj):

        pfam = PfamEntry.objects.filter(interpro_entry=obj)[0]
        protein_set = defaultdict(set)
        for match in PfamMatch.objects.filter(model=pfam):
            protein_set[match.protein].add(match)
        # Count the total unique proteins
        proteins = sum(len(match) for match in protein_set.values())
        return proteins

    def get_protein_count_old(self, obj):
        proteins = 0
        for pfam in PfamEntry.objects.filter(interpro_entry=obj):
            for match in PfamMatch.objects.filter(model=pfam):
                proteins += 1
        return proteins

    def get_unique_protein_count(self, obj):
        proteins = 0
        for match in PfamMatch.objects.filter(model__interpro_entry=obj):
            pfam = PfamEntry.objects.get(pk=match.model.pk)
            if pfam and pfam.interpro_entry is not None:
                proteins += 1
            else:
                print(
                    "This protein entry is not attached to an interpro entry via a pfam entry", pfam.accession)

            return proteins


class PfamSerializer(serializers.ModelSerializer):

    interpro = serializers.CharField(
        source='interpro_entry.accession', read_only=True)

    class Meta:
        model = PfamEntry
        fields = ["id", "accession", "name", "description", "interpro"]
