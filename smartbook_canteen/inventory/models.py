
from datetime import datetime
from jsonfield import JSONField

from django.db import models
from dashboard.models import Canteen
# from administration.models import BonusPoint
from utils import calculate_actual_quantity
from datetime import timedelta


class Category(models.Model):

    canteen = models.ForeignKey(Canteen, null=True, blank=True) 
    parent = models.ForeignKey('self', null=True, blank=True)
    name = models.CharField('Name', max_length=200, null=True, blank=True, unique=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Category'

    def get_json_data(self):

        category_data = {
            'id': self.id,
            'name': self.name,
            'canteen':self.canteen.name if self.canteen else '',
            'parent_id': self.parent.id if self.parent else '',
            'parent_name': self.parent.name if self.parent else '',
            'subcategories': [],
            'subcategories_count': Category.objects.filter(parent=self.parent).count() if self.parent else 0,
        }
        return category_data

    def set_attributes(self, category_details):

        self.name = category_details['name']
        canteen_obj = Canteen.objects.get(id=category_details['canteen'])
        self.canteen = canteen_obj;
        if category_details.get('parent_id', ''): 
            parent = Category.objects.get(id=category_details['parent_id'])
            self.parent = parent
        else:
            self.parent = None
        self.save()
        return self


class Item(models.Model):

    canteen = models.ForeignKey(Canteen, null=True, blank=True)
    category = models.ForeignKey(Category, null = True, blank =True)
    name = models.CharField('Name', max_length=200, null=True, blank=True)
    code = models.CharField('Code', max_length=200, unique=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    
    uom = models.CharField('UOM', max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Item, self).save() # for getting pk
        if self.name:
            self.code = self.name[:3] + str(self.id ) 
        super(Item, self).save()
       
        
    def __unicode__(self):
        return str(self.code) + ' - ' + self.name

    class Meta:
        verbose_name_plural = 'Item'

    def get_json_data(self):
        batch_item_exists = False
        batch_items = BatchItem.objects.filter(item__id=self.id)
        if batch_items:
            batch_item_exists = True
        else:
            batch_item_exists = False
        item_data = {
            'id': self.id,
            'item_id':self.id,
            'item_name': self.name,
            'item_code':self.code,
            'name': str(self.name),
            'description': self.description,
            'uom':self.uom,
            'canteen_name': self.canteen.name if self.canteen else '',
            'category_name':self.category.name if self.category else '',
            'batch_item_exists': batch_item_exists
        }
        return item_data        
    
    def set_attributes(self, item_details):
        print item_details
        print item_details['canteen'];
        canteen_obj = Canteen.objects.get(id=item_details['canteen'])
        self.canteen = canteen_obj;
        category_obj = Category.objects.get(id=item_details['category_id'])
        self.category = category_obj;
        self.name = item_details['name']
        self.description = item_details['description'] 
        if item_details['new_item'] == 'true':
            self.uom = item_details['uom']  
            
        self.save()
        return self
        

class Batch(models.Model):
    canteen = models.ForeignKey(Canteen, null=True, blank=True)
    name = models.CharField('Batch name', max_length=200, unique=True)
    created_date = models.DateField('Created', null=True, blank=True)
    expiry_date = models.DateField('Expiry date', null=True, blank=True)
    closed = models.BooleanField('Batch Closed', default=False)

    def save(self, *args, **kwargs):
        super(Batch, self).save() # for getting pk
        if self.created_date and self.expiry_date:
            self.name = str(self.created_date.strftime('%d/%m/%Y')) + '-' + str(self.expiry_date.strftime('%d/%m/%Y')) + '-' +str(self.canteen.id)
        super(Batch, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Batch'

    def get_json_data(self):

        batch_data = {
            'id': self.id,
            'name': self.name,
            'created_date': self.created_date.strftime('%d/%m/%Y') if self.created_date else '',
            'expiry_date': self.expiry_date.strftime('%d/%m/%Y') if self.expiry_date else '',
            'closed_flag':self.closed,
        }
        return batch_data

    def set_attributes(self, batch_details):
        print("hghg");
        print(batch_details);
        canteen_obj = Canteen.objects.get(id=batch_details['canteen'])
        self.canteen = canteen_obj;
        self.name = batch_details['name']
        print(self.name)
        self.created_date = datetime.strptime(batch_details['created_date'], '%d/%m/%Y')
        if batch_details['expiry_date']:
            self.expiry_date = datetime.strptime(batch_details['expiry_date'], '%d/%m/%Y')
        else:
            self.expiry_date = None;
        self.save()
        return self

    def set_name(self):
        self.created_date = datetime.now().date()
        self.expiry_date = self.created_date + timedelta(days=6)
        self.name = str(self.created_date.strftime('%d/%m/%Y')) + '-' + str(self.expiry_date.strftime('%d/%m/%Y')) + '-' + str(self.canteen.id) 
        self.save()

UOM_STATUS_CHOICES = (
    ('used', 'used'),
    ('not used', 'not used')
)


class BatchItem(models.Model):

    batch = models.ForeignKey(Batch, null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True)
    closing_stock = models.CharField('closing stock', max_length=200, null=True, blank=True)
    consumed_quantity = models.DecimalField('Consumed Quantity', max_digits=20, decimal_places=5, default=0)
    stock = models.FloatField('Stock', default=0, max_length=100)
    purchase_price = models.DecimalField('Purchase Price', default=0, max_digits=50, decimal_places=5)    
    selling_price = models.DecimalField('Selling Price', default=0, max_digits=50, decimal_places=5)
    uom = models.CharField('UOM', max_length=200, null=True, blank=True)
    created_date =  models.DateField('Created Date', null="True", blank =True)
    
    def __unicode__(self):
        return self.batch.name + ' - ' + self.item.code+ ' - ' + self.item.name

    class Meta:
        verbose_name_plural = 'Batch Item'

    def get_json_data(self):

        stock = self.stock
        consumed_quantity = self.consumed_quantity
        closing_stock = self.closing_stock
        batch_item_details = {
            'item_id': self.item.id,
            'item_name': self.item.name,
            'code': self.item.code,                                                                                                      
            'id': self.id,
            'batch_id': self.batch.id,
            'purchase_price':self.purchase_price,
            'selling_price':self.selling_price,
            'stock': round(float(self.stock),2),
            'consumed_quantity':self.consumed_quantity,
            'closing_stock':self.closing_stock,
            'uom' :self.uom,

        }
        return batch_item_details

    def set_quantity(self, quantity, quantity_unit):
        item = self.item
        raw_quantity = quantity = float(quantity)
        print "in set quantity", quantity, quantity_unit
        if type(quantity_unit) == 'dict':
            quantity_unit = quantity_unit['uom']
        actual_quantity = calculate_actual_quantity(item, quantity, quantity_unit)
        self.quantity_in_actual_unit = self.quantity_in_actual_unit + float(actual_quantity)
        self.save()



class StockValue(models.Model):

    stock_by_value = models.DecimalField('Balance', max_digits=20, null=True, blank=True, decimal_places=5)

    def __unicode__(self):
        return str(self.stock_by_value)
    class Meta:
        verbose_name_plural = 'Stock Value'

class OpeningStockValue(models.Model):

    stock_by_value = models.DecimalField('Balance', max_digits=20, null=True, blank=True, decimal_places=5)

    def __unicode__(self):
        return str(self.stock_by_value)
    class Meta:
        verbose_name_plural = 'Opening Stock Value'


class cashEntry(models.Model):
    
    batch = models.ForeignKey(Batch, null= True, blank=True)
    date = models.DateField('Date', null="True", blank =True)
    amount = models.DecimalField('Amount', max_digits=20, null=True, blank=True, decimal_places=5)
    def __unicode__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural = 'cash enrty'

    def set_attributes(self, cash_entries):
        
        self.date = cash_entries['date']
        self.amount = cash_entries['amount']
        batch_obj = Batch.objects.get(id=cash_entries['batch'])
        self.batch = batch_obj
        self.save()
        return self 

    def get_json_data(self):
         
        cash_entry_details={
        'id':self.id,
        'batch':self.batch.name,
        'date':self.date.strftime('%d/%m/%Y'),
        'amount':self.amount,
        }  
        return cash_entry_details




