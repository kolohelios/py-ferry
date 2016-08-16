'use strict';

angular.module('py-ferry')
.controller('GamesDetailRouteEditModalInstanceCtrl', 
['$scope', '$uibModalInstance', 'terminals', 'game', 'ferries', 'routes', 'Route', '_',
function ($scope, $uibModalInstance, terminals, game, ferries, routes, Route, _) {

  $scope.terminals = terminals;
  $scope.game = game;
  $scope.ferries = ferries;
  $scope.availableFerries = [];
  $scope.ferriesObject = {};
  $scope.routes = routes;
  $scope.terminal1Id = 0;
  $scope.terminal2Id = 0;
  
  $scope.route = {};
  
  $scope.selectRoute = function(route) {
    $scope.route = _.cloneDeep(route);
    $scope.availableFerries = [];
    $scope.ferriesObject = {};
    $scope.availableFerries = $scope.ferries.filter(function(ferry) {
      if(!(ferry.route && ferry.route.id)) {
        $scope.ferriesObject[ferry.id] = false;
        return true;
      } else if(ferry.route.id == $scope.route.id) {
        $scope.ferriesObject[ferry.id] = true;
        return true;
      }
      return false;
    });
    $scope.route.terminal1Id = $scope.route.first_terminal.id;
    $scope.route.terminal2Id = $scope.route.second_terminal.id;
    delete $scope.route.first_terminal;
    delete $scope.route.second_terminal;
    delete $scope.route.route_distance;
  };
  
  $scope.save = function () {
    $scope.route.ferries = [];
    console.log($scope.ferriesObject);
    for(var ferry in $scope.ferriesObject) {
      if($scope.ferriesObject[ferry]) {
        $scope.route.ferries.push(ferry);  
      }
    }
    Route.save(game.id, $scope.route)
    .then(function(response) {
      $uibModalInstance.close(response);
    })
    .catch(function(error) {
      console.error(error);
    });
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}]);