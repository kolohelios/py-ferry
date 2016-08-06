'use strict';

angular.module('py-ferry')
.controller('NavCtrl', ['$scope', '$state', function($scope, $state) {
  $scope.isCollapsed = true;

  $scope.collapse = function() {
    $scope.isCollapsed = true;
  };
}]);
