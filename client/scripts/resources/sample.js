//
// Sample User Resource
//

angular.module('myApp').factory('User', function ($resource) {

    var userResource =  $resource('/users/:id', { id: '@_id' });

    return userResource;
});
