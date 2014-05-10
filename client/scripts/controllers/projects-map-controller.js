angular.module('myApp').controller('ProjectsMapController',
        function($scope, $routeParams, Projects) {

  $scope.projects = Projects.query();
  $scope.map = {
    center: {
        latitude: 45,
        longitude: -73
    },
    zoom: 8
  };
});
