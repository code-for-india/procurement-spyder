//
// Projects Resource
//

angular.module('myApp').factory('Projects', function ($resource) {

    var resource =  $resource('/projects/:id', { id: '@_id' });

    return resource;
});
