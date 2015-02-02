from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from views import Login, DashBoard, Logout, HelpView, SettingsView,\
 ResetPassword, ForgotPassword, PDCReport,CanteenList,AddCanteen,\
EditCanteen,DeleteCanteen,SearchCanteen

urlpatterns = patterns('',
	url(r'^login/$', Login.as_view(), name="login"),
	url(r'^logout/$', Logout.as_view(), name="logout"),
	url(r'^forgot_password/$', ForgotPassword.as_view(), name="forgot_password"),
	url(r'^reset_password/$', ResetPassword.as_view(), name="reset_password"),
	url(r'^canteen/$', CanteenList.as_view(), name="canteen"),
	url(r'^add_canteen/$', AddCanteen.as_view(), name="add_canteen"),
	url(r'^search_canteen/$', SearchCanteen.as_view(), name="add_canteen"),
	url(r'^edit_canteen/$', EditCanteen.as_view(), name="edit_canteen"),
	url(r'^delete_canteen/$', DeleteCanteen.as_view(), name="delete_canteen"),
	url(r'^$', login_required(DashBoard.as_view(), login_url='/login/'), name="dashboard"),
	url(r'^help/$', login_required(HelpView.as_view(), login_url='/login/'), name="help"),
	url(r'^settings/$', login_required(SettingsView.as_view(), login_url='/login/'), name="settings"),
	
)