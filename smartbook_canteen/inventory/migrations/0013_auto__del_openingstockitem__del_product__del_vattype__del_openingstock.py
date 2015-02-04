# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'OpeningStockItem'
        db.delete_table(u'inventory_openingstockitem')

        # Deleting model 'Product'
        db.delete_table(u'inventory_product')

        # Deleting model 'VatType'
        db.delete_table(u'inventory_vattype')

        # Deleting model 'OpeningStock'
        db.delete_table(u'inventory_openingstock')

        # Deleting model 'Brand'
        db.delete_table(u'inventory_brand')

        # Deleting field 'Item.offer_quantity'
        db.delete_column(u'inventory_item', 'offer_quantity')

        # Deleting field 'Item.uoms'
        db.delete_column(u'inventory_item', 'uoms')

        # Deleting field 'Item.smallest_unit'
        db.delete_column(u'inventory_item', 'smallest_unit')

        # Deleting field 'Item.unit_per_packet'
        db.delete_column(u'inventory_item', 'unit_per_packet')

        # Deleting field 'Item.unit_per_piece'
        db.delete_column(u'inventory_item', 'unit_per_piece')

        # Deleting field 'Item.size'
        db.delete_column(u'inventory_item', 'size')

        # Deleting field 'Item.actual_smallest_uom'
        db.delete_column(u'inventory_item', 'actual_smallest_uom')

        # Deleting field 'Item.cess'
        db.delete_column(u'inventory_item', 'cess')

        # Deleting field 'Item.product'
        db.delete_column(u'inventory_item', 'product_id')

        # Deleting field 'Item.unit_per_box'
        db.delete_column(u'inventory_item', 'unit_per_box')

        # Deleting field 'Item.brand'
        db.delete_column(u'inventory_item', 'brand_id')

        # Deleting field 'Item.barcode'
        db.delete_column(u'inventory_item', 'barcode')

        # Deleting field 'Item.pieces_per_box'
        db.delete_column(u'inventory_item', 'pieces_per_box')

        # Deleting field 'Item.pieces_per_packet'
        db.delete_column(u'inventory_item', 'pieces_per_packet')

        # Deleting field 'Item.vat_type'
        db.delete_column(u'inventory_item', 'vat_type_id')

        # Deleting field 'Item.item_type'
        db.delete_column(u'inventory_item', 'item_type')

        # Deleting field 'Item.packets_per_box'
        db.delete_column(u'inventory_item', 'packets_per_box')

        # Deleting field 'BatchItem.permissible_discount_percentage'
        db.delete_column(u'inventory_batchitem', 'permissible_discount_percentage')

        # Deleting field 'BatchItem.small_wholesale_price'
        db.delete_column(u'inventory_batchitem', 'small_wholesale_price')

        # Deleting field 'BatchItem.small_branch_price'
        db.delete_column(u'inventory_batchitem', 'small_branch_price')

        # Deleting field 'BatchItem.salesman_bonus_quantity'
        db.delete_column(u'inventory_batchitem', 'salesman_bonus_quantity')

        # Deleting field 'BatchItem.retail_profit_percentage'
        db.delete_column(u'inventory_batchitem', 'retail_profit_percentage')

        # Deleting field 'BatchItem.freight_charge'
        db.delete_column(u'inventory_batchitem', 'freight_charge')

        # Deleting field 'BatchItem.branch_price'
        db.delete_column(u'inventory_batchitem', 'branch_price')

        # Deleting field 'BatchItem.cost_price'
        db.delete_column(u'inventory_batchitem', 'cost_price')

        # Deleting field 'BatchItem.customer_bonus_quantity'
        db.delete_column(u'inventory_batchitem', 'customer_bonus_quantity')

        # Deleting field 'BatchItem.retail_price'
        db.delete_column(u'inventory_batchitem', 'retail_price')

        # Deleting field 'BatchItem.customer_card_price'
        db.delete_column(u'inventory_batchitem', 'customer_card_price')

        # Deleting field 'BatchItem.whole_sale_price'
        db.delete_column(u'inventory_batchitem', 'whole_sale_price')

        # Deleting field 'BatchItem.small_retail_price'
        db.delete_column(u'inventory_batchitem', 'small_retail_price')

        # Deleting field 'BatchItem.small_customer_card_price'
        db.delete_column(u'inventory_batchitem', 'small_customer_card_price')

        # Deleting field 'BatchItem.whole_sale_profit_percentage'
        db.delete_column(u'inventory_batchitem', 'whole_sale_profit_percentage')

        # Adding field 'BatchItem.created_date'
        db.add_column(u'inventory_batchitem', 'created_date',
                      self.gf('django.db.models.fields.DateField')(null='True', blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding model 'OpeningStockItem'
        db.create_table(u'inventory_openingstockitem', (
            ('selling_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('canteen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Canteen'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('batch_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.BatchItem'], null=True, blank=True)),
            ('opening_stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.OpeningStock'], null=True, blank=True)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5)),
            ('purchase_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5)),
            ('uom', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5)),
        ))
        db.send_create_signal(u'inventory', ['OpeningStockItem'])

        # Adding model 'Product'
        db.create_table(u'inventory_product', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Category'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Product'])

        # Adding model 'VatType'
        db.create_table(u'inventory_vattype', (
            ('vat_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('tax_percentage', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'inventory', ['VatType'])

        # Adding model 'OpeningStock'
        db.create_table(u'inventory_openingstock', (
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('canteen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Canteen'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'inventory', ['OpeningStock'])

        # Adding model 'Brand'
        db.create_table(u'inventory_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Brand'])

        # Adding field 'Item.offer_quantity'
        db.add_column(u'inventory_item', 'offer_quantity',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=50, decimal_places=5),
                      keep_default=False)

        # Adding field 'Item.uoms'
        db.add_column(u'inventory_item', 'uoms',
                      self.gf('jsonfield.fields.JSONField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.smallest_unit'
        db.add_column(u'inventory_item', 'smallest_unit',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.unit_per_packet'
        db.add_column(u'inventory_item', 'unit_per_packet',
                      self.gf('django.db.models.fields.DecimalField')(max_length=200, null=True, max_digits=50, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'Item.unit_per_piece'
        db.add_column(u'inventory_item', 'unit_per_piece',
                      self.gf('django.db.models.fields.DecimalField')(max_length=200, null=True, max_digits=50, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'Item.size'
        db.add_column(u'inventory_item', 'size',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.actual_smallest_uom'
        db.add_column(u'inventory_item', 'actual_smallest_uom',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.cess'
        db.add_column(u'inventory_item', 'cess',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2),
                      keep_default=False)

        # Adding field 'Item.product'
        db.add_column(u'inventory_item', 'product',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Product'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.unit_per_box'
        db.add_column(u'inventory_item', 'unit_per_box',
                      self.gf('django.db.models.fields.DecimalField')(max_length=200, null=True, max_digits=50, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'Item.brand'
        db.add_column(u'inventory_item', 'brand',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Brand'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.barcode'
        db.add_column(u'inventory_item', 'barcode',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.pieces_per_box'
        db.add_column(u'inventory_item', 'pieces_per_box',
                      self.gf('django.db.models.fields.DecimalField')(max_length=200, null=True, max_digits=50, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'Item.pieces_per_packet'
        db.add_column(u'inventory_item', 'pieces_per_packet',
                      self.gf('django.db.models.fields.DecimalField')(max_length=200, null=True, max_digits=50, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'Item.vat_type'
        db.add_column(u'inventory_item', 'vat_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.VatType'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.item_type'
        db.add_column(u'inventory_item', 'item_type',
                      self.gf('django.db.models.fields.CharField')(default='Stockable', max_length=50),
                      keep_default=False)

        # Adding field 'Item.packets_per_box'
        db.add_column(u'inventory_item', 'packets_per_box',
                      self.gf('django.db.models.fields.DecimalField')(max_length=200, null=True, max_digits=50, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'BatchItem.permissible_discount_percentage'
        db.add_column(u'inventory_batchitem', 'permissible_discount_percentage',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5),
                      keep_default=False)

        # Adding field 'BatchItem.small_wholesale_price'
        db.add_column(u'inventory_batchitem', 'small_wholesale_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=50, decimal_places=25),
                      keep_default=False)

        # Adding field 'BatchItem.small_branch_price'
        db.add_column(u'inventory_batchitem', 'small_branch_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=50, decimal_places=25),
                      keep_default=False)

        # Adding field 'BatchItem.salesman_bonus_quantity'
        db.add_column(u'inventory_batchitem', 'salesman_bonus_quantity',
                      self.gf('django.db.models.fields.FloatField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BatchItem.retail_profit_percentage'
        db.add_column(u'inventory_batchitem', 'retail_profit_percentage',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5),
                      keep_default=False)

        # Adding field 'BatchItem.freight_charge'
        db.add_column(u'inventory_batchitem', 'freight_charge',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5),
                      keep_default=False)

        # Adding field 'BatchItem.branch_price'
        db.add_column(u'inventory_batchitem', 'branch_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5),
                      keep_default=False)

        # Adding field 'BatchItem.cost_price'
        db.add_column(u'inventory_batchitem', 'cost_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=50, decimal_places=5),
                      keep_default=False)

        # Adding field 'BatchItem.customer_bonus_quantity'
        db.add_column(u'inventory_batchitem', 'customer_bonus_quantity',
                      self.gf('django.db.models.fields.FloatField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BatchItem.retail_price'
        db.add_column(u'inventory_batchitem', 'retail_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5),
                      keep_default=False)

        # Adding field 'BatchItem.customer_card_price'
        db.add_column(u'inventory_batchitem', 'customer_card_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5),
                      keep_default=False)

        # Adding field 'BatchItem.whole_sale_price'
        db.add_column(u'inventory_batchitem', 'whole_sale_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5),
                      keep_default=False)

        # Adding field 'BatchItem.small_retail_price'
        db.add_column(u'inventory_batchitem', 'small_retail_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=50, decimal_places=25),
                      keep_default=False)

        # Adding field 'BatchItem.small_customer_card_price'
        db.add_column(u'inventory_batchitem', 'small_customer_card_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=50, decimal_places=25),
                      keep_default=False)

        # Adding field 'BatchItem.whole_sale_profit_percentage'
        db.add_column(u'inventory_batchitem', 'whole_sale_profit_percentage',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=5),
                      keep_default=False)

        # Deleting field 'BatchItem.created_date'
        db.delete_column(u'inventory_batchitem', 'created_date')

    models = {
        u'dashboard.canteen': {
            'Meta': {'object_name': 'Canteen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.batch': {
            'Meta': {'object_name': 'Batch'},
            'canteen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Canteen']", 'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'inventory.batchitem': {
            'Meta': {'object_name': 'BatchItem'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Batch']", 'null': 'True', 'blank': 'True'}),
            'closing_stock': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consumed_quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '5'}),
            'created_date': ('django.db.models.fields.DateField', [], {'null': "'True'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']", 'null': 'True', 'blank': 'True'}),
            'purchase_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '50', 'decimal_places': '5'}),
            'quantity_in_actual_unit': ('django.db.models.fields.FloatField', [], {'default': '0', 'max_length': '100'}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '50', 'decimal_places': '5'}),
            'uom': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.category': {
            'Meta': {'object_name': 'Category'},
            'canteen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Canteen']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Category']", 'null': 'True', 'blank': 'True'})
        },
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'canteen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Canteen']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'uom': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.openingstockvalue': {
            'Meta': {'object_name': 'OpeningStockValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stock_by_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '5', 'blank': 'True'})
        },
        u'inventory.stockvalue': {
            'Meta': {'object_name': 'StockValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stock_by_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '5', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']