'use strict';

angular.module('py-ferry')
.controller('GamesDetailRouteCreateModalInstanceCtrl', ['$scope', '$uibModalInstance', 'terminals', 'game', 'ferries', 'Route', function ($scope, $uibModalInstance, terminals, game, ferries, Route) {

  $scope.terminals = terminals;
  $scope.game = game;
  $scope.ferries = ferries;
  
  $scope.route = {};
  
  $scope.create = function () {
    var ferriesObject = $scope.route.ferries;
    $scope.route.ferries = [];
    for(var ferry in ferriesObject) {
      $scope.route.ferries.push(ferry);
    }
    console.log($scope.route);
    Route.create(game.id, $scope.route)
    .then(function(response) {
      $uibModalInstance.close(response.data);
    })
    .catch(function(error) {
      console.error(error);
    });
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}]);