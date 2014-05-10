//
// Subscription Resource
//

angular.module('myApp').factory('Subscriptions', function ($resource) {

    var resource =  $resource('/subscriptions',
                              {},
                              {});

    return resource;
});
