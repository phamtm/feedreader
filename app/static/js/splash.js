// Module for the demo
angular.module('splashDemo', ['ui.splash'])
.controller('MainCtrl', ['$splash', function ($splash) {
  this.openSplash = function () {
    $splash.open({
      title: 'Hi there!',
      message: "This sure is a fine modal, isn't it?"
    });
  };
}]);

// Re-usable $splash module
angular.module('ui.splash', ['ui.bootstrap'])
.service('$splash', [
  '$modal',
  '$rootScope',
  function($modal, $rootScope) {
    return {
      open: function (attrs, opts) {
        var scope = $rootScope.$new();
        angular.extend(scope, attrs);
        opts = angular.extend(opts || {}, {
          backdrop: false,
          scope: scope,
          templateUrl: 'splash/content.html',
          windowTemplateUrl: 'splash/index.html'
        });
        return $modal.open(opts);
      }
    };
  }
])
.run([
  '$templateCache',
  function ($templateCache) {
    $templateCache.put('splash/index.html',
      '<section class="splash" ng-class="{\'splash-open\': animate}" ng-style="{\'z-index\': 1000, display: \'block\'}" ng-click="close($event)">' +
      '  <div class="splash-inner" ng-transclude></div>' +
      '</section>'
    );
    // $templateCache.put('splash/content.html',
    //   '<div class="splash-content text-center">' +
    //   '  <h1 ng-bind="title"></h1>' +
    //   '  <p class="lead" ng-bind="message"></p>' +
    //   '  <button class="btn btn-lg btn-outline" ng-bind="btnText || \'Ok, cool\'" ng-click="$close()"></button>' +
    //   '</div>'
    // );
    $templateCache.put('splash/content.html',
      '<div class="text-center">'+
      '<iframe style="margin:8px 10% 0 10%" width="80%" height="95%" src="http://kenh14.vn/musik/bnhv-nhi-liveshow-4-son-tung-m-tp-nhi-chi-thich-bat-nguoi-dep-20140919091742733.chn" frameborder="0"></iframe>'+
      '<span style="color:white">http://kenh14.vn/musik/bnhv-nhi-liveshow-4-son-tung-m-tp-nhi-chi-thich-bat-nguoi-dep-20140919091742733.chn</span>'+
      '</div>'
    );
  }
]);