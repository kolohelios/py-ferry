'use strict';

angular.module('py-ferry')
.controller('GamesCtrl', ['$scope', '$state', 'Game', 'Utils', function($scope, $state, Game, Utils) {
    if(!Utils.userLoggedIn()) {
        $state.go('login');
    }
    
    Game.list()
    .then(function() {
        $scope.games = Game.games;
    })
    .catch(function(error){
        console.error(error);
    });
    
    $scope.createGame = function() {
      Game.createGame();
    };
}]);