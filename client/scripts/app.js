//
// Starting point of the application
//
angular.module('myApp', [
    'ngRoute',
    'ngResource',
    'ngCookies',
    'ngSanitize',
    'ui.bootstrap'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'scripts/views/map.html',
                controller: 'ProjectsMapController'
            })
            .when('/projects', {
                templateUrl: 'scripts/views/project-list.html',
                controller: 'ProjectsListController'
            })
            .when('/projects/:id', {
                templateUrl: 'scripts/views/project-show.html',
                controller: 'ProjectShowController'
            })

            .when('/about', {
                templateUrl: 'scripts/views/about.html',
            })

            .otherwise({redirectTo: function() { return '/'; }});
    });

// angular.module('myApp')
//     .run(function($rootScope) {
//     });
