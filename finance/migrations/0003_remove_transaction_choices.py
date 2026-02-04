"""Remove the unintended `choices` field from Transaction model."""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0002_alter_transaction_transaction_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaction",
            name="choices",
        ),
    ]
