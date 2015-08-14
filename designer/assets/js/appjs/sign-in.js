var email = null;
var password = null;

var app = angular.module('login', ['ngRoute']);
app.controller('loginCtrl', function($scope, $http){
    $scope.submit = function(){
        email = $scope.username;
        password = $scope.password;
        var url = 'http://localhost:4900/editors/invoke';
        var data = {
            type: 'user',
            command: 'login',
            data: {
                email: email,
                password: password
            }
        };

        $http.post(url, data).
            then(function(response) {
                console.log(response);
            }, function(response) {
                console.log(response);
        });
    };


});

