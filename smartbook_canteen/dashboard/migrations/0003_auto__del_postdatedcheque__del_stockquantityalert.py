# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PostDatedCheque'
        db.delete_table(u'dashboard_postdatedcheque')

        # Deleting model 'StockQuantityAlert'
        db.delete_table(u'dashboard_stockquantityalert')

        # Removing M2M table for field batch_items on 'StockQuantityAlert'
        db.delete_table('dashboard_stockquantityalert_batch_items')

    def backwards(self, orm):
        # Adding model 'PostDatedCheque'
        db.create_table(u'dashboard_postdatedcheque', (
            ('transaction_ref', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('cheque_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dashboard', ['PostDatedCheque'])

        # Adding model 'StockQuantityAlert'
        db.create_table(u'dashboard_stockquantityalert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dashboard', ['StockQuantityAlert'])

        # Adding M2M table for field batch_items on 'StockQuantityAlert'
        db.create_table(u'dashboard_stockquantityalert_batch_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stockquantityalert', models.ForeignKey(orm[u'dashboard.stockquantityalert'], null=False)),
            ('batchitem', models.ForeignKey(orm[u'inventory.batchitem'], null=False))
        ))
        db.create_unique(u'dashboard_stockquantityalert_batch_items', ['stockquantityalert_id', 'batchitem_id'])

    models = {
        u'dashboard.canteen': {
            'Meta': {'object_name': 'Canteen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dashboard']