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
                templateUrl: 'scripts/views/subscription.html',
                controller: 'SubscriptionController'
            })

            .when('/about', {
                templateUrl: 'scripts/views/about.html',
            })

            .otherwise({redirectTo: function() { return '/'; }});
    });
