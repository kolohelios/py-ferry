'use strict';

angular.module('py-ferry')
.controller('NavCtrl', ['$scope', '$state', 'User', 'Utils', function($scope, $state, User, Utils) {
  
  // Utils.userLoggedIn();
  
  $scope.logout = function() {
    User.logout();
    $state.go('login');
  }
  
  $scope.isCollapsed = true;

  $scope.collapse = function() {
    $scope.isCollapsed = true;
  };
  
  $scope.userLoggedIn = function() {
    return User.user.id && User.user.id > 0;
  };
}]);
