'use strict';

angular.module('py-ferry')
.controller('GamesDetailFerryBuyModalInstanceCtrl', ['$scope', '$uibModalInstance', 'ferryClasses', 'game', 'Ferry', function ($scope, $uibModalInstance, ferryClasses, game, Ferry) {

  $scope.ferryClasses = ferryClasses;
  $scope.game = game;
  $scope.ferry = {};
  
  $scope.selectFerryClass = function(ferryClass) {
    if(ferryClass.cost > $scope.game.cash_available) {
      alert('Cannot afford this ferry.'); 
    } else {
      $scope.ferry.classId = ferryClass.id;  
    }
  };

  $scope.buy = function () {
    Ferry.buy(game.id, $scope.ferry)
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