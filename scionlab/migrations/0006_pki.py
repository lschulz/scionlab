# Generated by Django 2.2.8 on 2020-03-09 08:56

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.encoder
import jsonfield.fields
import scionlab.models.pki


def reset_pki(apps, schema_editor):
    """
    Previously, we had stored keys, certs and TRCs directly as string fields of the AS and ISD
    objects. Now they are standalone objects, and these string fields have been removed.

    Here we just create new keys and certs. There is no need to migrate any information, as the
    previous CPPKI is incompatible anyway.
    """
    # Note: we use the _current_ model logic, not the "historical" migration models.
    #
    # From https://docs.djangoproject.com/en/2.2/topics/migrations/#historical-models
    #  > If you import models directly rather than using the historical models, your migrations may
    #  > work initially but will fail in the future when you try to re-run old migrations (commonly,
    #  > when you set up a new installation and run through all the migrations to set up the DB).
    #
    # The logic for creating keys, TRCs and certificates is all implemented on models or model
    # managers. Even though the steps for recreating the PKI from scratch are not overly complicated
    # (it just requires to create things in the right order), it's complicated enough that I don't
    # want a completely separate implementation on the "historical" models.
    #
    # As this code is a no-op on an empty database, I hope we avoid the trap described above.
    # If you're reading this because this caused issues: sorry! Advice, from the same source:
    #
    #  > If you run into this kind of failure, it’s OK to edit the migration to use the historical
    #  > models rather than direct imports and commit those changes.

    from scionlab.models.core import AS, ISD
    for as_ in AS.objects.all():
        as_.init_keys()
    for isd in ISD.objects.all():
        isd.update_trc_and_certificates()


class Migration(migrations.Migration):

    dependencies = [
        ('scionlab', '0005_monolith'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='as',
            name='certificate_chain',
        ),
        migrations.RemoveField(
            model_name='as',
            name='core_certificate',
        ),
        migrations.RemoveField(
            model_name='as',
            name='core_offline_priv_key',
        ),
        migrations.RemoveField(
            model_name='as',
            name='core_offline_pub_key',
        ),
        migrations.RemoveField(
            model_name='as',
            name='core_online_priv_key',
        ),
        migrations.RemoveField(
            model_name='as',
            name='core_online_pub_key',
        ),
        migrations.RemoveField(
            model_name='as',
            name='core_sig_priv_key',
        ),
        migrations.RemoveField(
            model_name='as',
            name='core_sig_pub_key',
        ),
        migrations.RemoveField(
            model_name='as',
            name='enc_priv_key',
        ),
        migrations.RemoveField(
            model_name='as',
            name='enc_pub_key',
        ),
        migrations.RemoveField(
            model_name='as',
            name='sig_priv_key',
        ),
        migrations.RemoveField(
            model_name='as',
            name='sig_pub_key',
        ),
        migrations.RemoveField(
            model_name='isd',
            name='trc',
        ),
        migrations.RemoveField(
            model_name='isd',
            name='trc_priv_keys',
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_as_id_int', models.BigIntegerField(editable=False, help_text='Copy of AS.as_id_int.')),
                ('usage', models.CharField(choices=[('as-decrypt', 'as-decrypt'), ('as-signing', 'as-signing'), ('as-cert-signing', 'as-cert-signing'), ('trc-issuing-grant', 'trc-issuing-grant'), ('trc-voting-online', 'trc-voting-online'), ('trc-voting-offline', 'trc-voting-offline')], editable=False, max_length=16)),
                ('version', models.PositiveIntegerField(editable=False)),
                ('not_before', models.DateTimeField()),
                ('not_after', models.DateTimeField()),
                ('key', models.CharField(editable=False, max_length=255)),
                ('AS', models.ForeignKey(editable=False, null=True, on_delete=scionlab.models.pki._key_set_null_or_cascade, related_name='keys', to='scionlab.AS')),
            ],
            options={
                'unique_together': {('AS', 'usage', 'version')},
            },
        ),
        migrations.CreateModel(
            name='TRC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.PositiveIntegerField(editable=False)),
                ('not_before', models.DateTimeField()),
                ('not_after', models.DateTimeField()),
                ('trc', jsonfield.fields.JSONField(dump_kwargs={'cls': jsonfield.encoder.JSONEncoder, 'separators': (',', ':')}, editable=False, load_kwargs={})),
                ('isd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trcs', to='scionlab.ISD', verbose_name='ISD')),
                ('voting_offline', models.ManyToManyField(to='scionlab.Key')),
            ],
            options={
                'verbose_name': 'TRC',
                'verbose_name_plural': 'TRCs',
                'unique_together': {('isd', 'version')},
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('issuer', 'issuer'), ('chain', 'chain')], editable=False, max_length=16)),
                ('version', models.PositiveIntegerField()),
                ('not_before', models.DateTimeField()),
                ('not_after', models.DateTimeField()),
                ('certificate', jsonfield.fields.JSONField(dump_kwargs={'cls': jsonfield.encoder.JSONEncoder, 'separators': (',', ':')}, load_kwargs={})),
                ('AS', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='scionlab.AS')),
            ],
            options={
                'unique_together': {('AS', 'type', 'version')},
            },
        ),

        migrations.RunPython(reset_pki),
    ]
