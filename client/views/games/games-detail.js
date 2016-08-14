'use strict';

angular.module('py-ferry')
.controller('GamesDetailCtrl', 
['$scope', '$state', 'Game', 'Utils', '$uibModal', 'FerryClass', 'Terminal', 'Ferry', 'Route', '_',
function($scope, $state, Game, Utils, $uibModal, FerryClass, Terminal, Ferry, Route, _) {
    
    $scope.oneAtATime = true;
    
    var gameId = $state.params.gameId;
    
    Utils.userLoggedIn()
    .then(function() {
        // player is loaded
        FerryClass.list()
           .then(function(response) {
              $scope.ferryClasses = response; 
           })
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
           
        Game.fetch(gameId)
            .then(function(response) {
                $scope.game = Game.activeGame;
                $scope.game = function() {
                    return Game.getActiveGame();
                  };
                console.log($scope.game());
            })
            .catch(function(error){
                console.error(error);
            });
            
        Route.list(gameId)
            .then(function(response) {
                $scope.routes = response;
            })
            .catch(function(error){
                console.error(error);
            });
    })
    .catch(function(error) {
       console.error(error);
       $state.go('login');
    });
    
    $scope.animationsEnabled = false;
    
    $scope.endTurn = function() {
        Game.endTurn(gameId);  
    };
    
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
               game: function() {
                   console.log($scope.game);
                   return $scope.game();
               }
           }
        });
        
        modalInstance.result.then(function(ferry) {
            $scope.ferries.push(ferry);
        }, function() {
          console.info('Modal dismissed at: ' + new Date());
        });
    }
    
    $scope.ferry.sell = function() {
        var modalInstance = $uibModal.open({
           animation: $scope.animationsEnabled,
           templateUrl: 'views/games/games-detail-ferry-sell-modal.html',
           controller: 'GamesDetailFerrySellModalInstanceCtrl',
           size: 'md',
           resolve: {
               ferries: function() {
                   console.log($scope.ferries);
                   return $scope.ferries;
               },
               game: function() {
                   console.log($scope.game);
                   return $scope.game();
               }
           }
        });
        
        modalInstance.result.then(function(ferryId) {
            _.remove($scope.ferries, {id: ferryId});
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
               },
               game: function() {
                   console.log($scope.game);
                   return $scope.game();
               },
               ferries: function() {
                    console.log($scope.ferries);
                    var ferries = $scope.ferries.slice(0);
                    var unassignedFerries = _.filter($scope.ferries, function(ferry) {
                        return !ferry.route.id;
                    });
                   console.log(unassignedFerries);
                   return unassignedFerries;
               }
           }
        });
        
        modalInstance.result.then(function(route) {
            $scope.routes.push(route);
        }, function() {
          console.info('Modal dismissed at: ' + new Date());
        });
    }
    
    $scope.route.edit = function() {
        var modalInstance = $uibModal.open({
           animation: $scope.animationsEnabled,
           templateUrl: 'views/games/games-detail-route-edit-modal.html',
           controller: 'GamesDetailRouteEditModalInstanceCtrl',
           size: 'md',
           resolve: {
               terminals: function() {
                   console.log($scope.terminals);
                   return $scope.terminals;
               },
               game: function() {
                   console.log($scope.game);
                   return $scope.game();
               },
               ferries: function() {
                   console.log($scope.game);
                   return $scope.ferries;
               },
               routes: function() {
                   console.log($scope.routes);
                   return $scope.routes;
               }
           }
        });
        
        modalInstance.result.then(function(route) {
            $scope.routes.push(route);
        }, function() {
          console.info('Modal dismissed at: ' + new Date());
        });
    }
    
    $scope.$on('$locationChangeStart', function( event, newUrl ) {
      if (newUrl.indexOf('/games/') == -1) {
        Game.activeGame = {};
      }
    });
}]);