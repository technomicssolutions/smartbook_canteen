from django.contrib import admin

from models import Item, Category,Batch, BatchItem, StockValue, OpeningStockValue,cashEntry 


admin.site.register(Category)

admin.site.register(Batch)
admin.site.register(Item)
admin.site.register(BatchItem)
admin.site.register(cashEntry)
admin.site.register(OpeningStockValue)
admin.site.register(StockValue)
