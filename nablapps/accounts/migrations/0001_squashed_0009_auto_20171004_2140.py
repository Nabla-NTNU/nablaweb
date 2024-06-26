# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-23 18:46
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import nablapps.accounts.models

# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# nablapps.accounts.migrations.0007_move_to_new_likepress_app


class Migration(migrations.Migration):
    replaces = [
        ("accounts", "0001_initial"),
        ("accounts", "0002_registrationrequest"),
        ("accounts", "0003_auto_20150925_2315"),
        ("accounts", "0004_auto_20150927_1840"),
        ("accounts", "0005_likepress"),
        ("accounts", "0006_auto_20160202_2330"),
        ("accounts", "0007_move_to_new_likepress_app"),
        ("accounts", "0008_nablagroup_logo"),
        ("accounts", "0009_auto_20171004_2140"),
    ]

    initial = True

    dependencies = [
        ("auth", "0006_require_contenttypes_0002"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="NablaUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=30,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\w.@+-]+$",
                                "Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.",
                                "invalid",
                            )
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "telephone",
                    models.CharField(blank=True, max_length=15, verbose_name="Telefon"),
                ),
                (
                    "cell_phone",
                    models.CharField(blank=True, max_length=15, verbose_name="Mobil"),
                ),
                (
                    "birthday",
                    models.DateField(blank=True, null=True, verbose_name="Bursdag"),
                ),
                (
                    "address",
                    models.CharField(blank=True, max_length=40, verbose_name="Adresse"),
                ),
                (
                    "mail_number",
                    models.CharField(blank=True, max_length=4, verbose_name="Postnr"),
                ),
                (
                    "web_page",
                    models.CharField(
                        blank=True, max_length=80, verbose_name="Hjemmeside"
                    ),
                ),
                (
                    "wants_email",
                    models.BooleanField(default=True, verbose_name="Motta kullmail"),
                ),
                ("about", models.TextField(blank=True, verbose_name="Biografi")),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="avatars",
                        verbose_name="Avatar",
                    ),
                ),
                (
                    "ntnu_card_number",
                    models.CharField(
                        blank=True,
                        help_text="Dette er et 7-10 siffer lant nummeret på baksiden av kortet. På nye kort er dette siffrene etter EM. På gamle kort ert dette siffrene nede til venstre. Det brukes blant annet for å komme inn på bedpresser.",
                        max_length=10,
                        verbose_name="NTNU kortnr",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "users",
                "abstract": False,
                "verbose_name": "user",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="NablaGroup",
            fields=[
                (
                    "group_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="auth.Group",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Beskrivelse"),
                ),
                (
                    "mail_list",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="Epostliste"
                    ),
                ),
                (
                    "group_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("komite", "Komité"),
                            ("kull", "Kull"),
                            ("studprog", "Studieprogram"),
                            ("komleder", "Komitéleder"),
                            ("styremedlm", "Styremedlem"),
                            ("stilling", "Stilling"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
            bases=("auth.group",),
        ),
        migrations.CreateModel(
            name="FysmatClass",
            fields=[
                (
                    "nablagroup_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="accounts.NablaGroup",
                    ),
                ),
                (
                    "starting_year",
                    models.CharField(
                        max_length=4, unique=True, verbose_name="År startet"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Kull",
                "verbose_name": "Kull",
            },
            bases=("accounts.nablagroup",),
        ),
        migrations.AddField(
            model_name="nablauser",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="nablauser",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.CreateModel(
            name="RegistrationRequest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_created=True, verbose_name="Opprettet"),
                ),
                (
                    "username",
                    models.CharField(max_length=80, verbose_name="Brkuernavn"),
                ),
                (
                    "first_name",
                    models.CharField(max_length=80, null=True, verbose_name="Fornavn"),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=80, null=True, verbose_name="Etternavn"
                    ),
                ),
            ],
            options={
                "verbose_name": "Registreringsforespørsel",
                "verbose_name_plural": "Registreringsforespørsler",
            },
        ),
        migrations.AlterModelManagers(
            name="nablauser",
            managers=[
                ("objects", nablapps.accounts.models.NablaUserManager()),
            ],
        ),
        migrations.AddField(
            model_name="nablagroup",
            name="logo",
            field=models.FileField(
                blank=True, null=True, upload_to="logos", verbose_name="Logo"
            ),
        ),
        migrations.AlterField(
            model_name="nablauser",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="username",
            ),
        ),
    ]
