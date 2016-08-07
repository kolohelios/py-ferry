'use strict';

angular.module('py-ferry')
.controller('GamesDetailCtrl', 
['$scope', '$state', 'Game', 'Utils', '$uibModal', 'FerryClass', 'Terminal', 'Ferry',
function($scope, $state, Game, Utils, $uibModal, FerryClass, Terminal, Ferry) {
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
       
    Terminal.list()
        .then(function(response) {
          $scope.terminals = response; 
       })
       .catch(function(error) {
           console.error(error);
       });
     
    Ferry.list(gameId)
        .then(function(response) {
          $scope.ferries = response; 
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
           controller: 'GamesDetailFerryBuyModalInstanceCtrl',
           size: 'md',
           resolve: {
               ferryClasses: function() {
                   console.log($scope.ferryClasses);
                   return $scope.ferryClasses;
               },
               gameId: function() {
                   return gameId;
               }
           }
        });
        
        modalInstance.result.then(function() {
        }, function() {
          console.info('Modal dismissed at: ' + new Date());
        });
    }
    
    $scope.route = {};
    
    $scope.route.create = function() {
        var modalInstance = $uibModal.open({
           animation: $scope.animationsEnabled,
           templateUrl: 'views/games/games-detail-route-create-modal.html',
           controller: 'GamesDetailRouteCreateModalInstanceCtrl',
           size: 'md',
           resolve: {
               terminals: function() {
                   console.log($scope.terminals);
                   return $scope.terminals;
               }
           }
        });
        
        modalInstance.result.then(function() {
        }, function() {
          console.info('Modal dismissed at: ' + new Date());
        });
    }
}]);