import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InterProEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UniProtKBEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('reviewed', models.BooleanField()),
                ('sequence', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PfamEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('interpro_entry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seqfamapp.interproentry')),
            ],
        ),
        migrations.CreateModel(
            name='PfamMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.IntegerField()),
                ('stop', models.IntegerField()),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seqfamapp.pfamentry')),
                ('protein', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seqfamapp.uniprotkbentry')),
            ],
        ),
    ]
