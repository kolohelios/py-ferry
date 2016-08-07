'use strict';

angular.module('py-ferry')
.factory('Ferry', ['$http', '$window', '$q', 'apiUrl', '_', function($http, $window, $q, apiUrl, _) {
  function Ferry() {}

  Ferry.buy = function() {
    var self = this;
    var d = $q.defer();
    $http({
      method: 'GET',
      url: apiUrl + '/games'
    })
    .then(function(response) {
        self.games = response.data;
        d.resolve(response);
    })
    .catch(function(error) {
        d.reject(error);
    });
    return d.promise;
  };

  return Ferry;
}]);
