# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'cashEntry.cash'
        db.delete_column(u'inventory_cashentry', 'cash')

        # Adding field 'cashEntry.amount'
        db.add_column(u'inventory_cashentry', 'amount',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=5, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'cashEntry.cash'
        db.add_column(u'inventory_cashentry', 'cash',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=20, decimal_places=5, blank=True),
                      keep_default=False)

        # Deleting field 'cashEntry.amount'
        db.delete_column(u'inventory_cashentry', 'amount')

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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
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
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '50', 'decimal_places': '5'}),
            'stock': ('django.db.models.fields.FloatField', [], {'default': '0', 'max_length': '100'}),
            'uom': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'inventory.cashentry': {
            'Meta': {'object_name': 'cashEntry'},
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '20', 'decimal_places': '5', 'blank': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Batch']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': "'True'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Category']", 'null': 'True', 'blank': 'True'}),
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