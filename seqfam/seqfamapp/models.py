from django.db import models
from .utils import compress_sequence, decompress_sequence


class UniProtKBEntry(models.Model):
    accession = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    reviewed = models.BooleanField()
    sequence = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.sequence:
            self.sequence = compress_sequence(self.sequence)
            super(UniProtKBEntry, self).save(*args, **kwargs)

    @property
    def sequence_length(self):
        return len(decompress_sequence(self.sequence))


class InterProEntry(models.Model):
    accession = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PfamEntry(models.Model):
    accession = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    interpro_entry = models.ForeignKey(InterProEntry, null=True,
                                       on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class PfamMatch(models.Model):
    protein = models.ForeignKey(UniProtKBEntry, on_delete=models.CASCADE)
    model = models.ForeignKey(PfamEntry, on_delete=models.CASCADE)
    start = models.IntegerField()
    stop = models.IntegerField()
