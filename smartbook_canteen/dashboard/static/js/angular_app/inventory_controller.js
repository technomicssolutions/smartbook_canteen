function hide_inventory_item_popup_div($scope) {
    $('#add_brand').css('display', 'none');
    $('#add_product').css('display', 'none');
    $('#add_vat').css('display', 'none');
    $('#stock_search_popup').css('display', 'none');
}
function hide_opening_stock_popup_divs() {
    $('#new_batch').css('display', 'none');
    $('#add_item').css('display', 'none');
    $('#add_brand').css('display', 'none');
    $('#add_vat').css('display', 'none');
    $('#add_product').css('display', 'none');
    $('#transaction_reference_no_details').css('display', 'none');
}
function hide_item_popups($scope) {
    $('#add_item').css('display', 'none');
    $('#view_item').css('display', 'none');
    $('#stock_search_popup').css('display', 'none');
}

function get_batches($scope, $http){
   
    $http.get('/inventory/batches/?ajax=true').success(function(data){

        $scope.batches = data.batches;
        if ($scope.batches.length > 0) {
            paginate($scope.batches, $scope, 15);
        } 
    }).error(function(data, status){
        $scope.message = data.message;
    })
}
function search_batch($scope, $http){
    $scope.no_batch_msg = '';
    $scope.batches = [];
    $http.get('/inventory/search_batch/?batch_name='+$scope.batch_name+'&ajax=true').success(function(data){
        $scope.batches = data.batches;
        console.log($scope.batches)
        if ($scope.batches.length == 0) {
            $scope.no_batch_msg = 'No batch with this name';
        }
        paginate($scope.batches, $scope, 10);
    }).error(function(data, status){
        console.log('Request failed');
    });
}

function search_batch_for_report($scope, $http){
    $scope.no_batch_msg = '';
    $scope.batches = [];
    $http.get('/inventory/search_batch_for_report/?batch_name='+$scope.batch_name+'&ajax=true').success(function(data){
        $scope.batches = data.batches;
        console.log($scope.batches)
        if ($scope.batches.length == 0) {
            $scope.no_batch_msg = 'No batch with this name';
        }
        paginate($scope.batches, $scope, 10);
    }).error(function(data, status){
        console.log('Request failed');
    });
}

