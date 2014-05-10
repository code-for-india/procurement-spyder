//
// Subscription Resource
//

angular.module('myApp').factory('Subscription', function ($resource) {

    var resource =  $resource('/subscription',
                              {},
                              {});

    return resource;
});
