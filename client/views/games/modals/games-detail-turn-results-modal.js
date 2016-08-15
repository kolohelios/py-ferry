angular.module('py-ferry')
.controller('GamesDetailTurnResultsModalInstanceCtrl', 
['$scope', '$uibModalInstance', 'turnResult', '_', 'currencyScalerFilter', function ($scope, $uibModalInstance, turnResult, _, currencyScalerFilter) {

  $scope.turnResult = turnResult;
  console.log($scope.turnResult);
  
  $scope.rows = [];
  
  var totals = {};
  totals.passengers = 0;
  totals.fuelUsed = 0;
  totals.revenue = 0;
  $scope.turnResult.route_results.forEach(function(route) {
      var routeTotals = {};
      routeTotals.passengers = 0;
      routeTotals.fuelUsed = 0;
      routeTotals.revenue = 0;
      route.ferry_results.forEach(function(ferry) {
         var ferryRow = {};
         ferryRow.type = 'ferry';
         ferryRow.name = ferry.ferry.name;
         
         ferryRow.passengers = ferry.total_passengers + ferry.total_cars + ferry.total_trucks;
         routeTotals.passengers += ferryRow.passengers;
         totals.passengers += ferryRow.passengers;
         
         ferryRow.revenue = ferry.total_passengers * route.passenger_fare + ferry.total_cars * route.car_fare + ferry.total_trucks * route.truck_fare;
         routeTotals.revenue += ferryRow.revenue;
         totals.revenue += ferryRow.revenue;
         
         ferryRow.fuelUsed = ferry.fuel_used;
         routeTotals.fuelUsed += ferryRow.fuelUsed;
         totals.fuelUsed += ferryRow.fuelUsed;
         
         ferryRow.fuelCost = ferryRow.fuelUsed * $scope.turnResult.fuel_cost;
         
         $scope.rows.push(ferryRow);
      });
      routeTotals.type = 'route';
      routeTotals.name = route.first_terminal.name + ' to ' + route.second_terminal.name;
      routeTotals.fuelCost = routeTotals.fuelUsed * $scope.turnResult.fuel_cost;
      $scope.rows.push(routeTotals);
  });
  totals.type = 'total';
  totals.name = 'Total';
  $scope.rows.push(totals);


  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
}]);