function get_items($scope, $http){
    $http.get('/inventory/items/?ajax=true').success(function(data){
        $scope.items = data.items;
        paginate($scope.items, $scope, 15);
    }).error(function(data, status){
        $scope.message = data.message;
    })
}
function get_categories($scope, $http) {
    $http.get('/inventory/categories/?ajax=true').success(function(data){
        $scope.categories = data.categories;
        paginate($scope.categories, $scope, 6);
    }).error(function(data, status){
        console.log('Request failed');
    })
}
function search_category($scope, $http, category_name, view_type) {
    $scope.no_categories_msg = '';
    $http.get('/inventory/categories/?category_name='+category_name+'&ajax=true').success(function(data){
        if (view_type == 'tree'){
            $scope.categories_list = data.categories;
            if (data.categories.length == 0) {
                $scope.no_categories_msg = 'No Category with this name';
            }
        } else if (view_type == 'multiple_product') {
            $scope.current_product.categories = data.categories;
            if (data.categories.length == 0) {
                $scope.no_categories_msg = 'No Category with this name';
            }
        } else {
            $scope.categories = data.categories;
            paginate($scope.categories, $scope, 15);
            if ($scope.categories.length == 0) {
                $scope.no_categories_msg = 'No Category with this name';
                $scope.categories = [];
            }
        }
        
    }).error(function(data, status){
        console.log('Request failed');
    }) 
}
function validate_category($scope){
    if ($scope.category.name == '' || $scope.category.name == undefined) {
        $scope.validate_category_error_msg = 'Please enter the name';
        return false;
    } else if(($scope.parent_name != undefined && $scope.parent_name.length > 0) && ($scope.category.parent_id == undefined || $scope.category.parent_id == '')) {
        $scope.validate_category_error_msg = "Parent doesn't exists";
        return false;
    } return true;
}
function save_category($scope, $http, view_type){
    if (validate_category($scope)){
        if ($scope.category.is_closed != undefined){
            if ($scope.category.is_closed == true)
                $scope.category.is_closed = 'true';
            else
                $scope.category.is_closed = 'false';
        }
            
        params = {
            'category': angular.toJson($scope.category),
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        show_loader();
        $http({
            method: 'post',
            url: '/inventory/add_category/',
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data){
            hide_loader();
            $scope.validate_category_error_msg = '';
            if (data.result == 'error') {
                $scope.validate_category_error_msg = data.message;
            } else {
                if (view_type == 'tree') {
                    $scope.is_new_category = false;
                    if (data.new_category.parent_id != ''){
                        if (!$scope.selected_parent_catergory) {
                            for (var i=0; i<$scope.categories.length; i++){
                                if(data.new_category.parent_id == $scope.categories[i].id) {
                                    $scope.selected_parent_catergory = $scope.categories[i]
                                }
                            }
                        }
                        if (data.new_category.subcategories_count != 0){
                            if ($scope.selected_parent_catergory.subcategories_count != data.new_category.subcategories_count) {
                                $scope.show_category_details($scope.selected_parent_catergory);
                            }
                        }
                        $scope.selected_parent_catergory.subcategories.push(data.new_category);
                    } else {
                        if (data.new_category)
                            $scope.categories.push(data.new_category);
                    }
                } else {
                    document.location.href = '/inventory/categories/';
                }
            }
        }).error(function(data, status) {   
            console.log('Request failed' || data);
        });
    }
}
function get_item_search_list($scope, $http, item, batch, from) {
    var url = ''
    console.log(item);
    if($scope.item_name){
        console.log($scope.item_name);
        url = '/inventory/search_item/?'+'item_name'+'='+$scope.item_name;
    } else{
        console.log("sss")
        //url = '/inventory/search_item/?'+'item_name'+'='+item+'&batch='+batch;
        url = '/inventory/search_item/?'+'item_name'+'='+item;
    }
    if($scope.search_item_name){
        //console.log($scope.search_item_name)
        url = '/inventory/search_item/?'+'item_name'+'='+$scope.search_item_name;
    }
    console.log(url);
    if (url) {
        $http.get(url).success(function(data)
        {
            var item_name = $scope.item_name;
            console.log(data.items);
            $scope.no_item_msg = '';
            if (data.items.length == 0) {
                $scope.no_item_msg = 'No such item';
                $scope.items = [];
                if (from == 'opening_stock') {
                    $scope.current_item_details.items = [];
                    $scope.current_item_details.no_item_msg = "No such item";
                
                }
            } else {
                $scope.items = data.items;

                if (from == 'purchase') {
                    
                    $scope.current_purchase_item.items = data.items; 
                }else if (from == 'opening_stock'){
                    $scope.current_item_details.items = data.items;
                    console.log($scope.current_item_details.items)
                
                }else if(from == 'stock_search'){
                    $scope.stock_items = data.items;
                    $scope.no_item_msg = '';
                }else if(from == 'estimate'){
                    $scope.current_estimate_item.items = data.items;
                    $scope.no_item_msg = '';
                }else if(from == 'delivery'){
                    $scope.current_delivery_item.items = data.items;
                    $scope.no_item_msg = '';
                }
                if($scope.items.length == 0)
                    $scope.no_item_msg = "No such item";
            }
            paginate($scope.items, $scope, 15);
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
}
function validate_batch($scope) {
    // if ($scope.batch.name == '' || $scope.batch.name == undefined) {
    //     $scope.validate_batch_error_msg = 'Please enter the batch name';
    //     return false;
    if ($scope.batch.created_date == '' || $scope.batch.created_date == undefined) {
        $scope.validate_batch_error_msg = 'Please enter the created date';
        return false;
    } return true;
}
function save_batch($scope, $http, from) {
    if (validate_batch($scope)) {
        
        params = {
            'batch_details': angular.toJson($scope.batch),
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        $http({
            method:'post',
            url: '/inventory/add_batch/',
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data){
            if (data.result == 'ok') {
                if (from == 'purchase') {
                    $scope.current_purchase_item.batch = data.id;
                    $scope.current_purchase_item.batch_name = data.name;
                    $scope.get_batch($scope.current_purchase_item);
                    hide_popup();
                } else if(from == 'opening_stock'){
                    $scope.current_item_details.batch = data.id;
                    $scope.current_item_details.batch_name = data.name;
                    $scope.get_batch($scope.current_item_details);
                    hide_popup();
                
                }else
                    document.location.href = '/inventory/batches/';
            } else {
                $scope.validate_batch_error_msg = data.message;
            }   
        }).error(function(data, status){
            console.log('Request failed' || data);
        });
    }
}
function get_batch_search_details($scope, $http, from) {
    $scope.batches = [];
    $scope.no_batch_msg = '';
    console.log('hai');
    if ($scope.batch_name != '' && $scope.batch_name != undefined && $scope.batch_name.length > 0 ) {
        var batch_name = $scope.batch_name;
       
        $http.get('/inventory/search_batch/?batch_name='+batch_name).success(function(data){
           
            $scope.no_batch_msg = '';
            if (data.batches.length == 0) {
                $scope.no_batch_msg = 'No such batch';
                if (from == 'purchase')
                    $scope.current_purchase_item.batches = [];
                else if(from == 'opening_stock')
                    $scope.current_item_details.batches = [];
                else if(from == 'closing_stock')
                    $scope.current_item_details.batches = [];
            } else {
                if (from == 'purchase')
                    $scope.current_purchase_item.batches = data.batches;
                else if(from == 'sales')
                    $scope.current_sales_item.batches = data.batches;
                else if(from == 'opening_stock')
                    $scope.current_item_details.batches = data.batches;
                else if(from == 'closing_stock')
                    $scope.current_item_details.batches = data.batches;
                else if(from == 'estimate')
                    $scope.current_estimate_item.batches = data.batches;
                else if(from == 'delivery')
                    $scope.current_delivery_item.batches = data.batches;
                else if (from == 'price_settings'){
                    $scope.batches = data.batches;
                    if ($scope.batches.length == 0){
                        $scope.batch_items = [];
                        $scope.items_name = '';
                    }
                } else {
                    $scope.batches = data.batches;
                    $scope.no_batch_msg = '';
                }
            }
        }).error(function(data, status){
            console.log('Request failed'|| data);
        });
    }
}
function validate_item($scope) {
    if ($scope.item.name == '' || $scope.item.name == undefined) {
        $scope.validate_item_error_msg = 'Please enter the name';
        return false;
    // } else if($scope.item.product == '' || $scope.item.product == undefined){
    //     $scope.validate_item_error_msg = 'Please enter a product';
    //     return false;
    // } else if($scope.item.type == '' || $scope.item.type == undefined){
    //     $scope.validate_item_error_msg = 'Please choose a type';
    //     return false;
    //     } else if($scope.item.type == 'Stockable'){ 
    //     if($scope.item.brand == '' || $scope.item.brand == undefined){
    //         $scope.validate_item_error_msg = 'Please choose a brand';
    //         return false;
    //     } else if ($scope.item.cess && ($scope.item.cess != Number($scope.item.cess))) {
    //         $scope.validate_item_error_msg = 'Please enter valid cess';
    //         return false;
    //     } else if($scope.item.uom == '' || $scope.item.uom == undefined){
    //         $scope.validate_item_error_msg = 'Please enter a uom';
    //         return false;
    //     }
    }return true;
}
function initialize_item($scope){
    $scope.item = {
        'id': '',
        'name': '',
        'category':'',
        'description': '',
        'cess': '',
        'size':'',
        'barcode': '',
        'vat_type': '',
        'uom': '',
        'new_item': 'true',
    }

}
function save_item($scope, $http, from){
    console.log("fdgdfg")
    console.log($scope.batch)
    console.log(from)
    $scope.item.category = $scope.category_name;
    console.log($scope.item.category);
    if ($scope.item.description == null) {
        $scope.item.description = '';
    }
    console.log($scope.item)
    params = {
        'item': angular.toJson($scope.item),
        'csrfmiddlewaretoken': $scope.csrf_token,
    }
    if(validate_item($scope)){
        $http({
            method: 'post',
            url: '/inventory/add_item/',
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data){
            if (data.result == 'ok') {
                console.log("pppp")
                console.log($scope.batch)
                $scope.no_item_msg = '';
                if (from == 'purchase') {

                    $scope.current_purchase_item.name = data.item.name;
                    $scope.current_purchase_item.id = data.item.id;
                    $scope.current_purchase_item.code = data.item.code;
                    $scope.current_purchase_item.tax = data.item.tax;
                    $scope.current_purchase_item.uom = data.item.uom;
                    hide_popup();
                    $scope.get_batch($scope.current_purchase_item);
                    //get_item_uoms($scope, $http);
                } else if(from == 'opening_stock'){
                    console.log(data.item)
                    $scope.current_item_details.name = data.item.name;
                    $scope.current_item_details.id = data.item.id;
                    $scope.current_item_details.code = data.item.item_code;
                    // $scope.current_item_details.uom = data.item.uom;
                    // $scope.current_item_details.stock = 0
                    // $scope.current_item_details.purchase_price = 0
                    // $scope.current_item_details.selling_price = 0
                    $scope.get_batch($scope.current_item_details);

                    //get_item_uoms($scope, $http);
                    hide_popup();
                
                }else {
                    document.location.href = '/inventory/items/';
                }

            } else {
                $scope.validate_item_error_msg = data.message;
            }
        }).error(function(data, status){
            console.log('Request failed'||data);
        });
    }
}
function get_subcategory_list($scope, $http, category_id, view_type) {
    $http.get('/inventory/subcategory_list/'+category_id+'/').success(function(data){
        if (view_type == 'edit') {
            $scope.categories_details = data.category_details[0];
        } else {
            
            $scope.current_category.subcategories = [];
            $scope.current_category.subcategories = data.subcategories;
            if ($scope.selected_parent_catergory != undefined){
                $scope.selected_parent_catergory.subcategories = data.subcategories;
            }
        }
    }).error(function(data, status){
        console.log('Request failed' || data);
    })
}
function get_category_subcategory_list($scope, $http) {
    // $http.get('/inventory/categories_tree_view/?ajax=true').success(function(data){
    $http.get('/inventory/categories/?ajax=true&tree=true').success(function(data){
        $scope.categories = data.categories;
        for (var i=0; i<$scope.categories.length; i++) {
            $scope.categories[i].is_closed = true;
        }
    }).error(function(data, status){
        console.log('Request failed' || data);
    })
}
function BatchController($scope, $http){
    $scope.batch = {
        'id': '',
        'name': '',
        'created_date':'',
        'expiry_date': '',
    }
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        get_batches($scope, $http);
    }
    $scope.create_batch = function() {
        document.location.href = '/inventory/add_batch/';
    }
    $scope.save_batch = function() {
        save_batch($scope, $http);
    }
    $scope.view_batch = function(batch){
        $scope.batch = batch;
        create_popup();
    }
    $scope.edit_batch_details = function(batch) {
        $scope.batch = batch;
        document.location.href = '/inventory/edit_batch/?batch_id='+batch.id
    }
    $scope.delete_batch = function(batch) {
        document.location.href = '/inventory/delete_batch/?batch_id='+batch.id;
    }
    $scope.get_batch_list = function() {
        get_batch_search_details($scope, $http);
    }
    $scope.hide_popup = function() {
        hide_popup();
    }
}
function AddBatchController($scope, $http){
    $scope.batch = {
        'id': '',
        'name': '',
        'created_date':'',
        'expiry_date': '',
    }
    $scope.init = function(csrf_token, batch_id) {
        $scope.csrf_token = csrf_token;
        if (batch_id){
            $http.get('/inventory/edit_batch/?batch_id='+batch_id+'&ajax=true').success(function(data){
                $scope.batch = data.batch;
            }).error(function(data, status){
                console.log('Request failed');
            })
        }
    }
    $scope.save_batch = function() {
        
        save_batch($scope, $http);
    }
}
function ItemController($scope, $http){
    initialize_item($scope);
    //get_conversions($scope, $http);
    $scope.category_option = "Search Category";
    $scope.batch_item_exists = false;
    hide_popup();
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if ($scope.categories != undefined && $scope.categories.length > 0) {
            if($scope.focusIndex < $scope.categories.length-1){
                $scope.focusIndex++; 
            }
        } 
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        get_items($scope, $http);
        
    }
    $scope.create_item = function() {
        document.location.href = '/inventory/add_item/';
    }
    $scope.hide_popup = function() {
        hide_popup();
    }
    $scope.save_item = function() {
        console.log("ewqewr");
        save_item($scope, $http);
    }

    $scope.get_category_list = function() {
        search_category($scope, $http, $scope.category_name);
    }
    $scope.get_category_list = function() {
        $scope.item.category_id = '';
        if ($scope.category_name.length > 0){
            search_category($scope, $http, $scope.category_name);
        }
    }
    $scope.select_category_details = function(category) {
        $scope.focusIndex = 0;
        $scope.product.category_id = category.id;
        $scope.category_name = category.name;
        $scope.categories = [];
    }
    
    $scope.select_list_item = function(index) {
        if ($scope.categories != undefined && $scope.categories.length > 0) {
            category = $scope.categories[index];
            $scope.select_category(category);
        } 
    }
    
    $scope.select_category = function(category) {
        $scope.focusIndex = 0;
        $scope.item.category_id = category.id;
        $scope.category_name = category.name;
        $scope.categories = [];
    }
    $scope.edit_item_details = function(item) {
        $scope.item = item;
        $scope.product_name = item.product_name;
        $scope.brand_name = item.brand_name;
        $scope.vat_type = item.vat_name;
        $scope.uom = item.uom;
        $scope.item.new_item = 'false';
        $scope.edit_item = true;
        $scope.batch_item_exists = item.batch_item_exists;
        if ($scope.batch_item_exists == true){
            $scope.batch_item_exists = 'true';
        }else{
            $scope.batch_item_exists = 'false';
        }
        hide_item_popups();
        $('#add_item').css('display', 'block');
        create_popup();
    }
    $scope.delete_item = function(item) {
        document.location.href = '/inventory/delete_item/?item_id='+item.id;
    }
    $scope.get_items_list = function() {
        get_item_search_list($scope, $http,$scope.item_name);
    }
    $scope.select_page = function(page){
        select_page(page, $scope.items, $scope, 15);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.view_item = function(item){
        $scope.item = item;
        hide_item_popups();
        $('#view_item').css('display', 'block');
        create_popup();
    }
    $scope.hide_popups = function(){
        hide_popup()
    }
    $scope.new_category = function() {
        $scope.is_new_category = true;
        $scope.no_categories_msg = '';
        $scope.categories = [];
        $scope.category_option = "New Category";
    }
    $scope.is_category_name_exists = function(){
        is_category_name_exists($scope, $http, $scope.product.new_category_name, 'item_add');
    }
    $scope.search_category = function(){
        $scope.no_categories_msg = '';
        $scope.is_new_category = false;
        $scope.category_option = "Search Category";
    }
}
function OpeningStockController($scope, $http){
   
    $scope.opening_stock_items = [];
    for (var i=0; i<5; i++) {
        $scope.opening_stock_items.push(
        {
            'item_name': '',
            'code': '',
            'batch': '',
            'quantity': '',
            'purchase_unit': '',
            'purchase_price': '',
            'selling_price': '',
        });
    }
    $scope.current_item_details = [];
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if ($scope.vat_list != undefined && $scope.vat_list.length > 0) {
            if($scope.focusIndex < $scope.vat_list.length-1){
                $scope.focusIndex++; 
            }
        } else if ($scope.current_item_details.batches != undefined && $scope.current_item_details.batches.length > 0) {
            if($scope.focusIndex < $scope.current_item_details.batches.length-1){
                $scope.focusIndex++; 
            }
        } else if ($scope.current_item_details.items != undefined && $scope.current_item_details.items.length > 0) {
            if($scope.focusIndex < $scope.current_item_details.items.length-1){
                $scope.focusIndex++; 
            }
        }else if ($scope.categories_list != undefined && $scope.categories_list.length > 0) {
            if($scope.focusIndex < $scope.categories_list.length-1){
                $scope.focusIndex++; 
            }
        }
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        //get_conversions($scope, $http);
    }
    $scope.add_bulk_items = function(){
        for (var i=0; i<5; i++) {
            $scope.opening_stock_items.push(
            {
                'item_name': '',
                'code': '',
                'batch': '',
                'quantity': '',
            });
        }
    }
    $scope.add_new_opening_stock_item = function() {
        $scope.opening_stock_items.push(
        {
            'item_name': '',
            'code': '',
            'batch': '',
            'quantity': '',
            'purchase_unit': '',
            'purchase_price': '',
            'selling_price': '',
        
        });
    }
    $scope.hide_popup = function() {
        hide_popup();
    }
    $scope.select_category = function(category) {
        $scope.focusIndex = 0;
        $scope.item.category_id = category.id;
        $scope.category_name = category.name;
        $scope.categories = [];
    }
    // $scope.search_batch = function(item) {
    //     item.batch_search = true;
    //     item.item_search = false;
    //     $scope.current_item_details = item;
    //     $scope.batch_name = item.batch_name;
    //     get_batch_search_details($scope, $http, 'opening_stock');
    // }
    // $scope.select_batch = function(batch) {
    //     console.log(batch);
    //     $scope.focusIndex = 0;
    //     $scope.current_item_details.batch_name = batch.name;
    //     $scope.current_item_details.batch = batch.id;
    //     $scope.current_item_details.stock = batch.quantity_in_purchase_unit;
    //     if ($scope.current_item_details.id) {
    //         $scope.get_batch($scope.current_item_details);
    //     } 
    //     $scope.current_item_details.batches = [];
    //     $scope.current_item_details.batch_search = false;
    // }
    $scope.select_batch = function(batch) {
        $scope.batch = batch.id;
        $scope.batches = [];
        $scope.batch_name = batch.name;
        $scope.focusIndex = 0;
        console.log("bbbbb")
        console.log($scope.batch)
        // $scope.get_batch(item);
        // $scope.current_item_details.batch_name = batch.name;
        // $scope.current_item_details.batch = batch.id;
        // $scope.current_item_details.stock = batch.quantity_in_purchase_unit;
        // if ($scope.current_item_details.id) {
        //     $scope.get_batch($scope.current_item_details);
        // } 
        // $scope.current_item_details.batches = [];
        // $scope.current_item_details.batch_search = false;
    }
          
    $scope.get_batch_list = function(){
        $scope.batch = '';
        if ($scope.batch_name.length > 0)
            search_batch($scope, $http);
        
    }
    $scope.get_batch = function(item){
        console.log("aaaa")
        $http.get('/inventory/search_batch_item/?batch_id='+$scope.batch+'&item_id='+item.id).success(function(data){
            if (data.result == 'ok') {
                console.log(data.batch_items)

                $scope.batch_items=data.batch_items;
                $scope.batch_id=data.batch_items['id']
                console.log($scope.batch_items.code);
                item.stock = data.batch_items.stock;
                console.log(item.stock);
                console.log(data.batch_items.batch_id)
                // if (data.batch_items.uom.length > 0)
                //     $scope.current_item_details.uom_exists = true;
                // else
                //     $scope.current_item_details.uom_exists = false;
                item.purchase_unit = data.batch_items.uom;
                item.purchase_price = data.batch_items.purchase_price;
                item.selling_price = data.batch_items.selling_price;
                item.uom = data.batch_items.uom;
            } else {
                item.stock = 0;
                $scope.current_item_details.uom_exists = false;
                item.purchase_unit = '';
                item.purchase_price = 0.00;
                item.selling_price =0.00;

            }
        }).error(function(data, status) {
            console.log('Request failed' || data);
        });
    }
    
    $scope.search_items = function(item) { 
        item.item_search = true; 
        item.batch_search = false; 
        $scope.current_item_details = [];
        $scope.current_item_details = item;
        //console.log($scope.current_item_details);
        get_item_search_list($scope, $http, $scope.current_item_details.name, item.batch, 'opening_stock');
    }
    $scope.get_items = function() {
        get_item_search_list($scope, $http,$scope.item_name);
    }
    $scope.select_item_details = function(item) {
        console.log(item)
        console.log('byyyy')
        console.log($scope.batch)
        $scope.current_item_details.name = item.name;
        $scope.current_item_details.code = item.code;
        $scope.current_item_details.id = item.id;
        $scope.current_item_details.code=item['item_code']

        console.log(item['uom']);

        $scope.current_item_details.items = [];
        if ($scope.current_item_details.batch) {
            $scope.select_batch($scope.current_item_details.batch);
        }
        $scope.current_item_details.item_search = false;    
        $scope.current_item_details.batch_search = false;   
        $http.get('/inventory/search_batch_item/?batch_id='+$scope.batch+'&item_id='+item.id).success(function(data){
        console.log("haiii")
        console.log(data.result)
            if (data.result == 'ok') {
                console.log(data.batch_items)
                $scope.batch_items=data.batch_items;
                console.log($scope.batch_items);
                // item.stock = data.batch_items['stock'];
                $scope.current_item_details.stock=data.batch_items['stock'];
                console.log(item.stock);
                $scope.current_item_details.batch=data.batch_items['batch_id'];
                // if (data.batch_items.uom.length > 0)
                //     $scope.current_item_details.uom_exists = true;
                // else
                //     $scope.current_item_details.uom_exists = false;
                $scope.current_item_details.purchase_unit = data.batch_items.uom;
                $scope.current_item_details.purchase_price = data.batch_items.purchase_price;
                $scope.current_item_details.selling_price = data.batch_items.selling_price;
                $scope.current_item_details.uom = data.batch_items.uom;
                $scope.current_item_details.stock = data.batch_items.stock
            } else {
                
                $scope.current_item_details.stock = 0;
                $scope.current_item_details.uom_exists = false;
                $scope.current_item_details.purchase_unit = '';
                $scope.current_item_details.purchase_price = 0.00;
                $scope.current_item_details.selling_price =0.00;
                $scope.current_item_details.batch=$scope.batch;
            }
        }).error(function(data, status) {
            console.log('Request failed' || data);
        });
             
        hide_popup();
        $scope.items = [];
        $scope.focusIndex = 0;
        //get_item_uoms($scope, $http);
    }
    $scope.select_list_item = function(index) {
        
        if ($scope.categories_list!=undefined && $scope.categories_list.length>0){
            category = $scope.categories_list[index];
            $scope.select_category_details(category);
        }
        if ($scope.current_item_details.items!=undefined && $scope.current_item_details.items.length>0){
            item = $scope.current_item_details.items[index];
            $scope.select_item_details(item);
        }
        if ($scope.current_item_details.batches!=undefined && $scope.current_item_details.batches.length>0){
            batch = $scope.current_item_details.batches[index];
            $scope.select_batch(batch);
        }
    }
    $scope.get_conversion_units = function(item) {
        $scope.current_item_details = item;
        //get_conversions($scope, $http, item.purchase_unit, 'purchase_unit');
    }
    $scope.save_quantity = function(item) {
        item.quantity_entered = item.quantity;
    }
    $scope.calculate_net_amount = function(item) {
        if (item.purchase_price != Number(item.purchase_price)) {
            item.purchase_price = 0.00;
        } 
        if (item.quantity != Number(item.quantity)) {
            item.quantity = 0.00;
        } 
        item.net_amount = item.quantity*item.purchase_price;
    }
    $scope.validate_opening_stock = function(){
        if ($scope.opening_stock_items.length == 0) {
            $scope.validate_opening_stock_msg = 'Please choose Items';
            return false;
        } else if ($scope.opening_stock_items.length > 0) {
            for (var i =0; i<$scope.opening_stock_items.length; i++) {
                if ($scope.opening_stock_items[i].code == '') {
                    $scope.validate_opening_stock_msg = 'Item  cannot be null in row'+ (i+1);
                    return false;
                // } else if ($scope.opening_stock_items[i].batch == '') {
                //     $scope.validate_opening_stock_msg = 'Please choose batch in row '+ (i+1);
                //     return false;
                } else if ($scope.opening_stock_items[i].quantity == '' || !Number($scope.opening_stock_items[i].quantity ) || $scope.opening_stock_items[i].quantity == 0){
                    $scope.validate_opening_stock_msg = 'Please enter quantity in row '+ (i+1);
                    return false;
                } else if ($scope.opening_stock_items[i].purchase_price == '' || $scope.opening_stock_items[i].purchase_price == undefined) {
                    $scope.validate_opening_stock_msg = 'Please enter purchase price in row '+ (i+1);
                    return false;
                } else if ($scope.opening_stock_items[i].selling_price == '' || $scope.opening_stock_items[i].selling_price == undefined) {
                    $scope.validate_opening_stock_msg = 'Please enter selling price in row '+ (i+1);
                    return false;
                } else if ($scope.opening_stock_items[i].purchase_unit == '' || $scope.opening_stock_items[i].purchase_unit == undefined) {
                    $scope.validate_opening_stock_msg = 'Please choose uom in row '+ (i+1);
                    return false;
                } 
            }
        } return true;
    }
    $scope.remove_opening_stock_item = function(item) {
        var index = $scope.opening_stock_items.indexOf(item);
        $scope.opening_stock_items.splice(index, 1);
    }
    $scope.hide_popup_transaction_details = function() {
        document.location.href = '/inventory/opening_stock/';
    }
    $scope.save_opening_stock = function(){
       
        for (var i=0; i<$scope.opening_stock_items.length; i++) {
            if ($scope.opening_stock_items[i].uom_exists == true) {
                $scope.opening_stock_items[i].uom_exists = 'true';
            } else {
                $scope.opening_stock_items[i].uom_exists = 'false';
            }
            if ($scope.opening_stock_items[i].item_search == true) {
                $scope.opening_stock_items[i].item_search = 'true';
            } else {
                $scope.opening_stock_items[i].item_search = 'false';
            }
            if ($scope.opening_stock_items[i].batch_search == true) {
                $scope.opening_stock_items[i].batch_search = 'true';
            } else {
                $scope.opening_stock_items[i].batch_search = 'false';
                $scope.opening_stock_items[i].batch=$scope.batch_name;
            }
        }
        if ($scope.validate_opening_stock()) {
            
            $scope.opening_stock_items.batch=$scope.batch_name;
            console.log($scope.opening_stock_items.batch)
            console.log($scope.opening_stock_items)
            params = {
                'opening_stock_items': angular.toJson($scope.opening_stock_items),
                'csrfmiddlewaretoken': $scope.csrf_token,
                }
            show_loader();
            $http({
                method: 'post',
                url: '/inventory/opening_stock/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data){
                hide_loader();
                console.log(data.result)
                if (data.result == 'ok') {
                    hide_opening_stock_popup_divs()
                    $scope.transaction_reference_no = data.transaction_reference_no;
                    $scope.transaction_name = ' Opening Stock ';
                    $('#transaction_reference_no_details').css('display', 'block');
                    create_popup();
                } 
            }).error(function(data, status){
                console.log('Request failed'||data);
            });
        }
    }
    $scope.hide_item = function(item){
        $scope.focusIndex = 0;
        item.batch_search = false;
        if (item.item_search == true){
            item.item_search = false;
        } else {
            item.item_search = true;
        }
    }
    // $scope.hide_batch = function(){
    //     $scope.focusIndex = 0;
    //     $scope.item_search = false;
    //     if ($scope.batch_search == true){
    //         $scope.batch_search = false;
    //     } else {
    //         $scope.batch_search = true;
    //     }
    // }
    $scope.add_new_item = function(item) {
        $scope.current_item_details = item;
        initialize_item($scope);
        console.log("232")
        console.log($scope.batch)
        hide_opening_stock_popup_divs();        
        $('#add_item').css('display', 'block');
        $scope.no_product_msg = '';
        $scope.no_brand_msg = '';
        $scope.no_vat_msg = '';
        $scope.validate_item_error_msg = '';
        create_popup();
    }
    $scope.save_item = function() {
        save_item($scope, $http, 'opening_stock');
    }
    $scope.get_brands = function() {
        get_brand_search_list($scope, $http);
    }
    $scope.select_brand_details = function(brand) {
        $scope.item.brand = brand.id;
        $scope.brand_name = brand.name;
        $scope.brands = [];
    }
    $scope.get_products = function() {
        if($scope.product_name){
            get_product_search_list($scope, $http);
        }
    }
    $scope.select_product_details = function(product) {
        $scope.item.product = product.id;
        $scope.product_name = product.name + '-' + product.category_name;
        $scope.products = [];
    }
    $scope.get_vat_list = function() {
        get_vat_search_details($scope, $http);
    }
    $scope.select_vat_details = function(vat) {
        $scope.item.vat = vat.id;
        $scope.vat_type = vat.vat_name;
        $scope.vat_list = [];
    }
    

    $scope.new_batch = function(item) {
        $scope.validate_batch_error_msg = '';
        $scope.batch = {
            'id': '',
            'name': '',
            'created_date':'',
            'expiry_date': '',
        }
        $scope.current_item_details = item;
        hide_opening_stock_popup_divs();
        $('#new_batch').css('display', 'block');
        create_popup();
    }
    $scope.save_batch = function() {
        save_batch($scope, $http, 'opening_stock');
    }
    $scope.new_product = function(){
        $scope.new_inventory_item = $scope.item;
        $scope.product = {
            'name': '',
            'category_id': '',
            'id': '',
        }
        hide_opening_stock_popup_divs();
        $('#add_product').css('display', 'block');
        create_popup();
    }
    $scope.get_category_list = function() {
        if ($scope.category_name.length>0)
            search_category($scope, $http, $scope.category_name);
    }

    $scope.select_category_details = function(category){
        $scope.product.category_id = category.id;
        $scope.category_name = category.name;
        $scope.categories = [];
    }
    $scope.save_product = function(){

        save_product($scope, $http, 'opening_stock_item_add');
    }
    $scope.new_brand = function(){
        $scope.new_inventory_item = $scope.item;
        hide_opening_stock_popup_divs();
        $scope.brand = {
            'name': '',
        }
        $('#add_brand').css('display', 'block');
        create_popup();
    }
    $scope.hide_popups = function(){
        hide_opening_stock_popup_divs();
        $('#add_item').css('display', 'block');
        create_popup();
    }
    $scope.save_brand = function(){
        save_brand($scope, $http, 'opening_stock_item_add');
    }
    $scope.new_vat = function(){
        $scope.new_inventory_item = $scope.item;
        hide_opening_stock_popup_divs();
        $scope.vat={
            'id': '',
            'name': '',
            'percentage':0,
        }
        $('#add_vat').css('display', 'block');
        create_popup();
    }
    $scope.save_vat = function() {
        save_vat($scope, $http, 'opening_stock_item_add');
    }
    $scope.new_category = function() {
        $scope.is_new_category = true;
        $scope.no_categories_msg = '';
        $scope.categories = [];
    }
    $scope.is_category_name_exists = function(){
        is_category_name_exists($scope, $http, $scope.product.new_category_name, 'opening_stock_item_add');
    }
    $scope.search_category = function(){
        $scope.no_categories_msg = '';
        $scope.is_new_category = false;
    }
}

function CategoryTreeController($scope, $http){
    $scope.category = {
        'parent_id': '',
        'name': '',
        'parent_name': '',
    }
    $scope.is_new_category = false;
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if($scope.focusIndex < $scope.categories_list.length-1){
            $scope.focusIndex++; 
        }
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    $scope.select_list_item = function(index) {
        if ($scope.categories_list != undefined) {
            category = $scope.categories_list[index];
            if (category != undefined)
                $scope.select_category(category);
        }
    }
    $scope.init = function(csrf_token){
        $scope.is_new_category = false;
        $scope.csrf_token = csrf_token;
        get_category_subcategory_list($scope, $http);
    }
    $scope.toggle_category_view = function(event, category) {
        var target = $(event.currentTarget);
        var element = target.parent().find('ul').first();
        var height_property = element.css('height');
        if(height_property == '0px') {
            element.animate({'height': '100%'}, 500);
            if(category.subcategories.length == 0){
                $scope.show_category_details(category);
            }
            $(target).addClass('open').removeClass('closed');
        } else {
            element.animate({'height': '0px'}, 500);
            $(target).addClass('closed').removeClass('open');
        }
    } 
    $scope.show_category_details = function(category) {
        $scope.current_category = category;
        get_subcategory_list($scope, $http, category.id,'subcategory');
    }
    $scope.add_subcategory = function(category){
        $scope.is_new_category = true;
        $scope.category = {
            'parent_id': '',
            'name': '',
            'parent_name': '',
        }
        if (category) {
            $scope.category.parent_name = category.name;
            $scope.category.parent_id = category.id;
            $scope.selected_parent_catergory = category;
        } else {
            $scope.parent_name = '';
        }
    }
    $scope.edit_subcategory = function(category){
        $scope.is_new_category = true;
        $scope.category = {
            'parent_id': '',
            'name': '',
            'parent_name': '',
        }
        if (category) {
            $scope.category = category;
        } 
        $scope.selected_parent_catergory = category;
    }
    $scope.save_category = function(){
        save_category($scope, $http, 'tree');
    }
    $scope.get_category_list = function() {
        $scope.category.parent_id = '';
        $scope.no_categories_msg = '';
        if ($scope.parent_name.length > 0){
            search_category($scope, $http, $scope.parent_name, 'tree');
        }
    }
    $scope.select_category = function(category) {
        // $scope.selected_parent_catergory = category;
        $scope.category.parent_id = category.id;
        $scope.parent_name = category.name;
        $scope.categories_list = [];
    }
    $scope.hide_popup = function(){
        hide_popup();
    }
    $scope.delete_category = function(category, categories){
        document.location.href = '/inventory/delete_category/?category_id='+category.id;
    }
}

function StockSearchController($scope, $http, stock_items) {
    $scope.current_item_details = [];
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if($scope.stock_items != undefined && $scope.stock_items.length > 0 && $scope.focusIndex < $scope.stock_items.length-1){
            if($scope.focusIndex < $scope.stock_items.length-1){
                $scope.focusIndex++; 
            }
        } 
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    $scope.init = function(csrf_token) {
        $scope.stock_view_visible = false;
        $scope.csrf_token = csrf_token;
    }
     $scope.search_items = function() { 
        $scope.item_search = true;
        $scope.stock_items = [];
        get_item_search_list($scope, $http, $scope.item_name, '' , 'stock_search');
    }
    $scope.select_list_item = function(index){
        if ($scope.stock_items != undefined && $scope.stock_items.length > 0) {
            item = $scope.stock_items[index];
            $scope.get_item_stock_list(item)
        }
    }
    $scope.get_item_stock_list = function(item) {
        $scope.focusIndex = 0;
        $scope.item_search = false;
        $scope.stock_items = [];
        $scope.item_name = '';
        create_popup();
        $('#stock_search_popup').css('display', 'block');
        $('#add_brand').css('display', 'none');
        $('#add_product').css('display', 'none');
        $('#add_vat').css('display', 'none');
        $('#add_item').css('display', 'none');
        $('#view_item').css('display', 'none');
        $('#add_customer').css('display', 'none');
        $('#new_ledger').css('display', 'none');
        $('#add_category').css('display', 'none');
        $('#view_customer').css('display', 'none');
        $('#view_category').css('display', 'none');
        $('#view_batch').css('display', 'none');
        $('#view_product').css('display', 'none');
        $('#view_brand').css('display', 'none');
        $('#view_vat').css('display', 'none');
        $('#payment_details').css('display', 'none');
        $('#new_batch').css('display', 'none');
        $('#add_item').css('display', 'none');
        $('#add_supplier').css('display', 'none');
        $('#view_supplier').css('display', 'none');
        $('#transaction_reference_no_details').css('display', 'none');
        $('#bank_account_details').css('display', 'none');
        $('#add_customer_popup').css('display', 'none');
        $('#add_salesman_popup').css('display', 'none');
        $('#cost_price_calculator').css('display', 'none');
            
        var url = '';
        if(item.id){
            url = '/inventory/search_item_stock/?'+'id'+'='+item.id;
            show_loader();
            $http.get(url).success(function(data)
            {
                var item_name = $scope.item_name;
                $scope.no_item_msg = '';
                hide_loader();
                $scope.stock_items = [];
                $scope.stock_items_details = [];
                if (data.items.length > 0) {
                    if (stock_items.stock_items.length > 0) {
                        $scope.stock_items = [];
                        stock_items.stock_items = [];
                        $scope.fill_stock_data(data.items);
                    } else {
                        $scope.fill_stock_data(data.items);
                    }
                } else {
                    stock_items.stock_items = [];
                }
                
            }).error(function(data, status)
            {
                console.log(data || "Request failed");
            });
        }
    }
    $scope.fill_stock_data = function(stock){
        for(i=0; i<stock.length ;i++)  {
            stock_items.stock_items.push(stock[i]); 
        }  
        

        /*stock_items.add(stock);*/
    }
    $scope.hide_popup = function(){
        $('#stock_search_popup').css('display', 'none');
        $('#new_ledger').css('display', 'none');
        $scope.item_name = '';
        $scope.stock_items = [];
        hide_popup();
    }
    
}
function StockViewController($scope, $http, stock_items) {

    $scope.init = function(csrf_token){
        $scope.stock_items = [];
        $scope.item_name = '';
        $scope.stock_items = stock_items;
    }
    $scope.hide_popup = function(){
        $('#stock_search_popup').css('display', 'none');
        $('#new_ledger').css('display', 'none');
        $scope.item_name = '';
        hide_popup();
    }
}

function StockReportController($scope, $http) {
    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $http.get('/inventory/stock_report/?ajax=true').success(function(data){
            $scope.stocks_report = data.stocks_report;
            //paginate($scope.stocks_report, $scope, 15);
        }).error(function(data, status){
            console.log('Request failed');
        });
    }

    $scope.current_item_details = [];
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if($scope.batches != undefined && $scope.batches.length > 0 && $scope.focusIndex < $scope.batches.length-1){
            if($scope.focusIndex < $scope.batches.length-1){
                $scope.focusIndex++; 
            }
        } 
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    
    $scope.hide_popup = function() {
        hide_popup();
    }
    $scope.select_list_item = function(index) {
        if ($scope.batches != undefined && $scope.batches.length > 0) {
            batch = $scope.batches[index];
            $scope.select_batch(batch);
        } 
    }
    $scope.select_batch = function(batch) {
        $scope.closed_flag=batch.closed_flag
        $scope.batch = batch.id;
        $scope.batches = [];
        $scope.batch_name = batch.name;
        $scope.focusIndex = 0;
        $scope.generate_list();
    }
    // $scope.get_batch_list = function() {
    //     get_batch_search_details($scope, $http);
    // }
    $scope.get_batch_list = function(){
        $scope.batch = '';
        if ($scope.batch_name.length > 0)
            search_batch_for_report($scope, $http);
    }
    // $scope.calculate_purchase_price = function(batch_item){
    //     $scope.total_purchase_price = 0;
    //     batch_item.total_purchase_price = (parseFloat(batch_item.stock)*parseFloat(batch_item.purchase_price))
    // }
    
    $scope.generate_list = function(){
        $scope.no_batch_msg = '';
        console.log ($scope.batch_name);
        

        if ($scope.batch_name == '' || $scope.batch_name == undefined) {
            $scope.no_batch_msg = 'Please Choose batch';

        } else {
            // if (type_name == 'view') { 
                show_loader();
                $http.get('/inventory/stock_report/?batch_id='+$scope.batch+'&pdf=false').success(function(data){
                    $scope.batch_items = data.batch_items;
                    $scope.total_purchase_price = data.total_purchase_price;
                    $scope.total_selling_price = data.total_selling_price;
                    console.log($scope.total_purchase_price);
                    console.log($scope.total_selling_price);
                    if ($scope.batch_items.length == 0)
                        $scope.no_batch_msg = 'No items';
                    // else if($scope.total_purchase_price.length==0)
                    //     $scope.no_batch_msg = 'No items';

                    else {
                        
                        paginate($scope.batch_items,$scope.total_purchase_price,$scope.total_selling_price,$scope, 15);
                        console.log("mumyy");
                        
                        
                        
                    }
                    hide_loader();
                }).error(function(data, status){
                    console.log(data);
                });
            // } else
            //     document.location.href = '/inventory/closing_stock/?batch_id='+$scope.batch;
        }
    }
    $scope.select_page = function(page){
        select_page(page, $scope.stocks_report, $scope, 15);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.generate_pdf = function(){
        console.log("pdf")
        document.location.href = '/inventory/stock_report/?batch_id='+$scope.batch+'&pdf=true';
    }
}

function ClosingStockController($scope, $http){ 
    $scope.closing_stock_items = [];
    $scope.batch_items = {
        'item_name': '',
        'code': '',
        'stock': '',
        'consumed_quantity': '',
        'closing_stock': '',
    }
    $scope.current_item_details = [];
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if($scope.batches != undefined && $scope.batches.length > 0 && $scope.focusIndex < $scope.batches.length-1){
            if($scope.focusIndex < $scope.batches.length-1){
                $scope.focusIndex++; 
            }
        } 
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        $scope.total_selling_price=0;
    }
    $scope.hide_popup = function() {
        hide_popup();
    }
    $scope.select_list_item = function(index) {
        if ($scope.batches != undefined && $scope.batches.length > 0) {
            batch = $scope.batches[index];
            $scope.select_batch(batch);
        } 
    }
    $scope.select_batch = function(batch) {
        $scope.batch = batch.id;
        $scope.batches = [];
        $scope.batch_name = batch.name;
        $scope.focusIndex = 0;
        $scope.generate_list();
    }
    
    $scope.get_batch_list = function(){
        $scope.batch = '';
        if ($scope.batch_name.length > 0)
            search_batch($scope, $http);
    }
    
    $scope.generate_list = function(){
        $scope.no_batch_msg = '';
        console.log ($scope.batch_name);
        
        if ($scope.batch_name == '' || $scope.batch_name == undefined) {
            $scope.no_batch_msg = 'Please Choose batch';

        } else {
            // if (type_name == 'view') { 
                show_loader();
                $http.get('/inventory/closing_stock/?batch_id='+$scope.batch).success(function(data){
                    $scope.batch_items = data.batch_items;
                    $scope.total_amount_recieved=data.total_amount_recieved;
                    $scope.calculate_total_selling_price();
                    if ($scope.batch_items.length == 0)
                        $scope.no_batch_msg = 'No items';
                    else {
                        paginate($scope.batch_items, $scope, 15);
                    }
                    hide_loader();
                }).error(function(data, status){
                    console.log(data);
                });            
        }
    }
    $scope.calculate_consumed_quantity = function(item){
        console.log(item)
        console.log("cal")

        var consumed_quantity = 0;
        
        if (parseFloat(item.stock) >= parseFloat(item.closing_stock)){
            item.consumed_quantity = (parseFloat(item.stock) - parseFloat(item.closing_stock));
            
        }
        else{
            item.consumed_quantity = 'Closing Stock above stock level';
        }
        $scope.calculate_total_selling_price();                  
    }
    $scope.calculate_total_selling_price = function(){
       $scope.total_selling_price = 0;
       $scope.total_consumed_quantity = 0;
       for(var i = 0; i < $scope.batch_items.length; i++){
            $scope.total_selling_price = (parseFloat($scope.total_selling_price)+parseFloat($scope.batch_items[i].stock)*parseFloat($scope.batch_items[i].selling_price));
            if($scope.batch_items[i].consumed_quantity){
                $scope.total_consumed_quantity = (parseFloat($scope.total_consumed_quantity)+parseFloat($scope.batch_items[i].consumed_quantity)*parseFloat($scope.batch_items[i].selling_price));
            }
       }
       
    }
    $scope.validate_closing_stock = function(){
        if ($scope.batch_items.length == 0) {
            $scope.validate_closing_stock_msg = 'Please choose batchitems';
            return false;
        }return true;
    }
    $scope.save_closing_stock = function(){
        
        if ($scope.validate_closing_stock()) {
            params = {
                'closing_stock_items': angular.toJson($scope.batch_items),
                'csrfmiddlewaretoken': $scope.csrf_token,
                }
            show_loader();
            $http({
                method: 'post',
                url: '/inventory/closing_stock/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data){
                
                if (data.result == 'error'){
                    
                    $scope.validate_closing_stock_error_msg = data.message;
                }else{
                    document.location.href = '/inventory/closing_stock/';

                }
                hide_loader();    
                
            }).error(function(data, status) {   
                console.log('Request failed' || data);
            });
           
        }
    }
    $scope.select_page = function(page){
        select_page(page, $scope.batch_items, $scope, 15);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
}


function CashEntryController($scope, $http){
    $scope.cash_entry ={
        'id':'',
        'date':'',
        'amount':'',
        'batch':'',
    }
    
    $scope.current_item_details = [];
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if($scope.batches != undefined && $scope.batches.length > 0 && $scope.focusIndex < $scope.batches.length-1){
            if($scope.focusIndex < $scope.batches.length-1){
                $scope.focusIndex++; 
            }
        } 
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
    }
    $scope.hide_popup = function() {
        hide_popup();
    }
    $scope.select_list_item = function(index) {
        if ($scope.batches != undefined && $scope.batches.length > 0) {
            batch = $scope.batches[index];
            $scope.select_batch(batch);
        } 
    }
    $scope.select_batch = function(batch) {
        $scope.batch = batch.id;
        $scope.batches = [];
        $scope.batch_name = batch.name;
        $scope.focusIndex = 0;
        $scope.cash_entry.batch=batch.id;
        //$scope.generate_list();
    }
    
    $scope.get_batch_list = function(){
        $scope.batch = '';
        if ($scope.batch_name.length > 0)
            search_batch_for_report($scope, $http);
    }

    $scope.validate_cash_entry = function(){
        if ($scope.cash_entry.date == '' || $scope.cash_entry.date == undefined) {
            $scope.validate_cash_entry_error_msg = 'Please enter the date';
            return false;
        }else if($scope.cash_entry.amount == '' || $scope.cash_entry.amount == undefined){
            $scope.validate_cash_entry_error_msg = 'Please enter the Amount';
            return false;
        }
        return true;

    }

    $scope.save_cash_entry = function(){

        if ($scope.validate_cash_entry()) {
        console.log($scope.cash_entry)
        params = {
            'cash_entry_details': angular.toJson($scope.cash_entry),
            'csrfmiddlewaretoken': $scope.csrf_token,
        }
        $http({
            method:'post',
            url: '/inventory/cash_entry/',
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data){
            if (data.result == 'error'){
                    
                    $scope.validate_cash_entry_error_msg = data.message;
                }else{
                    document.location.href = '/inventory/cash_entry/';

                }
                hide_loader();    
                
            }).error(function(data, status) {   
                console.log('Request failed' || data);
            });
    }

    }
    
}

function CashFlowReportController($scope,$http){

    $scope.init = function(csrf_token){
        $scope.csrf_token = csrf_token;
        $http.get('/inventory/cash_flow_report/?ajax=true').success(function(data){
            $scope.cash_flow_report = data.cash_entries;
            //paginate($scope.stocks_report, $scope, 15);
        }).error(function(data, status){
            console.log('Request failed');
        });
    }

    $scope.current_item_details = [];
    $scope.focusIndex = 0;
    $scope.keys = [];
    $scope.keys.push({ code: 13, action: function() { $scope.select_list_item( $scope.focusIndex ); }});
    $scope.keys.push({ code: 38, action: function() { 
        if($scope.focusIndex > 0){
            $scope.focusIndex--; 
        }
    }});
    $scope.keys.push({ code: 40, action: function() { 
        if($scope.batches != undefined && $scope.batches.length > 0 && $scope.focusIndex < $scope.batches.length-1){
            if($scope.focusIndex < $scope.batches.length-1){
                $scope.focusIndex++; 
            }
        } 
    }});
    $scope.$on('keydown', function( msg, code ) {
        $scope.keys.forEach(function(o) {
          if ( o.code !== code ) { return; }
          o.action();
          $scope.$apply();
        });
    });
    
    $scope.hide_popup = function() {
        hide_popup();
    }
    $scope.select_list_item = function(index) {
        if ($scope.batches != undefined && $scope.batches.length > 0) {
            batch = $scope.batches[index];
            $scope.select_batch(batch);
        } 
    }
    $scope.select_batch = function(batch) {
        $scope.closed_flag=batch.closed_flag
        $scope.batch = batch.id;
        $scope.batches = [];
        $scope.batch_name = batch.name;
        $scope.focusIndex = 0;
        $scope.generate_list();
    }
    // $scope.get_batch_list = function() {
    //     get_batch_search_details($scope, $http);
    // }
    $scope.get_batch_list = function(){
        $scope.batch = '';
        if ($scope.batch_name.length > 0)
            search_batch_for_report($scope, $http);
    }
    // $scope.calculate_purchase_price = function(batch_item){
    //     $scope.total_purchase_price = 0;
    //     batch_item.total_purchase_price = (parseFloat(batch_item.stock)*parseFloat(batch_item.purchase_price))
    // }
    
    $scope.generate_list = function(){
        $scope.no_batch_msg = '';
        console.log ($scope.batch_name);
        

        if ($scope.batch_name == '' || $scope.batch_name == undefined) {
            $scope.no_batch_msg = 'Please Choose batch';

        } else {
            // if (type_name == 'view') { 
                show_loader();
                $http.get('/inventory/cash_flow_report/?batch_id='+$scope.batch+'&pdf=false').success(function(data){
                    $scope.cash_entries = data.cash_entries;
                    $scope.total_amount_recieved = data.total_amount_recieved;
                    $scope.total_selling_price = data.total_selling_price;
                    if ($scope.total_selling_price != 0){
                        $scope.total_cash_to_be_collected = $scope.total_selling_price - $scope.total_amount_recieved; 
                    }
                    else {
                        $scope.total_cash_to_be_collected=0
                    }
                    console.log($scope.cash_entries);
                    
                    if ($scope.cash_entries.length == 0)
                        $scope.no_batch_msg = 'No Cash entries for this Batch';
                    // else if($scope.total_purchase_price.length==0)
                    //     $scope.no_batch_msg = 'No items';

                    else {
                        
                        paginate($scope.cash_entries,$scope, 15);
                        console.log("ololol");
                        
                        
                        
                    }
                    hide_loader();
                }).error(function(data, status){
                    console.log(data);
                });
            // } else
            //     document.location.href = '/inventory/closing_stock/?batch_id='+$scope.batch;
        }
    }
    $scope.select_page = function(page){
        select_page(page, $scope.stocks_report, $scope, 15);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.generate_pdf = function(){
        console.log("pdf")
        document.location.href = '/inventory/cash_flow_report/?batch_id='+$scope.batch+'&pdf=true';
    }

}