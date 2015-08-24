

var app = angular.module('app', ['ngRoute', 'ui.bootstrap']);
app.controller('loginCtrl', function($scope, $http){
    $scope.login = function(){
       var email = $scope.username;
       var password = $scope.password;
        var url = '/login';
        var data = {
            email: email,
            password: password
        };

        $http.post(url, data).
            then(function(response) {
                console.log(response);
                var data = response['data']
                var user = data['node']
                window.location = user['slug']
            }, function(response) {
                console.log(response);
        });
    };

});

app.controller('registerCtrl', function($scope, $http){
   $scope.register = function() {
       var name = $scope.name;
       var email = $scope.username;
       var password = $scope.password;
       var confirm = $scope.confirmPassword;
       var url = '/editors/invoke'
       var message = {
           type : 'user',
           command : 'register',
           data : {
               name : name,
               email : email,
               password : password,
               confirm : confirm,
               roles : ['Basic User']
           }
       };
        if (name != null && email != null && password != null && confirm != null) {
            $http.post(url, message).
                then(function (response) {
                    console.log(response);
                    var data = response['data']
                    var user = data['node']
                    window.location = user['slug']
                }, function (error) {
                    console.log(error);
                });
        }
   };
});

app.controller('profileCtrl', function ($scope, $document , $http) {

    $scope.edit_contact_info = function() {
        var phone = $('.phone-display').text().replace(/\s/g, '')
        var mobile = $('.mobile-display').text().replace(/\s/g, '')
        var address = $('.address-display').text()

        console.log(address)

        $(".details-info").addClass('hidden');
        $(".details-info-edit").removeClass('hidden');
        $(".phone-number-edit").val(phone);
        $(".mobile-number-edit").val(mobile);
        $(".address-edit").text(address.trim());

    }

    $scope.cancel_update_contact = function () {
        console.log('Reached Cancel')
        $(".details-info-edit").addClass('hidden');
        $(".details-info").removeClass('hidden');
    }

    $scope.update_contact_info = function () {
        console.log('Reached Update')
        var message = {
            node : $('.profile-id').val(),
            type : 'user',
            command : 'update-contact-info',
            data : {
                address : $scope.address,
                phone : $scope.phone,
                mobile : $scope.mobile
            }
        };
        console.log(message);
        var url = '/editors/invoke';
        $http.post(url, message).
            then(function (response) {
                console.log(response);
                var data = response['data']
                var user = data['node']
                window.location = user['slug']
            }, function (error) {
                console.log(error);
            });
    }
});

