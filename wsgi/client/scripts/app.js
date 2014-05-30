//
// Starting point of the application
//
angular.module('myApp', [
    'ngRoute',
    'ngResource',
    'ngSanitize',
    // 'ngCookies',
    // 'ui.bootstrap',
    'reCAPTCHA'
    ])
    .config(function ($routeProvider, $locationProvider, reCAPTCHAProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'scripts/views/home.html',
            })

            .when('/about', {
                templateUrl: 'scripts/views/about.html',
            })

            .when('/subscribe', {
                templateUrl: 'scripts/views/subscription.html',
                controller: 'SubscriptionController'
            })

            .when('/verify', {
                templateUrl: 'scripts/views/subscription-verify.html',
            })

            .when('/verify-failed', {
                templateUrl: 'scripts/views/subscription-verify-failed.html',
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

            // use the HTML5 History API
		        $locationProvider.html5Mode(true);

            // Set recaptch public key
            reCAPTCHAProvider.setPublicKey('6LfnLPQSAAAAAIHLspjC8C8PRrf1FlEqK_tes9WD');

            // optional: gets passed into the Recaptcha.create call
            reCAPTCHAProvider.setOptions({
                theme: 'white'
            });
    });
