'use strict';

angular.module('py-ferry')
.filter('currencyScaler', [function() {
    return function(input) {
        input = input || '';
        console.log(input);
        return input;
    };
}]);