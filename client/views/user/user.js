'use strict';

angular.module('py-ferry')
.controller('UserCtrl', ['$scope', '$state', 'User', function($scope, $state, User) {
    $scope.player = {};
    
    $scope.login = function() {
        User.login($scope.player)
        .then(function(response) {
            console.log(response);
            $state.go('games');
        })
        .catch(function(error){
            console.error(error);
        });
    }
}]);
