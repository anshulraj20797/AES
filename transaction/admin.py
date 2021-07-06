from django.contrib import admin

from transaction import models

admin.site.register(models.BranchMaster)
admin.site.register(models.DepartmentMaster)
admin.site.register(models.CompanyLedgerMaster)
admin.site.register(models.ArticleMaster)
admin.site.register(models.ColorMaster)
admin.site.register(models.Transaction)
admin.site.register(models.TransactionLineItemDetails)
admin.site.register(models.InventoryItem)

