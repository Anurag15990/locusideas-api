
var app = angular.module('login', ['ngRoute']);
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
                }, function (error) {
                    console.log(error);
                });
        }
   };
});
