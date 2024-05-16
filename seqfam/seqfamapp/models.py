from django.db import models


class UniProtKBEntry(models.Model):
    accession = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    reviewed = models.BooleanField()
    sequence = models.TextField()


class InterProEntry(models.Model):
    accession = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)


class PfamEntry(models.Model):
    accession = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    interpro_entry = models.ForeignKey(InterProEntry, null=True,
                                       on_delete=models.SET_NULL)


class PfamMatch(models.Model):
    protein = models.ForeignKey(UniProtKBEntry, on_delete=models.CASCADE)
    model = models.ForeignKey(PfamEntry, on_delete=models.CASCADE)
    start = models.IntegerField()
    stop = models.IntegerField()
