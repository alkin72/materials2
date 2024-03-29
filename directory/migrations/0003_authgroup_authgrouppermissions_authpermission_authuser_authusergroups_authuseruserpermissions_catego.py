# Generated by Django 3.2.8 on 2022-02-14 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('directory', '0002_auto_20211127_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('value', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryWork',
            fields=[
                ('category_work_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                'db_table': 'category_work',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Coeficient',
            fields=[
                ('coeficient_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('value', models.DecimalField(decimal_places=3, max_digits=8)),
            ],
            options={
                'db_table': 'coeficient',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contragents',
            fields=[
                ('contragents_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='наименование')),
                ('fullname', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('e_mail', models.EmailField(blank=True, db_column='e-mail', max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'contragents',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('doc_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('number', models.BigIntegerField(unique=True, verbose_name='Номер документа')),
                ('datetime', models.DateField(verbose_name='Дата')),
                ('note', models.CharField(blank=True, max_length=100, null=True, verbose_name='примечание')),
                ('category_move', models.BooleanField(default=True, verbose_name='Движение')),
                ('move', models.BooleanField(default=False, verbose_name='Проведение')),
                ('isdelete', models.BooleanField(verbose_name='Удаление')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
                'db_table': 'document',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentReceipt',
            fields=[
                ('doc_receipt_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('number', models.BigIntegerField()),
                ('datetime', models.DateField()),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('isdelete', models.BooleanField()),
                ('move', models.BooleanField()),
                ('contragent_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'document_receipt',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentReceiptRef',
            fields=[
                ('doc_receipt_ref_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('number_row', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=3, max_digits=8)),
            ],
            options={
                'db_table': 'document_receipt_ref',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentRef',
            fields=[
                ('doc_ref_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True, verbose_name='')),
            ],
            options={
                'db_table': 'document_ref',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('fullname', models.CharField(blank=True, max_length=255, null=True)),
                ('lastname', models.CharField(blank=True, max_length=255, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('e_mail', models.CharField(blank=True, db_column='e-mail', max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'employee',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeWork',
            fields=[
                ('employee_work_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value_time', models.TimeField()),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'employee_work',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Materials',
            fields=[
                ('materials_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Номенклатура')),
            ],
            options={
                'db_table': 'materials',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('position_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'position',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('receipt_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'receipt',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ReceiptDetail',
            fields=[
                ('receipt_detail_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={
                'db_table': 'receipt_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RegisterMaterialsMove',
            fields=[
                ('register_materials_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=3, max_digits=7)),
                ('datetime', models.DateField()),
                ('move', models.BooleanField()),
                ('action', models.BooleanField()),
            ],
            options={
                'db_table': 'register_materials_move',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RegisterMaterialsRemainder',
            fields=[
                ('register_materials_remainder_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=3, max_digits=6)),
                ('datetime', models.DateField()),
            ],
            options={
                'db_table': 'register_materials_remainder',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RegisterReceipt',
            fields=[
                ('register_receipt_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateField()),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'register_receipt',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RegisterReceiptComposition',
            fields=[
                ('register_recept_composition_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=2, max_digits=4)),
                ('datetime', models.DateField()),
            ],
            options={
                'db_table': 'register_receipt_composition',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('unit_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Ед. изм.')),
                ('fullname', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'unit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('work_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('fullname', models.CharField(blank=True, max_length=255, null=True)),
                ('time', models.TimeField()),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'work',
                'managed': False,
            },
        ),
    ]
