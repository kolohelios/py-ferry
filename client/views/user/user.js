'use strict';

angular.module('py-ferry')
.controller('UserCtrl', ['$scope', '$state', 'User', function($scope, $state, User) {
    $scope.player = {};
    var passCheck = /([A-Z0-9 -]{8,12})\w+/i
    
    $scope.login = function() {
        User.login($scope.player)
        .then(function(response) {
            $state.go('gamesList');
        })
        .catch(function(error){
            console.error(error);
        });
    }
    
    $scope.checkPassword = function() {
        if($scope.player.password !== $scope.confirmPassword)  {
            console.error('Passwords do not match!');
            return false;
        } else if(!$scope.player.password.match(passCheck)) {
            console.error('bad password!');
            return false;
        }
        console.log('good password!');
        return true;
    }
}]);
