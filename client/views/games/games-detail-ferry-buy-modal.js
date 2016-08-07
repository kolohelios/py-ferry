'use strict';

angular.module('py-ferry')
.controller('ModalInstanceCtrl', ['$scope', '$uibModalInstance', 'ferryClasses', function ($scope, $uibModalInstance, ferryClasses) {

  $scope.ferryClasses = ferryClasses;

  $scope.ok = function () {
    $uibModalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}]);