app.controller("ProfileController", function($scope, Tweets, Profile){

	$scope.inHandle = "";
	$scope.tweets = {};
	$scope.profile = 0;

	$scope.fetchProfile = function() {
		if ($scope.inHandle != null && $scope.inHandle != "") {
			// TODO Validate user
			Tweets.get({id:$scope.inHandle}, function(response){
				$scope.tweets = response.tweets;
			});
			Profile.get({id:$scope.inHandle}, function(response){
				$scope.profile = response;
				var image = $scope.profile.profile_image_url;
				$scope.profile.image_original = image.replace("_normal", "");
				$scope.profile.image_mini = image.replace("_normal", "_mini");
			});
		}
	}

	$scope.fetchScore = function() {

		/* TODO replace place holder with rest end point for score

		if ($scope.inHandle != null && $scope.inHandle != "") {
			Score.get({id:$scope.inHandle}, function(response){
				$scope.score = response;
			});
		}
		*/
	}

		
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
	return $resource('http://repcheckr.net:5000/tweets/:id');
	//return $resource('http://127.0.0.1:5000/tweets/:id');
});

app.factory('Profile', function ($resource) {
	return $resource('http://repcheckr.net:5000/profile/:id');
	//return $resource('http://127.0.0.1:5000/profile/:id');
});

app.factory('Score', function ($resource) {
	//return $resource('http://repcheckr.net:5000/score/:id');
	//return $resource('http://127.0.0.1:5000/score/:id');
});

app.filter('epoch', function () {
  return function (utc) {
  	      var ms = new Date(utc);
	      return  ms.getTime();
        };
});
