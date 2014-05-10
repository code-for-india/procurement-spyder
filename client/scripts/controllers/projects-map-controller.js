angular.module('myApp').controller('ProjectsMapController',
        function($scope, $routeParams, Projects) {

  $scope.projects = Projects.query();
  $scope.map = {
    center: {
        latitude: 12,
        longitude: 78
    },
    zoom: 8,
    draggable: "true"
  };



  $scope.markers = [
    {
      latitude: 12.5,
      longitude: 78.5
    },
    {
      latitude: 12.8,
      longitude: 78.2
    }
  ];

  $scope.fit = true;

});
