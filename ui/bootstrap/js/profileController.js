app.controller("ProfileController", function($scope, $modal, Tweets, Profile, Score, usSpinnerService){

	$scope.inHandle = "";
	$scope.tweets = {};
	$scope.profile = 0;
	$scope.score = "Score";
	$scope.reverse = true;
	$scope.start = new Date(946839278*1000);
	$scope.end = new Date();
	$scope.error = null;

	$scope.fetchProfile = function() {
		if ($scope.inHandle != null && $scope.inHandle != "") {
			$scope.error = null;
			usSpinnerService.spin('profileSpinner');
			Profile.get({id:$scope.inHandle}, function(response){
				console.log(response);
				usSpinnerService.stop('profileSpinner');
				
				if(response.message) {
					$scope.error = response.message;
				} else {

					$scope.profile = response;
					var image = $scope.profile.profile_image_url;
					$scope.profile.image_original = image.replace("_normal", "");
					$scope.profile.image_mini = image.replace("_normal", "_mini");
				}
			});
			Tweets.get({id:$scope.inHandle}, function(response){
				if(response.message) {
					$scope.error = response.message;
				} else {
					$scope.tweets = response.tweets;
					$scope.error = null;
				}
			});
		}
	}

	$scope.filter = function() {
		if ($scope.inHandle != null && $scope.inHandle != "") {
			
			usSpinnerService.spin('filterSpinner');
			

			var p = 0;
			if ($scope.picture == "yes") { p = 1;}
			if ($scope.picture == "no") { p = -1;}

			var s = 0;
			if ($scope.start != null) { s = parseInt($scope.start.getTime()/1000);}

			var e = 1434825584;
			if ($scope.end != null) { e = parseInt($scope.end.getTime()/1000);}

			var k = 'created_at';
			if ($scope.key != null) { k = $scope.key;}

			var r = 0;
			if ($scope.reverse != null) { r = $scope.reverse ? 1 : 0;}

			var f = {id:$scope.inHandle,
					photo:p,
					start:s,
					end:e,
					key:k,
					reverse:r
				     };
			console.log(f);

			Tweets.get(f, function(response){
				usSpinnerService.stop('filterSpinner');
				if(response.message) {
					$scope.error = response.message;
				} else {
					$scope.tweets = response.tweets;
					$scope.error = null;
				}
			});
		}
	}

	$scope.fetchScore = function() {


		if ($scope.inHandle != null && $scope.inHandle != "") {
			if ($scope.score != "...") {
				$scope.score = "...";
				usSpinnerService.spin('scoreSpinner');

				Score.get({id:$scope.inHandle}, function(response){
					usSpinnerService.stop('scoreSpinner');
					if(response.message) {
						$scope.error = response.message;
						$scope.score = "Score";
					} else {
						$scope.score = response.score;
						$scope.error = null;
					}
				});
			}
		}
	}
	
	$scope.sortOrder = function() {
		$scope.reverse = !$scope.reverse;
	}

	$scope.timeRange = function () {

		if ($scope.inHandle != null && $scope.inHandle != "") {
		    var modalInstance = $modal.open({
			    templateUrl: 'timeRange.html',
			    controller: 'ModalInstanceCtrl',
			    size: 'lg',
			    resolve: {
					      range: function () {
						      return {start:$scope.start, end:$scope.end};
					      }
				      }
			    });
	
		    modalInstance.result.then(function (selectedItem) {
			    $scope.start = selectedItem.start;
			    $scope.end = selectedItem.end;
			}, function () {});
		}
	
		
	};
});


app.directive('tweet', function () {
	return {
	    restrict: "E",
		transclude: true,
		scope: {
		tweet: "=currentTweet"
		    },
		template: '<div ng-transclude id="{{tweet.id}}" class="well"></div>',
		replace: true
	}
});

app.factory('Tweets', function ($resource) {
	//return $resource('http://repcheckr.net:5000/tweets/:id');
	return $resource('http://127.0.0.1:5000/tweets/:id');
});

app.factory('Profile', function ($resource) {
	//return $resource('http://repcheckr.net:5000/profile/:id');
	return $resource('http://127.0.0.1:5000/profile/:id');
});

app.factory('Score', function ($resource) {
	//return $resource('http://repcheckr.net:5000/score/:id');
	return $resource('http://127.0.0.1:5000/score/:id');
});

app.filter('epoch', function () {
  return function (utc) {
  	      var ms = new Date(utc);
	      return  ms.getTime();
        };
});




app.controller('ModalInstanceCtrl', function ($scope, $modalInstance, range) {
	
	$scope.start = range.start;
	$scope.end = range.end;


	$scope.ok = function () {
	    $modalInstance.close({start:$scope.start, end:$scope.end});
	};

	$scope.cancel = function () {
	    $modalInstance.dismiss('cancel');
	};

	$scope.openStart = function($event) {
		    $event.preventDefault();
		    $event.stopPropagation();

		    $scope.openedStart = true;
      	};

	$scope.openEnd = function($event) {
		    $event.preventDefault();
		    $event.stopPropagation();

		    $scope.openedEnd = true;
      	};
});
