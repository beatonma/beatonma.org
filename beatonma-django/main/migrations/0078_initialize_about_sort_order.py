from django.db import migrations


def apply_default_ordering(apps, schema_editor):
    for model_name in ["AboutPost"]:
        Model = apps.get_model("main", model_name)
        for order, item in enumerate(Model.objects.all(), 1):
            item.sort_order = order
            item.save(update_fields=["sort_order"])


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0077_alter_aboutpost_options_aboutpost_parent_and_more"),
    ]

    operations = [
        migrations.RunPython(
            code=apply_default_ordering, reverse_code=migrations.RunPython.noop
        ),
    ]
