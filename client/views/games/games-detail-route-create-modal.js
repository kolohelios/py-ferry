'use strict';

angular.module('py-ferry')
.controller('GamesDetailRouteCreateModalInstanceCtrl', ['$scope', '$uibModalInstance', 'terminals', 'Ferry', function ($scope, $uibModalInstance, terminals, Ferry) {

  $scope.terminals = terminals;
  $scope.route = {};
  
//   $scope.selectFerryClass = function(classId) {
//     $scope.ferry.classId = classId;
//   };

//   $scope.buy = function () {
//     Ferry.buy(gameId, $scope.ferry)
//     .then(function(response) {
//       $uibModalInstance.close();
//     })
//     .catch(function(error) {
//       console.error(error);
//     });
//   };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}]);