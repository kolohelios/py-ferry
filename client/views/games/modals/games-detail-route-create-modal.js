'use strict';

angular.module('py-ferry')
.controller('GamesDetailRouteCreateModalInstanceCtrl', ['$scope', '$uibModalInstance', 'terminals', 'game', 'ferries', 'Route', function ($scope, $uibModalInstance, terminals, game, ferries, Route) {

  $scope.terminals = terminals;
  $scope.game = game;
  $scope.ferries = ferries;
  
  $scope.alerts = [];
  
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
      $uibModalInstance.close(response);
    })
    .catch(function(error) {
      if(error.data.message === 'A route already exists with these two terminals.') {
        $scope.alerts.push({msg: error.data.message});
      }
      console.error(error);
    });
  };
  
  $scope.closeAlert = function(index) {
    $scope.alerts.splice(index, 1);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}]);