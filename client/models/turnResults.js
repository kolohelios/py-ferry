'use strict';

angular.module('py-ferry')
.factory('TurnResult', ['$http', '$window', '$q', 'apiUrl', '_', function($http, $window, $q, apiUrl, _) {
  function TurnResult() {}

  TurnResult.fetch = function(gameId, yearNumber, weekNumber) {
    var d = $q.defer();
    $http({
      method: 'GET',
      url: apiUrl + '/games/' + gameId + '/turn_results/' + yearNumber + '/week/' + weekNumber
    })
    .then(function(response) {
        d.resolve(response.data);
    })
    .catch(function(error) {
        d.reject(error);
    });
    return d.promise;
  };

  return TurnResult;
}]);
