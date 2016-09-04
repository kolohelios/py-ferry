'use strict';

angular.module('py-ferry')
.filter('currencyScaler', [function() {
    return function(input) {
        console.log(input);
        input = input * 1 || 0;
        switch(input.toString().length) {
            case 1:
            case 2:
            case 3:
            case 4:
                return '$' + input;
            case 5:
            case 6:
                return '$' + (input / 1000).toFixed(2) + ' thousand';
            case 7:
            case 8:
            case 9:
                return '$' + (input / 1000000).toFixed(2) + ' million';
            default:
                return 'too large!';
        }
    };
}]);