'use strict';

angular.module('py-ferry')
.factory('Route', ['$http', '$window', '$q', 'apiUrl', '_', function($http, $window, $q, apiUrl, _) {
  function Route() {}
  
    Route.create = function(gameId, data) {
        return $http({
          method: 'POST',
          url: apiUrl + '/games/' + gameId + '/routes',
          data: data
        });
    };
  
    Route.list = function(gameId) {
        var d = $q.defer();
        $http({
        method: 'GET',
        url: apiUrl + '/games/' + gameId + '/routes'
        })
        .then(function(response) {
            d.resolve(response.data);
        })
        .catch(function(error) {
            d.reject(error);
        });
        return d.promise;
    }

  return Route;
}]);
