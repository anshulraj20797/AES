from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import DO_NOTHING, SET_NULL


# Masters required in transaction models
class BranchMaster(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    contact_person_name = models.CharField(max_length=20)
    gst_number = models.CharField(max_length=20)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(blank=True, null=True, max_length=10)

    def __str__(self):
        return self.short_name


class DepartmentMaster(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class CompanyLedgerMaster(models.Model):
    name = models.CharField(max_length=32, unique=True)
    gst_number = models.CharField(max_length=20, unique=True)
    supplier_status = models.BooleanField(default=False)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    remarks = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name


class ArticleMaster(models.Model):
    name = models.CharField(max_length=80, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    blend_pct = models.CharField(max_length=50)
    twists = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name


class ColorMaster(models.Model):
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    remarks = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name

TRANSACTION_STATUS_CHOICE = (('PENDING','PENDING'),('COMPLETED','COMPLETED'),('CLOSE','CLOSE'))

class Transaction(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.DO_NOTHING)
    branch = models.ForeignKey(BranchMaster, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(DepartmentMaster, on_delete=DO_NOTHING)
    transaction_id = models.CharField(unique=True, max_length=255)
    transaction_status = models.CharField(max_length=255 ,choices=TRANSACTION_STATUS_CHOICE)
    remarks = models.CharField(max_length=255 ,null=True)

    def __str__(self):
        return self.transaction_id

UNIT_CHOICE = (('KG','KG'),('METER','METER'))

class TransactionLineItemDetails(models.Model):
    transaction_id = models.ForeignKey(Transaction ,related_name='lineitems', on_delete=models.DO_NOTHING)
    id = models.BigAutoField(auto_created=True, primary_key=True)
    article = models.ForeignKey(ArticleMaster, on_delete=models.DO_NOTHING)    
    color = models.ForeignKey(ColorMaster, on_delete=DO_NOTHING)
    required_on_date = models.DateTimeField()
    quantity = models.DecimalField(max_digits=4, decimal_places=2)
    rate_per_unit = models.IntegerField()
    unit = models.CharField(max_length=255, choices=UNIT_CHOICE)

    def __str__(self):
        return str(self.id)

class InventoryItem(models.Model):
    transactionlineitemdetails_id = models.ForeignKey(TransactionLineItemDetails, related_name='inventory_items', on_delete=models.PROTECT)
    id = models.BigAutoField(auto_created=True, primary_key=True)
    article = models.ForeignKey(ArticleMaster, on_delete=models.DO_NOTHING)
    color = models.ForeignKey(ColorMaster, on_delete=DO_NOTHING)
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.DO_NOTHING)
    gross_quantity = models.DecimalField(max_digits=4, decimal_places=2)
    net_quantity = models.DecimalField(max_digits=4, decimal_places=2)
    unit = models.CharField(max_length=255, choices=UNIT_CHOICE)

    def __str__(self):
        return str(self.id)
   






    
