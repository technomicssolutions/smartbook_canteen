function DashboardController($scope, $http) {
    $scope.init = function(csrf_token) {
        console.log('hai');
    }
}

function get_Canteen_list($scope, $http){
	$http.get('/canteen/').success(function(data){
       
        if (data.result == 'ok') {
            if (data.canteens.length > 0) {
                $scope.canteens = data.canteens;
                $scope.message = data.message;
            }
        } else{
        	
            $scope.message = data.message;
        }
    }).error(function(data, status){
    	
        $scope.message = data.message;
    })
}


function get_canteen_search_details($scope, $http, from) {
	
    $scope.canteens = [];
    $scope.no_canteen_msg = '';
    
    if ($scope.canteen_name != '' && $scope.canteen_name != undefined && $scope.canteen_name.length > 0) {
        var canteen_name = $scope.canteen_name;
       
        $http.get('/search_canteen/?canteen_name='+canteen_name).success(function(data){
           
            $scope.no_canteeen_msg = '';
            if (data.canteens.length == 0) {
                $scope.no_canteen_msg = 'No such canteen';
            }
            else {
                $scope.canteens = data.canteens;
                $scope.no_canteen_msg = '';
            }
           
        }).error(function(data, status){
            console.log('Request failed'|| data);
        });
    }
}

function CanteenController($scope, $http){
    $scope.canteen = {
        'id': '',
        'name': '',
    }
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        get_Canteen_list($scope, $http);
    }
    $scope.create_new = function() {
        document.location.href = '/add_canteen/';
    }
    $scope.save_canteen = function() {
        save_canteen($scope, $http);
    }
    $scope.view_canteen = function(canteen){
        $scope.canteen = canteen;
        create_popup();
    }
    $scope.edit_canteen_details = function(canteen) {
        $scope.canteen = canteen;
        document.location.href = '/edit_canteen/?canteen_id='+canteen.id
    }
    $scope.delete_canteen = function(canteen) {
        document.location.href = '/delete_canteen/?canteen_id='+canteen.id;
    }
    $scope.get_canteen_list = function() {
    	
        get_canteen_search_details($scope, $http);
    }
    $scope.hide_popup = function() {
        hide_popup();
    }
    $scope.save_canteen = function() {
    	if ($scope.validate_canteen())
    		 params = {
            'canteen_details': angular.toJson($scope.canteen),
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        $http({
            method:'post',
            url: '/add_canteen/',
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data){
        	if (data.result == 'ok'){
        		document.location.href = '/canteen/';
        	}
        	else {
                $scope.validate_canteen_error_msg = data.message;
            }   
        }).error(function(data, status){
            console.log('Request failed' || data);
        });

    }

    $scope.validate_canteen = function() {
    if ($scope.canteen.name == '' || $scope.canteen.name == undefined) {
        $scope.validate_canteen_error_msg = 'Please enter the canteen name';
        return false;
    } return true;
   }
}  





       