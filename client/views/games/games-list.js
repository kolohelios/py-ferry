'use strict';

angular.module('py-ferry')
.controller('GamesListCtrl', ['$scope', '$state', 'Game', 'Utils', function($scope, $state, Game, Utils) {

    Game.list()
    .then(function() {
        $scope.games = Game.games;
    })
    .catch(function(error){
        console.error(error);
        console.log(error);
    });
    
    $scope.createGame = function() {
        Game.createGame();
    };
    
    $scope.deleteGame = function(gameId) {
        Game.deleteGame(gameId)
    };
}]);