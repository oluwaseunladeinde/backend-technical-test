import gzip
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from seqfamapp.models import UniProtKBEntry, InterProEntry, PfamEntry, PfamMatch


class Command(BaseCommand):
    help = "Insert data into the database"

    def handle(self, *args, **options):
        filepath = Path(__file__).resolve().parent / "data.json.gz"
        with gzip.open(filepath, "rt") as fh:
            data = json.load(fh)

        objs = []
        for info in data["proteins"]:
            objs.append(UniProtKBEntry(**info))

        proteins = {}
        for obj in UniProtKBEntry.objects.bulk_create(objs):
            proteins[obj.accession] = obj

        self.stdout.write(
            self.style.SUCCESS(f"Inserted {len(proteins)} proteins")
        )

        objs = []
        for info in data["interpro"]:
            objs.append(InterProEntry(**info))

        interpro = {}
        for obj in InterProEntry.objects.bulk_create(objs):
            interpro[obj.accession] = obj

        self.stdout.write(
            self.style.SUCCESS(f"Inserted {len(interpro)} InterPro entries")
        )

        objs = []
        for info in data["pfam"]:
            interpro_accession = info["interpro"]
            if interpro_accession is not None:
                interpro_entry = interpro[interpro_accession]
            else:
                interpro_entry = None

            objs.append(PfamEntry(accession=info["accession"],
                                  name=info["name"],
                                  description=info["description"],
                                  interpro_entry=interpro_entry))

        pfam = {}
        for obj in PfamEntry.objects.bulk_create(objs):
            pfam[obj.accession] = obj

        self.stdout.write(
            self.style.SUCCESS(f"Inserted {len(interpro)} Pfam entries")
        )

        objs = []
        for info in data["matches"]:
            protein_accession = info["uniprot_acc"]
            pfam_accession = info["pfam_acc"]
            objs.append(PfamMatch(protein=proteins[protein_accession],
                                  model=pfam[pfam_accession],
                                  start=info["start"],
                                  stop=info["stop"]))

        n = len(PfamMatch.objects.bulk_create(objs))

        self.stdout.write(
            self.style.SUCCESS(f"Inserted {n} Pfam matches")
        )
