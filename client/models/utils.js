'use strict';

angular.module('py-ferry')
.factory('Utils', ['$http', '$window', '$q', 'apiUrl', '_', 'User', function($http, $window, $q, apiUrl, _, User) {
  function Utils() {}

  Utils.userLoggedIn = function() {
    var d = $q.defer();
    if(User.user.id && User.user.id > 0) {
        d.resolve(true);
    } else if(!User.checkedLocalStorage) {
      User.checkedLocalStorage = true;
      User.checkTokenFromLocalStorage()
      .then(function(response) {
        d.resolve(true);
        console.log(response);
      })
      .catch(function(error) {
        d.reject(error);
        console.error(error);
      });
    }
    return d.promise;
  };
  
  return Utils;
}]);
