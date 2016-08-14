'use strict';

angular.module('py-ferry')
.controller('GamesDetailFerrySellModalInstanceCtrl', ['$scope', '$uibModalInstance', 'game', 'ferries', 'Ferry', function ($scope, $uibModalInstance, game, ferries, Ferry) {

  $scope.game = game;
//   $scope.ferry = {};
  
//   $scope.selectFerryClass = function(ferryClass) {
//     if(ferryClass.cost > $scope.game.cash_available) {
//       alert('Cannot afford this ferry.'); 
//     } else {
//       $scope.ferry.classId = ferryClass.id;  
//     }
//   };

  $scope.sell = function (ferryId) {
    Ferry.sell(game.id, ferryId)
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