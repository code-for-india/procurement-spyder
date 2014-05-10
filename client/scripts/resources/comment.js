//
// Project comments Resource
//

angular.module('myApp').factory('Comments', function ($resource) {

    var resource =  $resource('/projects/:projectId/comments/:id',
      { id: '@_id', projectId: '@projectId' });

    return resource;
});
