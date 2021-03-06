'use strict';

angular.module('py-ferry')
.controller('GamesDetailCtrl', 
['$scope', '$state', 'Game', 'Utils', '$uibModal', 'FerryClass', 'Terminal', 'Ferry', 'Route', 'TurnResult', '_', 'currencyScalerFilter',
function($scope, $state, Game, Utils, $uibModal, FerryClass, Terminal, Ferry, Route, TurnResult, _, currencyScalerFilter) {
    
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
    
    $scope.endTurn = function(turns) {
        Game.endTurn(gameId, turns);
    };
    
    $scope.ferry = {};
    
    $scope.ferry.buy = function() {
        var modalInstance = $uibModal.open({
           animation: $scope.animationsEnabled,
           templateUrl: 'views/games/modals/games-detail-ferry-buy-modal.html',
           controller: 'GamesDetailFerryBuyModalInstanceCtrl',
           size: 'md',
           resolve: {
               ferryClasses: function() {
                   return $scope.ferryClasses;
               },
               game: function() {
                   return $scope.game();
               }
           }
        });
        
        modalInstance.result.then(function(ferry) {
            $scope.ferries.push(ferry);
        }, function() {
          console.info('Modal dismissed at: ' + new Date());
        });
    };
    
    $scope.ferry.sell = function() {
        var modalInstance = $uibModal.open({
           animation: $scope.animationsEnabled,
           templateUrl: 'views/games/modals/games-detail-ferry-sell-modal.html',
           controller: 'GamesDetailFerrySellModalInstanceCtrl',
           size: 'md',
           resolve: {
               ferries: function() {
                   return $scope.game().ferries;
               },
               game: function() {
                   return $scope.game();
               }
           }
        });
        
        modalInstance.result.then(function(ferryId) {
            _.remove($scope.ferries, {id: ferryId});
        }, function() {
          console.info('Modal dismissed at: ' + new Date());
        });
    };
    
    $scope.ferry.maintenance = function() {
        var modalInstance = $uibModal.open({
           animation: $scope.animationsEnabled,
           templateUrl: 'views/games/modals/games-detail-ferry-maintenance-modal.html',
           controller: 'GamesDetailFerryMaintenanceModalInstanceCtrl',
           size: 'md',
           resolve: {
               ferries: function() {
                   return $scope.game().ferries;
               },
               game: function() {
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
    
    $scope.route = {};
    
    $scope.route.create = function() {
        var modalInstance = $uibModal.open({
           animation: $scope.animationsEnabled,
           templateUrl: 'views/games/modals/games-detail-route-create-modal.html',
           controller: 'GamesDetailRouteCreateModalInstanceCtrl',
           size: 'md',
           resolve: {
               terminals: function() {
                   return $scope.terminals;
               },
               game: function() {
                   return $scope.game();
               },
               ferries: function() {
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
           templateUrl: 'views/games/modals/games-detail-route-edit-modal.html',
           controller: 'GamesDetailRouteEditModalInstanceCtrl',
           size: 'md',
           resolve: {
               terminals: function() {
                   return $scope.terminals;
               },
               game: function() {
                   return $scope.game();
               },
               ferries: function() {
                    return $scope.game().ferries;
               },
               routes: function() {
                   return $scope.game().routes;
               }
           }
        });
        
        modalInstance.result.then(function(route) {
            var index = _.findIndex($scope.routes, {id: route.id});
            $scope.routes.splice(index, 1, route);
            Ferry.list(gameId)
            .then(function(response) {
                    $scope.ferries = response; 
                })
                .catch(function(error) {
                    console.error(error);
                });
        }, function() {
          console.info('Modal dismissed at: ' + new Date());
        });
    }
    
    $scope.turnResults = {};
    
    $scope.turnResults.open = function() {
        var modalInstance;
        TurnResult.fetch($scope.game().id, $scope.game().current_year, $scope.game().current_week - 1)
          .then(function(response) {
              modalInstance = $uibModal.open({
               animation: $scope.animationsEnabled,
               templateUrl: 'views/games/modals/games-detail-turn-results-modal.html',
               controller: 'GamesDetailTurnResultsModalInstanceCtrl',
               size: 'lg',
               resolve: {
                  turnResult: function() {
                      // TODO handle the new year problem here
                      return response;
                  }
               }
            });
          })
          .catch(function(error) {
              console.error(error);
          });
        
        
        modalInstance.result.then(function() {
            
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