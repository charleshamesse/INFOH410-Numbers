var app = angular.module('Numbers', ['ngSanitize','chart.js'])
    .config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    })
    .controller('MainController', function ($scope, $http,$timeout) {
        $scope.test = "mmmh";
        // Train
        $scope.train = function () {
            $http({
                method: 'GET',
                url: 'nn/train'
            }).then(function successCallback(response) {
                $scope.response = response;
            }, function errorCallback(response) {
                $scope.response = "Error: " + response;
            });
        };

        $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
        $scope.series = ['Series A', 'Series B'];
        $scope.data = [
        [65, 59, 80, 81, 56, 55, 40],
        [28, 48, 40, 19, 86, 27, 90]
        ];
        $scope.onClick = function (points, evt) {
            console.log(points, evt);
        };

        // Test
        $scope.test = function () {
            var canvas = angular.element( document.querySelector( '#n-canvas' ) ).get(0);
            var ctx = canvas.getContext('2d');
            var yolo = ctx.getImageData(0,0,280,280);
            var img = []
            for(i=3;i<yolo.data.length;i+=4){
                img.push(yolo.data[i]);
            }
            var imageArray = JSON.stringify({"img":img});
            $http.post('nn/recognize',imageArray).
                success(function(data, status, headers, config) {
                    console.log(data);
                }).
                error(function(data, status, headers, config) {
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                  });
        };

        // Utils
        $scope.clear = function() {
            var canvas = angular.element( document.querySelector( '#n-canvas' ) ).get(0);
            var ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

    })
    .directive("drawing", function () {
        return {
            restrict: "A",
            link: function (scope, element) {
                var ctx = element[0].getContext('2d');

                // variable that decides if something should be drawn on mousemove
                var drawing = false;

                // the last coordinates before the current move
                var lastX;
                var lastY;

                element.bind('mousedown', function (event) {
                    if (event.offsetX !== undefined) {
                        lastX = event.offsetX;
                        lastY = event.offsetY;
                    } else { // Firefox compatibility
                        lastX = event.layerX - event.currentTarget.offsetLeft;
                        lastY = event.layerY - event.currentTarget.offsetTop;
                    }

                    // begins new line
                    ctx.beginPath();

                    drawing = true;
                });
                element.bind('mousemove', function (event) {
                    if (drawing) {
                        // get current mouse position
                        if (event.offsetX !== undefined) {
                            currentX = event.offsetX;
                            currentY = event.offsetY;
                        } else {
                            currentX = event.layerX - event.currentTarget.offsetLeft;
                            currentY = event.layerY - event.currentTarget.offsetTop;
                        }

                        draw(lastX, lastY, currentX, currentY);

                        // set current coordinates to last one
                        lastX = currentX;
                        lastY = currentY;
                    }

                });
                element.bind('mouseup', function (event) {
                    // stop drawing
                    drawing = false;
                });

                // canvas reset
                function reset() {
                    element[0].width = element[0].width;
                }

                function draw(lX, lY, cX, cY) {
                    // line from
                    ctx.moveTo(lX, lY);
                    // to
                    ctx.lineTo(cX, cY);
                    // style
                    ctx.strokeStyle = "rgb(0, 140, 186)";
                    ctx.lineWidth=10;
                    // draw it
                    ctx.stroke();
                }
            }
        };
    });
;
