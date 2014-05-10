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
                templateUrl: 'scripts/views/home.html',
            })
            .when('/hello', {
                templateUrl: 'scripts/views/hello.html',
                controller: 'ShowController'
            })

            .otherwise({redirectTo: function() { return '/'; }});
    });

// angular.module('myApp')
//     .run(function($rootScope) {
//     });
