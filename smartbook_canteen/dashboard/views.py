import simplejson
import ast
from datetime import datetime
import calendar
from operator import itemgetter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from num2words import num2words

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from sales.models import Sale, SalesItem
# from purchases.models import Purchase, PurchaseReturn
# from accounts.models import Ledger, LedgerEntry
from inventory.models import Category
from dashboard.models import Canteen

style = [
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]
sales_receipt_style = [
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]
para_style = ParagraphStyle('fancy')
para_style.fontSize = 10.5
para_style.fontName = 'Helvetica'




class Login(View):
    def get(self, request, *args, **kwargs):
        canteen_list = []
        canteens = Canteen.objects.all()
        print (canteens);
        print("sss")
        for canteen in canteens:
            print (canteen);
            canteen_list.append(canteen.get_json_data())
        res = {
            'result': 'ok',
            'canteens': canteen_list,
         }
        return render(request, 'login.html', res)

    def post(self, request, *args, **kwargs):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        request.session['canteen'] = request.POST['canteen']
        print request.session['canteen']
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            context = {
                'message' : 'Username or password is incorrect',
                'username': request.POST['username']
            }
            return render(request, 'login.html', context)

class DashBoard(View):

    def get(self, request, *args, **kwargs):
        current_date = datetime.now().date()
        return render(request, 'dashboard.html', {'current_date': current_date})


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))

class CanteenList(View):

    def get(self, request, *args, **kwargs):
        canteen_list = []
        canteens = Canteen.objects.all()
        print (canteens);
        print("sss")
        for canteen in canteens:
            print (canteen);
            canteen_list.append(canteen.get_json_data())
        res = {
            'result': 'ok',
            'canteens': canteen_list,
         }
        response = simplejson.dumps(res)
        if request.is_ajax():
            print("ajax");
            res = {
            'result': 'ok',
            'canteens': canteen_list,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        # return HttpResponse(response, status=200, mimetype='application/json')    
        return render(request, 'canteen_list.html', {})



class AddCanteen(View):

    def get(self, request, *args, **kwargs):
        canteen_id = request.GET.get('canteen_id', '')
        if request.is_ajax()and request.GET.get('canteen_id', ''):
            canteen = Canteen.objects.get(id=canteen_id)
            res = {
                'result': 'ok',
                'canteens': canteen.get_json_data(),
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'add_canteen.html', {'canteen_id' : canteen_id})

    def post(self, request, *args, **kwargs):
        
        canteen = None
        if request.is_ajax():
            canteen_details = ast.literal_eval(request.POST['canteen_details'])
            if canteen_details.get('id', ''):
                canteens = Canteen.objects.filter(name=canteen_details['name']).exclude(id=canteen_details['id'])
                if canteens.count() == 0:
                    canteen = Canteen.objects.get(id=canteen_details['id'])
                    canteen_obj = canteen.set_attributes(canteen_details)
                else:
                    res = {
                        'result': 'error',
                        'message': 'canteen with this name already exists',
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status=200, mimetype='application/json')
            else:
                try:
                    canteen = Canteen.objects.get(name=canteen_details['name'])  
                    res = {
                        'result': 'error',
                        'message': 'Canteen with this name already exists',
                    }
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status=200, mimetype='application/json')
                except Exception as ex:
                    canteen = Canteen()
                    canteen_obj = canteen.set_attributes(canteen_details)
            res = {
                'result': 'ok',
                'id': canteen.id,
                'name': canteen.name,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

class EditCanteen(View):

    def get(self, request, *args, **kwargs):
        canteen_id = request.GET.get('canteen_id', '')
        print (canteen_id);
        if request.GET.get('canteen_id', ''):
            print("hii");
            canteen = Canteen.objects.get(id=canteen_id)
            res = {
                'result': 'ok',
                'canteen': canteen.get_json_data(),
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'add_canteen.html', {'canteen_id' : canteen_id})

class DeleteCanteen(View):

    def get(self, request, *args, **kwargs):
        msg = ''
        canteen_id = request.GET.get('canteen_id', '')
        print (canteen_id);
        canteen = Canteen.objects.get(id=canteen_id)
        canteen.delete()
        return HttpResponseRedirect(reverse('canteen'))         

class SearchCanteen(View):

    def get(self, request, *args, **kwargs):

        canteen_name = request.GET.get('canteen_name', '')
        print (canteen_name);
        canteens = Canteen.objects.filter(name__istartswith=canteen_name)
        canteen_list = []
        for canteen in canteens:
            canteen_data = canteen.get_json_data()
            canteen_list.append(canteen_data)
        res = {
            'result': 'ok',
            'canteens': canteen_list,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')
class HelpView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'help.html', {})

class SettingsView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'settings.html', {})

        
class ResetPassword(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'reset_password.html', {})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            pass_dict = request.POST
            user = request.user
            user.set_password(pass_dict['new_password'])
            user.save()
            res = {
                'result': 'ok',
                'message': 'Password Changed Successfully',
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'reset_password.html', {})

class ForgotPassword(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'forgot_password.html', {})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            pass_dict = request.POST
            try:
                user = User.objects.get(username=pass_dict['username'])
                user.set_password(pass_dict['new_password'])
                user.save()
                res = {
                    'result': 'ok',
                    'message': 'Password Changed Successfully',
                }
            except:
                res = {
                    'result': 'ok',
                    'message': 'User Doest Not Exists',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'reset_password.html', {})

# 