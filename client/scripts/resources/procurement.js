//
// Project procurements Resource
//

angular.module('myApp').factory('Procurements', function ($resource) {

    var resource =  $resource('/projects/:projectId/procurements/:id',
      { id: '@_id', projectId: '@projectId' });

    return resource;
});
