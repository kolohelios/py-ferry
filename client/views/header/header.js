'use strict';

angular.module('py-ferry')
.controller('NavCtrl', ['$scope', '$state', 'User', 'Utils', 'Game', function($scope, $state, User, Utils, Game) {
  
  $scope.logout = function() {
    User.logout();
    $state.go('login');
  }
 
  $scope.game = function() {
    return Game.getActiveGame();
  };
  
  $scope.isCollapsed = true;

  $scope.collapse = function() {
    $scope.isCollapsed = true;
  };
  
  $scope.userLoggedIn = function() {
    return User.user.id && User.user.id > 0;
  };
}]);
