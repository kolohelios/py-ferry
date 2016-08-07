'use strict';

angular.module('py-ferry')
.controller('GamesDetailCtrl', ['$scope', '$state', 'Game', 'Utils', '$uibModal', 'FerryClass', function($scope, $state, Game, Utils, $uibModal, FerryClass) {
    if(!Utils.userLoggedIn()) {
        $state.go('login');
    }
    
    var gameId = $state.params.gameId;
    
    FerryClass.list()
       .then(function(response) {
          $scope.ferryClasses = response; 
       })
       .catch(function(error) {
           console.error(error);
       });
    
    $scope.animationsEnabled = true;
    
    Game.fetch(gameId)
    .then(function(response) {
        $scope.game = response.data;
    })
    .catch(function(error){
        console.error(error);
        console.log(error);
    });
    
    $scope.ferry = {};
    
    $scope.ferry.buy = function() {
        var modalInstance = $uibModal.open({
           animation: $scope.animationsEnabled,
           templateUrl: 'views/games/games-detail-ferry-buy-modal.html',
           controller: 'ModalInstanceCtrl',
           size: 'md',
           resolve: {
               ferryClasses: function() {
                   console.log($scope.ferryClasses);
                   return $scope.ferryClasses;
               }
           }
        });
        
        modalInstance.result.then(function (selectedItem) {
          $scope.selected = selectedItem;
        }, function () {
          console.info('Modal dismissed at: ' + new Date());
        });
    }
}]);