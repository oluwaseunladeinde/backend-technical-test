import os
import django

from .models import UniProtKBEntry
from utils import compress_sequence

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seqfam.settings')
django.setup()


def update_protein_sequences():

    proteins = UniProtKBEntry.objects.all()
    for protein in proteins:

        if protein.sequence:
            compressed_sequence = compress_sequence(protein.sequence)

            protein.sequence = compressed_sequence
            protein.save()


if __name__ == '__main__':
    update_protein_sequences()
