from rest_framework import serializers
from .models import UniProtKBEntry, InterProEntry, PfamEntry, PfamMatch


class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniProtKBEntry
        fields = '__all__'


class InterProSerializer(serializers.ModelSerializer):
    protein_count = serializers.SerializerMethodField()

    class Meta:
        model = InterProEntry
        fields = '__all__'

    def get_protein_count(self, obj):
        proteins = 0
        for pfam in PfamEntry.objects.filter(interpro_entry=obj):
            for match in PfamMatch.objects.filter(model=pfam):
                proteins += 1

        return proteins


class PfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PfamEntry
        fields = '__all__'
