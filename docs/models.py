# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


CHOICES_category_doc = (
    (True, 'Приход'),
    (False, 'Расход'),
)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class CategoryWork(models.Model):
    category_work_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'category_work'


class Coeficient(models.Model):
    coeficient_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=8, decimal_places=3)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coeficient'


class Contragents(models.Model):
    contragents_id = models.BigAutoField(primary_key=True)
    name = models.CharField('наименование', max_length=255)
    fullname = models.CharField('полное наименование', max_length=255)
    address = models.CharField('адрес', max_length=255, blank=True, null=True)
    phone = models.CharField('телефон', max_length=255, blank=True, null=True)
    e_mail = models.EmailField('e-mail', db_column='e-mail', max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    note = models.CharField('примечание', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contragents'

        def __init__(self):
            self.name = None

        def __str__(self):
            return f'Контрагент: {self.name}'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Document(models.Model):
    objects = None
    doc_id = models.BigAutoField(primary_key=True)
    number = models.BigIntegerField('Номер документа', unique=True)
    datetime = models.DateField('Дата')
    holding = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='holding')
    note = models.CharField('примечание', max_length=100, blank=True, null=True)
    category_move = models.BooleanField('Движение', default=True)
    move = models.BooleanField('Проведение', default=False)
    isdelete = models.BooleanField('Пометить на удаление')
    contragent = models.ForeignKey(Contragents, models.DO_NOTHING, 'Контрагент')

    class Meta:
        managed = False
        db_table = 'document'
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return str(self.number)


class DocumentReceipt(models.Model):
    doc_receipt_id = models.BigAutoField(primary_key=True)
    number = models.BigIntegerField()
    datetime = models.DateField()
    holding = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='holding')
    note = models.CharField(max_length=255, blank=True, null=True)
    isdelete = models.BooleanField('Пометить на удаление')
    move = models.BooleanField()
    #contragent_id = models.BigIntegerField()
    contragent = models.ForeignKey(Contragents, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'document_receipt'

    # def get_success_url(self):


class DocumentReceiptRef(models.Model):
    doc_receipt_ref_id = models.BigAutoField(primary_key=True)
    doc_receipt = models.ForeignKey(DocumentReceipt, models.DO_NOTHING, related_name='docs_receipt_set')
    receipt = models.ForeignKey('Receipt', models.DO_NOTHING,  verbose_name='')
    value = models.DecimalField(max_digits=8, decimal_places=3,  verbose_name='')
    unit = models.ForeignKey('Unit', models.DO_NOTHING,  verbose_name='')

    class Meta:
        managed = False
        db_table = 'document_receipt_ref'


class DocumentRef(models.Model):
    objects = None
    doc_ref_id = models.BigAutoField(primary_key=True)
    doc = models.ForeignKey(Document, models.DO_NOTHING, related_name='docs_set')
    materials = models.ForeignKey('Materials', models.DO_NOTHING, verbose_name='')
    value = models.DecimalField(verbose_name='', max_digits=8, decimal_places=3, blank=True, null=True)
    unit = models.ForeignKey('Unit', models.DO_NOTHING, verbose_name='')

    class Meta:
        managed = False
        db_table = 'document_ref'

    def __str__(self):
        return str(self.doc)


class Employee(models.Model):
    employee_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    position = models.ForeignKey('Position', models.DO_NOTHING)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    e_mail = models.CharField(db_column='e-mail', max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    address = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'

    def __str__(self):
        return self.name


class EmployeeWork(models.Model):
    employee_work_id = models.BigAutoField(primary_key=True)
    work = models.ForeignKey('Work', models.DO_NOTHING)
    employee = models.ForeignKey(Employee, models.DO_NOTHING)
    value_time = models.TimeField()
    category_work = models.ForeignKey(CategoryWork, models.DO_NOTHING)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_work'


class Materials(models.Model):
    materials_id = models.BigAutoField(primary_key=True)
    name = models.CharField('Номенклатура', max_length=100)
    category = models.ForeignKey(Category, models.DO_NOTHING)
    coeficient = models.ForeignKey(Coeficient, models.DO_NOTHING)
    unit = models.ForeignKey('Unit', models.DO_NOTHING, verbose_name='')

    class Meta:
        managed = False
        db_table = 'materials'

    def __str__(self):
        return self.name


class Position(models.Model):
    position_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'position'

    def __str__(self):
        return self.name


class Receipt(models.Model):
    receipt_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date = models.DateField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receipt'

    def __str__(self):
        return self.name


class ReceiptDetail(models.Model):
    receipt_detail_id = models.BigAutoField(primary_key=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    materials = models.ForeignKey(Materials, models.DO_NOTHING, verbose_name='')
    value = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='')

    class Meta:
        managed = False
        db_table = 'receipt_detail'


class RelationDoc(models.Model):
    rel_id = models.BigAutoField(primary_key=True)
    doc = models.ForeignKey(Document, models.DO_NOTHING)
    doc_receipt = models.ForeignKey(DocumentReceipt, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'relation_doc'


class RegisterMaterialsMove(models.Model):
    objects = None
    register_materials_id = models.BigAutoField(primary_key=True)
    materials = models.ForeignKey(Materials, models.DO_NOTHING)
    value = models.DecimalField(max_digits=7, decimal_places=3)
    datetime = models.DateField()
    registrator = models.ForeignKey(Document, models.DO_NOTHING, db_column='registrator')
    move = models.BooleanField()
    action = models.BooleanField()
    move_deff = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'register_materials_move'


class RegisterMaterialsRemainder(models.Model):
    register_materials_remainder_id = models.BigAutoField(primary_key=True)
    materials = models.ForeignKey(Materials, models.DO_NOTHING)
    value = models.DecimalField(max_digits=6, decimal_places=3)
    datetime = models.DateField()

    class Meta:
        managed = False
        db_table = 'register_materials_remainder'


class RegisterReceipt(models.Model):
    register_receipt_id = models.BigAutoField(primary_key=True)
    receipt = models.ForeignKey(Receipt, models.DO_NOTHING)
    datetime = models.DateField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'register_receipt'


class RegisterReceiptComposition(models.Model):
    register_recept_composition_id = models.BigAutoField(primary_key=True)
    register_receipt = models.ForeignKey(RegisterReceipt, models.DO_NOTHING)
    materials = models.ForeignKey(Materials, models.DO_NOTHING)
    value = models.DecimalField(max_digits=4, decimal_places=2)
    datetime = models.DateField()

    class Meta:
        managed = False
        db_table = 'register_receipt_composition'


class Unit(models.Model):
    unit_id = models.BigAutoField(primary_key=True)
    name = models.CharField('Ед. изм.', max_length=255)
    fullname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unit'

    def __str__(self):
        return self.name


class Work(models.Model):
    work_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    time = models.TimeField()
    category_work = models.ForeignKey(CategoryWork, models.DO_NOTHING)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work'

    def __str__(self):
        return self.name

# class Choicemove(models.Model):
#
#     value = models.CharField(max_length=2, choices=CHOICES)