'use strict';

angular.module('py-ferry')
.controller('ModalInstanceCtrl', ['$scope', '$uibModalInstance', 'ferryClasses', 'gameId', 'Ferry', function ($scope, $uibModalInstance, ferryClasses, gameId, Ferry) {

  $scope.ferryClasses = ferryClasses;
  $scope.ferry = {};
  
  $scope.selectFerryClass = function(classId) {
    $scope.ferry.classId = classId;
  };

  $scope.buy = function () {
    Ferry.buy(gameId, $scope.ferry)
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