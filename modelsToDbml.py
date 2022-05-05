import django.apps
from django.db import models
from django.contrib.postgres.fields import CITextField

fields_dict = {
    models.AutoField.__name__: "int",
    models.CharField.__name__: "varchar",
    models.IntegerField.__name__: "int",
    models.TextField.__name__: "text",
    CITextField.__name__: "citext",
    models.DateTimeField.__name__: "datetime",
    models.BooleanField.__name__: "boolean",
    models.SmallIntegerField.__name__: "small_int",
    models.FileField.__name__: "file",
    models.BigAutoField.__name__: "big_int",
    models.FilePathField.__name__: "file_path",
    models.FloatField.__name__: "float",
    models.BigIntegerField.__name__: "big_int",
    models.BinaryField.__name__: "binary",
    models.CommaSeparatedIntegerField.__name__: "comma_seprated_int",
    models.DateField.__name__: "date",
    models.DecimalField.__name__: "decimal",
    models.DurationField.__name__: "duration",
    models.EmailField.__name__: "email",
    models.GenericIPAddressField.__name__: "generic_ip",
    models.ImageField.__name__: "image",
    models.IPAddressField.__name__: "ip",
    models.NullBooleanField.__name__: "null_boolean",
    models.PositiveIntegerField.__name__: "positive_int",
    models.PositiveSmallIntegerField.__name__: "positive_small_int",
    models.SlugField.__name__: "slug",
    models.SmallAutoField.__name__: "small_int",
    models.TimeField.__name__: "time",
    models.URLField.__name__: "url",
    models.UUIDField.__name__: "uuid",
    models.ManyToManyField.__name__: "many_to_many",
    models.OneToOneField.__name__: "one_to_one",
    models.ForeignKey.__name__: "foreign_key",
}

def convert():
    tables_dict = {}
    rels = []

    tables = django.apps.apps.get_models()
    for table in tables:
        keys = table.__dict__.keys()
        tables_dict[str(table.__name__)] = []
        for key in keys:
            value = table.__dict__[key]

            # Check the fields and ManyToMany relations only
            if not isinstance(value, django.db.models.query_utils.DeferredAttribute) and\
                    not isinstance(value, models.fields.related_descriptors.ManyToManyDescriptor):
                continue

            field = value.__dict__['field']
            if isinstance(field, models.ManyToManyField) and field.related_model == table:
                continue
            try:
                line = str(field.name) + ' '+fields_dict[type(field).__name__]
                if not (isinstance(field, models.ManyToManyField) or
                        isinstance(field, models.OneToOneField) or
                        isinstance(field, models.ForeignKey)):
                    line = line + ' [note: "'
                    line = line + "primary_key : " + str(field.primary_key)
                    if field.max_length is not None:
                        line = line + "<br>max_length : " + str(field.max_length)
                    line = line + "<br>nullable : "+str(field.null)
                    line = line + "<br>blank : "+str(field.blank)
                    if field.choices is not None:
                        line = line + "<br>choices : "+str(field.choices)
                    line = line+'"]'
                elif not isinstance(field, models.ManyToManyField):
                    if field.to_fields[0] is not None and field.to_fields[0] != 'self':
                        rels.append("ref: "+table.__name__+"."+field.name+" > "+str(field.related_model.__name__)+"."+field.to_fields[0])
                    else:
                        _, related_field = field.related_fields[0]
                        rels.append("ref: "+table.__name__+"."+field.name+" > "+str(field.related_model.__name__)+"."+related_field.name)
                else:
                    related_field = ""
                    for keey in field.related_model.__dict__.keys():
                        valuee = field.related_model.__dict__[keey]
                        if isinstance(valuee, django.db.models.query_utils.DeferredAttribute):
                            related_field = valuee.__dict__['field'].name
                            break
                    rels.append("ref: " + table.__name__ + "." + field.name + " > " + str(field.related_model.__name__) + "." + related_field)
                tables_dict[str(table.__name__)].append(line)
            except KeyError:
                pass

    with open("output.dbml", "w") as output:
        for table_name in tables_dict.keys():
            if not tables_dict[table_name]:
                continue
            output.write("table "+table_name+" {\n")
            for line in tables_dict[table_name]:
                output.write(line+"\n")
            output.write("}\n\n")
        for rel in rels:
            output.write(rel+"\n")
    output.close()
