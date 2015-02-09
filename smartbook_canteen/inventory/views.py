import simplejson
import ast
from datetime import datetime
import calendar

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm
from dashboard.models import Canteen
from inventory.models import Item, Batch, BatchItem, Category,StockValue, OpeningStockValue

style = [
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]
sales_receipt_style = [
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]
para_style = ParagraphStyle('fancy')
para_style.fontSize = 14
para_style.fontName = 'Helvetica'
# from accounts.models import Ledger, Transaction, LedgerEntry
# from purchases.models import Purchase, PurchaseItem
# from sales.models import Sale, SalesItem
# from suppliers.models import Supplier

def get_category_details(request, categories):
    
    category_list = []
    if request.is_ajax():
        for category in categories:
            category_list.append(category.get_json_data())
        res = {
            'categories': category_list,
        }
        return res
class SearchBatch(View):

    def get(self, request, *args, **kwargs):
        print 'hai';
        batch_name = request.GET.get('batch_name', '')
        print batch_name;
        # batch_item = BatchItem.objects.get(id=batch_name['id'])
        # print 'wowwww';
        # print batch_item;
        batches = Batch.objects.filter(name__istartswith=batch_name).filter(canteen=request.session['canteen']).filter(closed=False)
        
        batch_list = []
        # batches = Batch.objects.filter(canteen=request.session['canteen'])
        for batch in batches:

            batch_data = batch.get_json_data()
            batch_list.append(batch_data)
            print(batch_data)
        res = {
            'result': 'ok',
            'batches': batch_list,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class SearchBatchForReport(View):

    def get(self, request, *args, **kwargs):
        print 'hai';
        batch_name = request.GET.get('batch_name', '')
        print batch_name;
        # batch_item = BatchItem.objects.get(id=batch_name['id'])
        # print 'wowwww';
        # print batch_item;
        batches = Batch.objects.filter(name__istartswith=batch_name).filter(canteen=request.session['canteen'])
        batch_list = []
        # batches = Batch.objects.filter(canteen=request.session['canteen'])
        for batch in batches:

            batch_data = batch.get_json_data()
            batch_list.append(batch_data)
            print(batch_data)
        res = {
            'result': 'ok',
            'batches': batch_list,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')        

class SearchBatchItem(View):
    def get(self, request, *args, **kwargs):
        print("sss");
        batch_id = request.GET.get('batch_id', '')
        item_id = request.GET.get('item_id', '')
        print (batch_id,item_id);
        if item_id and batch_id:
            item = Item.objects.get(id=item_id)
            batch = Batch.objects.get(id=batch_id)
            print(item);
            print(batch);
            batch_items = BatchItem.objects.filter(item=item, batch=batch)
            print(batch_items)
            if batch_items:
                for batch_item in batch_items:
                    print(batch_item);
                    batch_item_data = batch_item.get_json_data();
            else :
                batch_item_data = {
                    'stock':0,
                    'purchase_price':0,
                    'selling_price':0,
                    'uom' : item.uom,
                }   
        res = {
            'result': 'ok',
            'batch_items': batch_item_data,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')


class BatchList(View):
    def get(self, request, *args, **kwargs):
        batch_list = []
        batches = Batch.objects.filter(canteen=request.session['canteen'])

        if request.is_ajax():
            for batch in batches:
                batch_list.append(batch.get_json_data())
            res = {
                'result': 'ok',
                'batches': batch_list,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'batch_list.html', {})

class AddBatch(View):

    def get(self, request, *args, **kwargs):
        batch_id = request.GET.get('batch_id', '')
        if request.is_ajax()and request.GET.get('batch_id', ''):
            batch = Batch.objects.get(id=batch_id)
            res = {
                'result': 'ok',
                'batch': batch.get_json_data(),
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'add_batch.html', {'batch_id' : batch_id})

    def post(self, request, *args, **kwargs):
        
        batch = None
        if request.is_ajax():
            batch_details = ast.literal_eval(request.POST['batch_details'])
            batch_details['canteen'] = request.session['canteen']
            print batch_details
            if batch_details.get('id', ''):
                batches = Batch.objects.filter(name=batch_details['name']).exclude(id=batch_details['id'])
                if batches.count() == 0:
                    batch = Batch.objects.get(id=batch_details['id'])
                    batch_details['canteen'] = request.session['canteen']
                    batch_obj = batch.set_attributes(batch_details)
                else:
                    res = {
                        'result': 'error',
                        'message': 'Batch with this name already exists',
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status=200, mimetype='application/json')
            else:
                try:
                    batch = Batch.objects.get(name=batch_details['name'])  
                    res = {
                        'result': 'error',
                        'message': 'Batch with this name already exists',
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status=200, mimetype='application/json')
                except Exception as ex:
                    batch = Batch()
                    batch_details['canteen'] = request.session['canteen'];
                    batch_details['name'] = str(batch_details['created_date']) + '-' + str(batch_details['created_date']) + '-' +str(request.session['canteen']);
                    print batch_details
                    print "hai"
                    batch_obj = batch.set_attributes(batch_details)
            res = {
                'result': 'ok',
                'id': batch.id,
                'name': batch.name,

            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
       

class EditBatch(View):

    def get(self, request, *args, **kwargs):
        batch_id = request.GET.get('batch_id', '')
        if request.is_ajax() and request.GET.get('batch_id', ''):
            batch = Batch.objects.get(id=batch_id)
            res = {
                'result': 'ok',
                'batch': batch.get_json_data(),
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'add_batch.html', {'batch_id' : batch_id})

class DeleteBatch(View):

    def get(self, request, *args, **kwargs):
        msg = ''
        batch_id = request.GET.get('batch_id', '')
        batch = Batch.objects.get(id=batch_id)
        batch_items = BatchItem.objects.filter(batch=batch)
        if batch_items:
            msg = 'Cannot delete this batch'
            return render(request, 'batch_list.html', {'msg' :msg })
        else:
            batch.delete()
        return HttpResponseRedirect(reverse('batches'))


class Categories(View):

    def get(self, request, *args, **kwargs):

        categories = Category.objects.filter(canteen=request.session['canteen'])
        print (categories);
        if request.GET.get('category_name', ''):
            categories = Category.objects.filter(Q(name__istartswith=request.GET.get('category_name', '')) & Q(canteen=request.session['canteen']));
            # print (categories);
        if request.is_ajax():
            if request.GET.get('tree', '') == 'true':
                print ("ssss");
                categories = Category.objects.filter(Q(parent=None) & Q(canteen=request.session['canteen'])).order_by('id') 
                
            res = get_category_details(request, categories)
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'category_tree_view.html', {'categories': categories})

class AddCategory(View):

    def post(self, request, *args, **kwargs):
        print(request.session['canteen']);
        if request.is_ajax(): 
            category_details = ast.literal_eval(request.POST['category'])
            if category_details.get('id', ''):
                category = Category.objects.get(id=category_details.get('id', ''))
                if category_details.get('parent_id', ''): 
                    category_obj = Category.objects.filter(parent__id=category_details['parent_id'],name=category_details['name']).exclude(id=category_details.get('id', ''))
                else:
                    category_obj = Category.objects.filter(name=category_details['name']).exclude(id=category_details.get('id', ''))
                if category_obj.count() == 0:
                    category_details['canteen']=request.session['canteen'];
                    # print (category_details);
                    category_obj = category.set_attributes(category_details)
                    res = {
                        'result': 'ok',
                        'edited_category': category.get_json_data(),
                        'new_category': {}
                    }
                else:
                    res = {
                        'result': 'error',
                        'message': 'Category name already exists',
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status=200, mimetype='application/json')
            else:
                try:
                    if category_details['parent_id'] != '': 
                        parent = Category.objects.get(id=category_details['parent_id'])
                        category = Category.objects.get(name=category_details['name'], parent=parent)
                    else:
                        category = Category.objects.get(name=category_details['name'])
                    res = {
                        'result': 'error',
                        'message': 'Category name already exists',
                    }
                except Exception as ex:
                    
                    category = Category()
                    category_details['canteen']=request.session['canteen'];
                    # print (category_details);
                    category_obj = category.set_attributes(category_details)
                    res = {
                        'result': 'ok',
                        'message': 'ok',
                        'new_category': category.get_json_data()
                    }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

class CategorySubcategoryList(View):

    def get(self, request, *args, **kwargs):
        print("hiii");
        category_data={};
        category_id = kwargs['category_id']
        print (category_id)
        category = Category.objects.filter(id=category_id)
        print (category);
        ctx_category_details = []
        ctx_subcategory = []
        subcategories = Category.objects.filter(Q(parent=category) & Q(canteen=request.session['canteen']))
        print(subcategories);
        for subcatrgory in subcategories:
            ctx_subcategory.append(subcatrgory.get_json_data())
        # category_data = category.get_json_data()
        category_data['subcategories'] = ctx_subcategory
        ctx_category_details.append(category_data)
        res = {
            'result': 'ok',
            'subcategories': ctx_subcategory,
            'category_details': ctx_category_details
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class ItemList(View):

    def get(self, request, *args, **kwargs):       
        if request.is_ajax():
            items_list = []
            items = Item.objects.filter(canteen=request.session['canteen']).order_by('name')
            for item in items:
                item_data = item.get_json_data()                
                items_list.append(item_data)
                print(items_list)
            res = {
                'result': 'ok',
                'items': items_list,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'item_list.html', {})   

class AddItem(View):

    def get(self, request, *args, **kwargs):
        
        category_list=[];
        categories=Category.objects.filter(canteen=request.session['canteen'])
        for category in categories:
            category_data = category.get_json_data()
            category_list.append(category_data)
            print(category_list)
        return render(request, 'add_inventory_item.html', {'categories':category_list})

    def post(self, request, *args, **kwargs):
        print("232");
        item_details = ast.literal_eval(request.POST['item'])
        print(item_details);
        if item_details.get('id', ''):
         
            item = Item.objects.get(id=item_details['id'])
            item_obj = item.set_attributes(item_details)
        else:
            item = Item()
            item_details['canteen']=request.session['canteen'];
            print item_details;
            item_obj = item.set_attributes(item_details)
        # item_data = item_obj.get_json_data()
        res = {
            'result': 'ok',
            'item': item_obj.get_json_data()
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')       
                    
class DeleteItem(View):

    def get(self, request, *args, **kwargs):
        
        item_id = request.GET.get('item_id','')
        msg = ''
        item = Item.objects.get(id=item_id)
        if item.batchitem_set.all().count() == 0:
            item.delete()
        else:
            msg = "Item cannot be deleted"
            return render(request, 'item_list.html', {'msg':msg})
        return HttpResponseRedirect(reverse('items'))
        

class SearchItem(View):

    def get(self, request, *args, **kwargs):
        items_list = []
        try:
            item_code = request.GET.get('item_code', '')
            item_name = request.GET.get('item_name', '')
            print ("hii");
            print(item_name);
            items = []
            if item_code:
                items = Item.objects.filter(code__istartswith=item_code)
            elif item_name:
                items = Item.objects.filter(Q(name__istartswith=item_name) &Q(canteen=request.session['canteen']));
                print (items);
            for item in items: 
                quantity_in_purchase_unit = 0;
                purchase_price = 0
                quantity_in_smallest_unit = 0
                purchase_price = 0
                cost_price = 0
                uom = ''
                item_name = ''
                batch_name = ''
                wholesale_profit = 0
                retail_profit = 0
                wholesale_price = 0
                retail_price = 0
                branch_price = 0
                customer_card_price = 0
                permissible_discount = 0
                stock = 0
                is_cost_price_existing = 'false'
                is_wholesale_profit = 'false'
                is_retail_profit = 'false'
                is_branch_price = 'false'
                is_customer_card_price = 'false'
                is_permissible_discount = 'false'
                
                item_data = item.get_json_data()
                item_data['purchase_price'] = purchase_price
                item_data['quantity_in_purchase_unit'] = quantity_in_purchase_unit
                item_data['purchase_price'] = purchase_price
                item_data['cost_price'] = cost_price
                item_data['uom'] = uom
                item_data['item_name'] = item_name
                item_data['batch_name'] = batch_name
                item_data['wholesale_profit'] = wholesale_profit
                item_data['retail_profit'] = retail_profit
                item_data['wholesale_price'] = wholesale_price
                item_data['retail_price'] = retail_price
                item_data['branch_price'] = branch_price
                item_data['customer_card_price'] = customer_card_price
                item_data['permissible_discount'] = permissible_discount
                item_data['is_cost_price_existing'] = is_cost_price_existing
                item_data['is_wholesale_profit'] = is_wholesale_profit
                item_data['is_retail_profit'] = is_retail_profit
                item_data['is_branch_price'] = is_branch_price
                item_data['is_customer_card_price'] = is_customer_card_price
                item_data['is_permissible_discount'] = is_permissible_discount
                items_list.append(item_data)
                print items_list;                           
            res = {
                'result': 'ok',
                'items': items_list,
            }
        except Exception as ex:
            res = {
                'result': 'error',
                'error_message': str(ex),
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class ItemUom(View):

    def get(self, request, *args, **kwargs):

        if request.is_ajax():
            item_id = request.GET.get('item')
            item = Item.objects.get(id=item_id)
            uom_list = []
            uom_list.append({
                'uom': item.uom,
            })
            if item.packets_per_box != None:
                uom_list.append({
                    'uom': 'packet',
                })
            if item.pieces_per_packet != None or item.pieces_per_box != None:
                uom_list.append({
                    'uom': 'piece',
                })
            if item.smallest_unit != item.uom and item.smallest_unit != 'packet' and item.smallest_unit != 'piece':
                uom_list.append({
                    'uom': item.smallest_unit if item.smallest_unit else '',
                })
            for uom in uom_list:
                if uom['uom'] == 'Kg':
                    uom_list.append({
                        'uom': 'gm',
                    })
                    uom_list.append({
                        'uom': 'mg',
                    })
                elif uom['uom'] == 'Metre':
                    uom_list.append({
                        'uom': 'cm',
                    })
                    uom_list.append({
                        'uom': 'mm',
                    })
                elif uom['uom'] == 'litre':
                    uom_list.append({
                        'uom': 'ml',
                    })
            res = {
                'uoms': uom_list,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')        

class UOMConversionView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            uom_list = settings.UOM
            res = {
                'result': 'ok',
                'uoms': uom_list,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

class DeleteCategory(View):

    def get(self, request, *args, **kwargs):

        category_id = request.GET.get('category_id', '')
        category = Category.objects.get(id=category_id)
        if category.product_set.all().count() == 0:
            category.delete()
        return HttpResponseRedirect(reverse('categories'))


class OpeningStockView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'opening_stock.html', {})

    def post(self, request, *args, **kwargs):

        total_purchase_price = 0
        if request.is_ajax():
            opening_stock_items = ast.literal_eval(request.POST['opening_stock_items'])
            print(opening_stock_items);
            if opening_stock_items:
                try:
                    print(request.session['canteen']);
                    # opening_stock = OpeningStock.objects.create(date=datetime.now(),canteen=request.session['canteen'] )
                    print("dsfdsf");
                    for item_detail in opening_stock_items:
                        print (item_detail);
                        try:
                            uom =  item_detail['purchase_unit']
                            purchase_unit = uom['uom']
                        except:
                            purchase_unit = item_detail['purchase_unit']
                        item = Item.objects.get(id=item_detail['id'])
                        batch = Batch.objects.get(id=item_detail['batch'])
                        print(purchase_unit);
                        print(item,batch);
                        batch_item, batch_item_created = BatchItem.objects.get_or_create(item=item,batch=batch)
                        canteen=Canteen.objects.get(id=request.session['canteen']);
                        print(batch_item,batch_item_created,canteen);
                        
                        quantity = 0
                        selling_price = 0
                        purchase_price = 0  
                        if batch_item_created:
                            print("vvv");
                            batch_item.purchase_price = item_detail['purchase_price']
                            batch_item.selling_price = item_detail['selling_price']
                            batch_item.consumed_quantity = 0
                            batch_item.closing_stock = 0
                            batch_item.uom = purchase_unit
                            batch_item.stock = float(batch_item.stock)+float(item_detail['quantity'])
                            total_purchase_price = float(total_purchase_price) + float(item_detail['net_amount'])
                            batch_item.save()
                        else :
                            print("qqqq");
                            batch_item.purchase_price = item_detail['purchase_price']
                            batch_item.selling_price = item_detail['selling_price']
                            batch_item.uom = purchase_unit
                            batch_item.stock = float(batch_item.stock)+float(item_detail['quantity'])
                            total_purchase_price = float(total_purchase_price) + float(item_detail['net_amount'])
                            batch_item.save()    
                except Exception as ex:
                    res = {
                        'result': 'error',
                        'error_message': str(ex),
                    }
                # ledger_entry_cash_ledger = LedgerEntry()
                # ledger_entry_cash_ledger.ledger = cash_ledger
                # ledger_entry_cash_ledger.credit_amount = total_purchase_price
                # ledger_entry_cash_ledger.date = datetime.now()
                # ledger_entry_cash_ledger.transaction_reference_number = transaction.transaction_ref
                # ledger_entry_cash_ledger.save()
                # ledger_entry_stock_ledger = LedgerEntry()
                # ledger_entry_stock_ledger.ledger = stock_ledger
                # ledger_entry_stock_ledger.debit_amount = total_purchase_price
                # ledger_entry_stock_ledger.date = datetime.now()
                # ledger_entry_stock_ledger.transaction_reference_number = transaction.transaction_ref 
                # ledger_entry_stock_ledger.save()
                try:
                    stock_value = StockValue.objects.latest('id')
                except Exception as ex:
                    stock_value = StockValue()
                if stock_value.stock_by_value is not None:
                    stock_value.stock_by_value = float(stock_value.stock_by_value) + float(total_purchase_price)
                else:
                    stock_value.stock_by_value = float(total_purchase_price)
                stock_value.save()
                try:
                    opening_stock_value = OpeningStockValue.objects.latest('id')
                except Exception as ex:
                    opening_stock_value = OpeningStockValue()
                if opening_stock_value.stock_by_value is not None:
                    opening_stock_value.stock_by_value = float(opening_stock_value.stock_by_value) + float(total_purchase_price)
                else:
                    opening_stock_value.stock_by_value = float(total_purchase_price)
                opening_stock_value.save()
                
            res = {
                'result': 'ok',
                'transaction_reference_no':'tyryty',
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

class BatchItemDetailsView(View):

    def get(self, request, *args, **kwargs):

        batch_id = request.GET.get('batch_id', '')
        item_id = request.GET.get('item_id', '')
        try:
            batch_item = BatchItem.objects.get(batch__id=batch_id, item__id=item_id)
            res = {
                'result': 'ok',
                'batch_item': batch_item.get_json_data()
            }
        except Exception as ex:
            print ex
            res = {
                'result': 'error',
                'batch_item': {}
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class SearchItemStock(View):
    def get(self, request, *args, **kwargs):
        try:
            item_id = request.GET.get('id', '')
            item_dict = []
            if item_id:
                item = Item.objects.get(id=item_id)
            batch_items = item.batchitem_set.all()
            for batch_item in batch_items:
                item_dict.append({
                    'id': item.id,
                    'name': item.name,
                    'item_name': str(item.name),
                    'category': item.product.category.name,
                    'code': item.code,
                    'product_name': item.product.name,
                    'brand_name': item.brand.name,                  
                    'stock': batch_item.get_json_data()['stock'], 
                    'batch': batch_item.batch.name,
                    'uom': batch_item.uom,
                    'size': item.size
                })  
                    
            res = {
                'result': 'ok',
                'items': item_dict,
            }
        except Exception as ex:
            res = {
                'result': 'error',
                'error_message': str(ex),
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class BatchItemsView(View):

    def get(self, request, *args, **kwargs):
        batch_id = request.GET.get('batch_id', '')
        batch_item_list = []
        try:
            batch_items = BatchItem.objects.filter(batch__id=batch_id)
            for item in batch_items:
                batch_item_list.append(item.get_json_data())
            res = {
                'result': 'ok',
                'batch_items': batch_item_list,
            }
        except Exception as ex:
            print str(ex)
            res = {
                'result': 'error',
                'batch_items': []
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class IsCategoryNameExists(View):

    def get(self, request, *args, **kwargs):

        if request.GET.get('name', ''):
            categories = Category.objects.filter(name=request.GET.get('name', ''))
            if categories.count() > 0:
                res = {
                    'result': 'error',
                    'message': 'Category with this name already exists',
                }
            else:
                res = {
                    'result': 'ok',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

class StockReport(View):

    def get(self, request, *args, **kwargs):

        batch_id = request.GET.get('batch_id', '')
        flag = request.GET.get('pdf', '')
        print batch_id;
        print flag;
        total_purchase_price=0;
        total_selling_price=0;
        batch_item_details = []
        batch_data=[]
        if batch_id:
            if flag == 'false':
                print("dsds");
                batch_list = Batch.objects.get(id=batch_id)
                print batch_list;
                batch_data.append(batch_list.get_json_data())
                batch_items = BatchItem.objects.filter(batch=batch_list)
                print batch_items;
                for batch_item in batch_items:
                    batch_item_details.append(batch_item.get_json_data())
                    
                print batch_item_details;
                for batch_total in batch_item_details:
                    total_purchase_price = float(total_purchase_price) + (float(batch_total['stock'])*float(batch_total['purchase_price']))
                    total_selling_price = float(total_selling_price) + (float(batch_total['consumed_quantity'])*float(batch_total['selling_price']))
                print 'jingaaaa';
                print total_purchase_price;
                if request.is_ajax():
                    res = {
                        'result': 'ok',
                        'batch': batch_data,
                        'batch_items': batch_item_details,
                        'total_purchase_price':total_purchase_price,
                        'total_selling_price':total_selling_price,
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status=200, mimetype='application/json')
            if flag == 'true':        
                print("oooo");
                total_purchase_price=0;
                total_selling_price=0;
                batch = Batch.objects.get(id=batch_id)
                batch_data = batch.get_json_data()
                print batch_data['closed_flag'];

                if batch_data['closed_flag'] == True:
                    print("false")
                    batch_items = BatchItem.objects.filter(batch=batch)
                    print batch_items;
                    for batch_item in batch_items:
                        batch_item_details.append(batch_item.get_json_data())
                    print batch_item_details;
                    print(request.GET.get('pdf', ''));
                    current_date = datetime.now().strftime('%d-%m-%Y')
                    style = [
                        ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
                    ]
                    response = HttpResponse(content_type='application/pdf')
                    p = SimpleDocTemplate(response, pagesize=A4)
                    elements = []
                    d = [['Stock Report'+' '+str(current_date)]]
                    t = Table(d, colWidths=(450), rowHeights=25, style=style)
                    t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTSIZE', (0,0), (-1,-1), 12),
                        ])   
                    elements.append(t)
                    data2 = []
                    blank2="";
                    data2.append([blank2])
                
                    table2 = Table(data2, colWidths=(100), style=style)
                    table2.setStyle([
                            ('FONTSIZE', (0,0), (-1,-1), 11),
                            ])   
                    elements.append(table2) 
                    data = []
                    para_style = ParagraphStyle('fancy')
                    para_style.fontSize = 10
                    para_style.fontName = 'Helvetica'
                    data.append(['Item', 'Item code', 'Stock', 'Consumed Quantity', 'Closing Stock','Purchase Price','Selling price'])
                    table = Table(data, colWidths=(80, 80, 50, 110,80,80,80), style=style)
                    table.setStyle([
                        ('FONTSIZE', (0,0), (-1,0), 11),
                        ])  
                    elements.append(table)
                    elements.append(Spacer(1,.1*cm ))
                    data = []
                    for batch_item in batch_item_details:
                        total_purchase_price = float(total_purchase_price) + (float(batch_item['stock'])*float(batch_item['purchase_price']))
                        total_selling_price = float(total_selling_price) + (float(batch_item['consumed_quantity'])*float(batch_item['selling_price']))
                        item_name = Paragraph(batch_item['item_name'], para_style)
                        item_code = Paragraph(batch_item['code'], para_style)
                        stock = Paragraph(str(batch_item['stock']), para_style)
                        consumed_quantity = Paragraph(str(batch_item['consumed_quantity']), para_style)
                        closing_stock = Paragraph(str(batch_item['closing_stock']), para_style)
                        purchase_price = Paragraph(str(batch_item['purchase_price']), para_style)
                        selling_price = Paragraph(str(batch_item['selling_price']), para_style)
                        data.append([item_name, item_code,stock,consumed_quantity,closing_stock,purchase_price,selling_price])
                    if len(data) > 0:
                        table = Table(data, colWidths=(80, 80, 50, 110,80,80,80), style=style)
                        elements.append(table)
                    data0 = []
                    blank="";
                    data0.append([blank])
                    data0.append([blank])
                    table0 = Table(data0, colWidths=(100), style=style)
                    table0.setStyle([
                                ('FONTSIZE', (0,0), (-1,-1), 11),
                                ])   
                    elements.append(table0)   
                    data1 = []
                    data1.append(['Total  Purchase Price :', total_purchase_price])
                    data1.append(['Total Consumed Quantity Price :', total_selling_price])
                    table1 = Table(data1, colWidths=(200, 110), style=style)
                    table1.setStyle([
                                ('FONTSIZE', (0,0), (-1,-1), 11),
                                ])   
                    elements.append(table1)    
                    p.build(elements)  
                    return response 

                else:
                    print("true")
                    batch_items = BatchItem.objects.filter(batch=batch)
                    print batch_items;
                    for batch_item in batch_items:
                        batch_item_details.append(batch_item.get_json_data())
                    print batch_item_details;
                    print(request.GET.get('pdf', ''));
                    current_date = datetime.now().strftime('%d-%m-%Y')
                    style = [
                        ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
                    ]
                    response = HttpResponse(content_type='application/pdf')
                    p = SimpleDocTemplate(response, pagesize=A4)
                    elements = []
                    d = [['Stock Report'+' '+str(current_date)]]
                    t = Table(d, colWidths=(450), rowHeights=25, style=style)
                    t.setStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTSIZE', (0,0), (-1,-1), 12),
                        ])   
                    elements.append(t)
                    data2 = []
                    blank2="";
                    data2.append([blank2])
                
                    table2 = Table(data2, colWidths=(100), style=style)
                    table2.setStyle([
                            ('FONTSIZE', (0,0), (-1,-1), 11),
                            ])   
                    elements.append(table2) 
                    data = []
                    para_style = ParagraphStyle('fancy')
                    para_style.fontSize = 10
                    para_style.fontName = 'Helvetica'
                    data.append(['Item', 'Item code', 'Stock', 'Consumed Quantity','Purchase Price','Selling price'])
                    table = Table(data, colWidths=(80, 80, 50, 110,80,80), style=style)
                    table.setStyle([
                        ('FONTSIZE', (0,0), (-1,0), 11),
                        ])  
                    elements.append(table)
                    elements.append(Spacer(1,.1*cm ))
                    data = []
                    for batch_item in batch_item_details:
                        total_purchase_price = float(total_purchase_price) + (float(batch_item['stock'])*float(batch_item['purchase_price']))
                        total_selling_price = float(total_selling_price) + (float(batch_item['consumed_quantity'])*float(batch_item['selling_price']))
                        item_name = Paragraph(batch_item['item_name'], para_style)
                        item_code = Paragraph(batch_item['code'], para_style)
                        stock = Paragraph(str(batch_item['stock']), para_style)
                        consumed_quantity = Paragraph(str(batch_item['consumed_quantity']), para_style)
                        # closing_stock = Paragraph(str(batch_item['closing_stock']), para_style)
                        purchase_price = Paragraph(str(batch_item['purchase_price']), para_style)
                        selling_price = Paragraph(str(batch_item['selling_price']), para_style)
                        data.append([item_name, item_code,stock,consumed_quantity,purchase_price,selling_price])
                    if len(data) > 0:
                        table = Table(data, colWidths=(80, 80, 50, 110,80,80), style=style)
                        elements.append(table)
                    data0 = []
                    blank="";
                    data0.append([blank])
                    data0.append([blank])
                    table0 = Table(data0, colWidths=(100), style=style)
                    table0.setStyle([
                                ('FONTSIZE', (0,0), (-1,-1), 11),
                                ])   
                    elements.append(table0)   
                    data1 = []
                    data1.append(['Total  Purchase Price :', total_purchase_price])
                    # data1.append(['Total Consumed Quantity Price :', total_selling_price])
                    table1 = Table(data1, colWidths=(200, 110), style=style)
                    table1.setStyle([
                                ('FONTSIZE', (0,0), (-1,-1), 11),
                                ])   
                    elements.append(table1)    
                    p.build(elements)  
                    return response         
        return render(request, 'stock_report.html', {})

class ClosingStockView(View):

    def get(self, request, *args, **kwargs):

        batch_id = request.GET.get('batch_id', '')
        print batch_id;
        batch_item_details = []
        if batch_id:
            batch = Batch.objects.get(id=batch_id)
            print batch;
            batch_items = BatchItem.objects.filter(batch=batch)
            print batch_items;
            for batch_item in batch_items:

                batch_item_details.append(batch_item.get_json_data())
            print batch_item_details;

            if request.is_ajax():
                res = {
                    'result': 'ok',
                    'batch_items': batch_item_details,
                }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'closing_stock.html', {})

    def post(self, request, *args, **kwargs):

        closing_stock = 0
        print 'hello';
        if request.is_ajax():
            closing_stock_details = ast.literal_eval(request.POST['closing_stock_items'])
            print closing_stock_details;
        canteen=Canteen.objects.get(id=request.session['canteen']); 
        new_batch,batch_created = Batch.objects.get_or_create(created_date=datetime.now().date())
        print(new_batch,batch_created)
        new_batch.canteen = canteen
        new_batch.save()
        new_batch.set_name()
        if closing_stock_details:
            for item_detail in closing_stock_details:                
                batch_item = BatchItem.objects.get(id=item_detail['id'])
                batch_item.consumed_quantity = item_detail['consumed_quantity']
                batch_item.closing_stock = item_detail['closing_stock']
                batch_item.save()
                if batch_item.closing_stock > 0:

                    new_batch_item, created = BatchItem.objects.get_or_create(item=batch_item.item, batch=new_batch)
                    new_batch_item.stock = batch_item.closing_stock
                    new_batch_item.purchase_price = batch_item.purchase_price
                    new_batch_item.selling_price = batch_item.selling_price
                    new_batch_item.closing_stock = 0
                    new_batch_item.consumed_quantity = 0
                    new_batch_item.uom = batch_item.uom
                    print(new_batch_item);
                    new_batch_item.save()
        batch_item.batch.closed = True
        batch_item.batch.save()
        new_batch.closed = False
        new_batch.save()
        res = {
            'result': 'ok',
                
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')
               
