'use strict';

angular.module('py-ferry')
.controller('GamesDetailRouteEditModalInstanceCtrl', 
['$scope', '$uibModalInstance', 'terminals', 'game', 'ferries', 'routes', 'Route', '_',
function ($scope, $uibModalInstance, terminals, game, ferries, routes, Route, _) {

  $scope.terminals = terminals;
  $scope.game = game;
  $scope.ferries = ferries;
  $scope.availableFerries = [];
  $scope.routes = routes;
  $scope.terminal1Id = 0;
  $scope.terminal2Id = 0;
  
  $scope.route = {};
  
  $scope.selectRoute = function(route) {
    $scope.route = _.clone(route);
    $scope.availableFerries = _.filter($scope.ferries, function(ferry) {
      return !ferry.route.id || ferry.route.id == $scope.route.id;
    });
    $scope.route.terminal1Id = $scope.route.first_terminal.id;
    $scope.route.terminal2Id = $scope.route.second_terminal.id;
    delete $scope.route.first_terminal;
    delete $scope.route.second_terminal;
    delete $scope.route.route_distance;
  };
  
  $scope.save = function () {
    var ferriesObject = $scope.route.ferries;
    $scope.route.ferries = [];
    for(var ferry in ferriesObject) {
      $scope.route.ferries.push(ferry);
    }
    Route.save(game.id, $scope.route)
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