'use strict';

angular.module('py-ferry')
.controller('GamesDetailFerrySellModalInstanceCtrl', ['$scope', '$uibModalInstance', 'game', 'ferries', 'Ferry', function ($scope, $uibModalInstance, game, ferries, Ferry) {

  $scope.game = game;
  $scope.ferries = ferries;
  $scope.ferryId = -1;

  $scope.selectFerry = function(ferryId) {
    console.log($scope.ferryId, ferryId);
    if($scope.ferryId == ferryId) {
      $scope.ferryId = -1;
    } else {
      $scope.ferryId = ferryId;
    }
  };

  $scope.sell = function() {
    Ferry.sell(game.id, $scope.ferryId)
    .then(function(response) {
      $uibModalInstance.close(response.id);
    })
    .catch(function(error) {
      console.error(error);
    });
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}]);