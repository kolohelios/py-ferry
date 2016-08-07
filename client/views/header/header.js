'use strict';

angular.module('py-ferry')
.controller('NavCtrl', ['$scope', '$state', 'User', function($scope, $state, User) {
  User.checkTokenFromLocalStorage()
  .then(function(response) {
    console.log(response);
    $state.go('gamesList');
  })
  .catch(function(error) {
    console.error(error);
    $state.go('login')
  });
  
  $scope.logout = function() {
    User.logout();
    $state.go('login');
  }
  
  $scope.isCollapsed = true;

  $scope.collapse = function() {
    $scope.isCollapsed = true;
  };
}]);
