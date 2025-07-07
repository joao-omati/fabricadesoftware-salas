# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


'''





            ESSE MODELS É UM TESTE. NELE ESTÃO TODAS AS TABELAS DO BANCO DE DADOS ATUAL
            

            


'''
 
from django.db import models


class Curso(models.Model):
    idcurso = models.AutoField(primary_key=True)
    matriculauser = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='matriculauser', to_field='matricula', blank=True, null=True)
    nomecurso = models.CharField(max_length=255)
    dthinsert = models.DateTimeField(blank=True, null=True)
    dthdelete = models.DateTimeField(blank=True, null=True)
    statusdelete = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'curso'


class Diasemana(models.Model):
    iddiasemana = models.AutoField(primary_key=True)
    idreservasala = models.ForeignKey('Reservasala', models.DO_NOTHING, db_column='idreservasala')
    idperiodo = models.ForeignKey('Periodo', models.DO_NOTHING, db_column='idperiodo')
    segunda = models.BooleanField(blank=True, null=True)
    terca = models.BooleanField(blank=True, null=True)
    quarta = models.BooleanField(blank=True, null=True)
    quinta = models.BooleanField(blank=True, null=True)
    sexta = models.BooleanField(blank=True, null=True)
    sabado = models.BooleanField(blank=True, null=True)
    domingo = models.BooleanField(blank=True, null=True)
    dthinsert = models.DateTimeField(blank=True, null=True)
    dthdelete = models.DateTimeField(blank=True, null=True)
    statusdelete = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diasemana'


class Periodo(models.Model):
    idperiodo = models.AutoField(primary_key=True)
    idreservasala = models.ForeignKey('Reservasala', models.DO_NOTHING, db_column='idreservasala')
    primeiro = models.BooleanField(blank=True, null=True)
    segundo = models.BooleanField(blank=True, null=True)
    terceiro = models.BooleanField(blank=True, null=True)
    quarto = models.BooleanField(blank=True, null=True)
    integral = models.BooleanField(blank=True, null=True)
    dthinsert = models.DateTimeField(blank=True, null=True)
    dthdelete = models.DateTimeField(blank=True, null=True)
    statusdelete = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'periodo'


class Reserva(models.Model):
    idreserva = models.AutoField(primary_key=True)
    matriculauser = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='matriculauser', to_field='matricula')
    idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='idcurso', blank=True, null=True)
    idturma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='idturma')
    codturma = models.CharField(max_length=255)
    datainicial = models.DateField(blank=True, null=True)
    datafinal = models.DateField(blank=True, null=True)
    dthinsert = models.DateTimeField(blank=True, null=True)
    dthdelete = models.DateTimeField(blank=True, null=True)
    statusdelete = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reserva'


class Reservasala(models.Model):
    idreservasala = models.AutoField(primary_key=True)
    idreserva = models.ForeignKey(Reserva, models.DO_NOTHING, db_column='idreserva')
    idsala = models.ForeignKey('Sala', models.DO_NOTHING, db_column='idsala')
    turno = models.CharField(max_length=25, blank=True, null=True)
    responsavel = models.CharField(max_length=255)
    descricaoreserva = models.CharField(max_length=255, blank=True, null=True)
    statusreserva = models.BooleanField(blank=True, null=True)
    dthinsert = models.DateTimeField(blank=True, null=True)
    dthdelete = models.DateTimeField(blank=True, null=True)
    statusdelete = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservasala'


class Sala(models.Model):
    idsala = models.AutoField(primary_key=True)
    matriculauser = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='matriculauser', to_field='matricula', blank=True, null=True)
    bloco = models.CharField(max_length=10)
    andar = models.CharField(max_length=25)
    numerosala = models.IntegerField()
    capacidade = models.IntegerField()
    tvtamanho = models.CharField(max_length=5)
    datashow = models.BooleanField(blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    motivoinativo = models.CharField(max_length=255, blank=True, null=True)
    dthinsert = models.DateTimeField(blank=True, null=True)
    dthdelete = models.DateTimeField(blank=True, null=True)
    statusdelete = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sala'


class Turma(models.Model):
    idturma = models.AutoField(primary_key=True)
    idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='idcurso', blank=True, null=True)
    matriculauser = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='matriculauser', to_field='matricula', blank=True, null=True)
    codturma = models.CharField(max_length=255)
    periodoletivo = models.CharField(max_length=25, blank=True, null=True)
    qtdaluno = models.IntegerField(blank=True, null=True)
    dthinsert = models.DateTimeField(blank=True, null=True)
    dthdelete = models.DateTimeField(blank=True, null=True)
    statusdelete = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turma'


class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True)
    matricula = models.IntegerField(unique=True)
    matriculauser = models.ForeignKey('self', models.DO_NOTHING, db_column='matriculauser', to_field='matricula', blank=True, null=True)
    nome = models.CharField(max_length=255)
    emailinst = models.CharField(max_length=255)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    cargo = models.CharField(max_length=25)
    senha = models.CharField(max_length=255)
    statuslogin = models.BooleanField(blank=True, null=True)
    dthinsert = models.DateTimeField(blank=True, null=True)
    dthdelete = models.DateTimeField(blank=True, null=True)
    statusdelete = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
