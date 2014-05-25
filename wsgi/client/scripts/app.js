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

            .when('/success', {
                templateUrl: 'scripts/views/subscription-success.html',
            })

            .when('/updated', {
                templateUrl: 'scripts/views/subscription-updated.html',
            })

            .when('/unsubscribed', {
                templateUrl: 'scripts/views/subscription-deleted.html',
            })

            .otherwise({redirectTo: function() { return '/'; }});
    });
