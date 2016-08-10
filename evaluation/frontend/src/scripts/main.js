var app = angular.module('app', ['ngCookies'])

app.run(function ($http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.xsrfCookieName = 'csrftoken';
  return $http.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('MainController', ['$scope', function($scope) {

}]);



app.controller('BorderController',
  ['$scope', '$http', function ($scope, $http) {

    $scope.allLogs = [];
    $scope.focusIndex = 0;
    $scope.evaluation = {};
    $scope.border_quality_values = [
      {name: "None", id: 0},
      {name: "Precise", id: 10},
      {name: "Approximate", id: 20},
      {name: "Not Useable", id: 30},
    ];

    $http.get('/api/processlog').success(function (data) {

      $scope.allLogs = data;

    });

    $scope.selectFile = function (index) {
      $scope.focusIndex = index;
    };

    $scope.openFile = function (name) {
      $scope.activeFile = name;
      $http.get('/api/processlog/', {params: {'name': name}}).success(function (result) {
        $scope.logData = result[0];


        $http.get('/api/evaluation/' + $scope.logData.evaluation + '/').then(function (evaluation) {

          $scope.evaluation = evaluation.data;

        }, function() {
          $scope.evaluation = {
            border_quality: 0,
            region_isolate: false
          };

        })

      })
    };

    $scope.keys = [];
    $scope.keys.push({
      code: 13, action: function () {
        $scope.open($scope.focusIndex);
      }
    });
    $scope.keys.push({
      code: 38, action: function () {
        $scope.focusIndex--;
      }
    });
    $scope.keys.push({
      code: 40, action: function () {
        $scope.focusIndex++;
      }
    });

    $scope.$on('keydown', function (msg, obj) {
      var code = obj.code;
      $scope.keys.forEach(function (o) {
        if (o.code !== code) {
          return;
        }
        o.action();
        $scope.$apply();
      });
    });

    $scope.$watch('focusIndex', function handleFooChange(newValue, oldValue) {

      if (newValue < 0) {
        $scope.focusIndex = 0;
      } else if (newValue > $scope.allLogs.length - 1) {
        newValue = $scope.allLogs.length - 1;
      }
      $scope.openFile($scope.allLogs[newValue].name);

    })

    $scope.postEvaluation = function() {

      $http.post('/api/evaluation/', $scope.evaluation).then(function(data) {
        $scope.evaluation = data.data;
        $scope.logData.evaluation = data.data.id;
        
        $http.put('/api/processlog/' + $scope.logData.id + '/', $scope.logData).then(function (data) {
          $scope.logData = data.data;
        })
      });

    }

  }]);


app.controller('LogController',
  ['$scope', '$http', function ($scope, $http) {

    $scope.regionIsolated = true;

  }]);


app.directive('keytrap', function () {
  return function (scope, elem) {
    elem.bind('keydown keypress', function (event) {
      scope.$broadcast('keydown', {code: event.keyCode});
    });
  };
});