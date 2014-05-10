//
// Project images Resource
//

angular.module('myApp').factory('Images', function ($resource) {

    var resource =  $resource('/projects/:projectId/images/:id',
      { id: '@_id', projectId: '@projectId' });

    return resource;
});
