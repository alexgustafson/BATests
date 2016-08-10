angular.module('app').controller('ProcessManager', ['$scope', '$http', function ($scope, $http) {
  $scope.showNewEditor = false;
  $scope.showEditEditor = false;
  $scope.activeProcessQueue = {};
  $scope.newProcess = {
    title: ''
  };
  $scope.submitProcess = function () {

    $http.post('/api/processqueue/', $scope.newProcess).success(function (data) {
      console.log(data);
    })
  }

  $scope.toggleNewEditor = function () {
    $scope.showEditEditor = false;
    $scope.showNewEditor = !$scope.showNewEditor;
  }

  $scope.toggleEditEditor = function () {
    $scope.showNewEditor = false;
    $scope.showEditEditor = !$scope.showEditEditor;
  }

}]);


angular.module('app').controller('ProcessQueueListController', ['$scope', '$http', function ($scope, $http) {

  $scope.processQueue = {};
  $scope.processQueueList = [];


  $http.get('/api/processqueue/').success(function (data) {

    console.log(data);
    $scope.processQueueList = data;

  });


}]);

angular.module('app').controller('ProcessQueueEditor', ['$scope', '$http', function ($scope, $http) {

  $scope.showNewEditor = false;
  $scope.showEditEditor = false;
  $scope.activeItem = {};

  $scope.$watch(
    'activeProcessQueue',
    function (newValue, oldValue) {
      $http.get('/api/processqueueitem/', {'params': {'queue': newValue.id}}).success(function (data) {

        console.log(data);
        $scope.processQueueItems = data;

      });

    }
  );

  $scope.toggleNewEditor = function () {
    $scope.showEditEditor = false;
    $scope.showNewEditor = !$scope.showNewEditor;
  }

  $scope.toggleEditEditor = function (item) {
    $scope.activeItem = item;
    $scope.showNewEditor = false;
    $scope.showEditEditor = !$scope.showEditEditor;
  }


}]);