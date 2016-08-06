'use strict';

angular.module('py-ferry')
.factory('User', ['$http', '$window', '$q', 'apiUrl', '_', 'localStorage', function($http, $window, $q, apiUrl, _, localStorage) {
  function User() {}
  
  User.user = {};

  User.login = function(data) {
    var self = this;
     
    var d = $q.defer();
    $http({
      method: 'POST',
      url: apiUrl + '/auth',
      data: data
    })
    .then(function(response) {
        var token = response.data.access_token;
        $http.defaults.headers.common.Authorization = 'JWT ' + token;
        localStorage.setItem('accessToken', token);
        self.getUser()
        .then(function(response) {
            self.user = response.data;
            d.resolve(self.user);
        })
        .catch(function(error) {
            d.reject(error);
        });
    })
    .catch(function(error) {
        d.reject(error);
    });
    return d.promise;
  };
  
  User.getUser = function() {
      return $http({
      method: 'GET',
      url: apiUrl + '/user',
    });
  };

  return User;
}]);
