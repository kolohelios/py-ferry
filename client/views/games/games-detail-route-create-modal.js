'use strict';

angular.module('py-ferry')
.controller('GamesDetailRouteCreateModalInstanceCtrl', ['$scope', '$uibModalInstance', 'terminals', 'game', 'Route', function ($scope, $uibModalInstance, terminals, game, Route) {

  $scope.terminals = terminals;
  $scope.game = game;
  
  $scope.route = {};
  
  $scope.create = function () {
    Route.create(game.id, $scope.route)
    .then(function(response) {
      $uibModalInstance.close();
    })
    .catch(function(error) {
      console.error(error);
    });
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}]);