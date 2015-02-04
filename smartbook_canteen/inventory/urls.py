from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from inventory.views import SearchBatch, SearchBatchItem, BatchList, AddBatch, DeleteBatch, Categories, AddCategory, \
	ItemList, AddItem, DeleteItem, SearchItem,\
	OpeningStockView, BatchItemDetailsView, DeleteCategory,ItemUom,\
	EditBatch, CategorySubcategoryList, SearchItemStock, BatchItemsView, IsCategoryNameExists, StockReport, \
	StockAgingReport, CategoryWiseStockReport, CategoryWiseStockAgingReport, CategoryWiseVendorReport, CategoryWisePurchaseReport, \
	CategoryWiseProfitReport, ClosingStockView


urlpatterns = patterns('',
	url(r'^categories/$', login_required(Categories.as_view(), login_url='/login/'),name='categories'),
	url(r'^subcategory_list/(?P<category_id>\d+)/$', login_required(CategorySubcategoryList.as_view(), login_url='/login/'), name='subcategory_list'),
	url(r'^add_category/$', login_required(AddCategory.as_view(), login_url='/login/'),name='add_category'),
	url(r'^delete_category/$', login_required(DeleteCategory.as_view(), login_url='/login/'),name='delete_category'),
	url(r'^is_category_name_exists/$', login_required(IsCategoryNameExists.as_view(), login_url='/login/'),name='is_category_name_exists'),

	url(r'^search_batch/$', login_required(SearchBatch.as_view(), login_url='/login/'), name='search_batch'),
	url(r'^search_batch_item/$', login_required(SearchBatchItem.as_view(), login_url='/login/'), name='search_batch_item'),

	url(r'^items/$', login_required(ItemList.as_view(), login_url='/login/'),name='items'),
	url(r'^add_item/$', login_required(AddItem.as_view(), login_url='/login/'),name='add_item'),
	url(r'^item_uoms/$', login_required(ItemUom.as_view(), login_url='/login/'), name='item_uoms'),
	url(r'^delete_item/$', login_required(DeleteItem.as_view(), login_url='/login/'),name='delete_item'),
	url(r'^search_item/$', login_required(SearchItem.as_view(), login_url='/login/'), name='search_item'),
	

	url(r'^batches/$', login_required(BatchList.as_view(), login_url='/login/'),name='batches'),
	url(r'^add_batch/$', login_required(AddBatch.as_view(), login_url='/login/'), name='add_batch'),
	url(r'^edit_batch/$', login_required(EditBatch.as_view(), login_url='/login/'), name='edit_batch'),
	url(r'^delete_batch/$', login_required(DeleteBatch.as_view(), login_url='/login/'), name='delete_batch'),
	url(r'^batch_item_details/$', login_required(BatchItemDetailsView.as_view(), login_url='/login/'), name="batch_item_details"),
	url(r'^batch_items/$', login_required(BatchItemsView.as_view(), login_url='/login/'), name="batch_items"),

	
	url(r'^opening_stock/$', login_required(OpeningStockView.as_view(), login_url='/login/'), name='opening_stock'),
	url(r'^search_item_stock/$', login_required(SearchItemStock.as_view(), login_url='/login/'), name='search_item_stock'),

	url(r'^stock_report/$', login_required(StockReport.as_view(), login_url='/login/'), name='stock_report'),
	url(r'^stock_aging_report/$', login_required(StockAgingReport.as_view(), login_url='/login/'), name='stock_aging_report'),
	url(r'^catergory_wise_stock_report/$', login_required(CategoryWiseStockReport.as_view(), login_url='/login/'), name='catergory_wise_stock_report'),
	url(r'^category_stock_aging_report/$', login_required(CategoryWiseStockAgingReport.as_view(), login_url='/login/'), name='category_stock_aging_report'),
	url(r'^category_purchase_report/$', login_required(CategoryWisePurchaseReport.as_view(), login_url='/login/'), name='category_purchase_report'),
	url(r'^category_vendor_report/$', login_required(CategoryWiseVendorReport.as_view(), login_url='/login/'), name='category_vendor_report'),
	url(r'^category_profit_report/$', login_required(CategoryWiseProfitReport.as_view(), login_url='/login/'), name='category_profit_report'),
	url(r'^closing_stock/$', login_required(ClosingStockView.as_view(), login_url='/login/'), name='closing_stock'),

)
