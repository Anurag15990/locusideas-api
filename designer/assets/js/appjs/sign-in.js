
var modalInstance;
var app = angular.module('app', ['ngRoute', 'ui.bootstrap']);
app.controller('loginCtrl', function($scope, $http){
    $scope.login = function(){
       var email = $scope.username;
       var password = $scope.password;
        var url = '/login';
        var data = {
            email: email,
            password: password
        };

        $http.post(url, data).
            then(function(response) {
                console.log(response);
                var data = response['data']
                var user = data['node']
                window.location = user['slug']
            }, function(response) {
                console.log(response);
        });
    };

});

app.controller('registerCtrl', function($scope, $http){
   $scope.register = function() {
       var name = $scope.name;
       var email = $scope.username;
       var password = $scope.password;
       var confirm = $scope.confirmPassword;
       var url = '/editors/invoke'
       var message = {
           type : 'user',
           command : 'register',
           data : {
               name : name,
               email : email,
               password : password,
               confirm : confirm,
               roles : ['Basic User']
           }
       };
        if (name != null && email != null && password != null && confirm != null) {
            $http.post(url, message).
                then(function (response) {
                    console.log(response);
                    var data = response['data']
                    var user = data['node']
                    window.location = user['slug']
                }, function (error) {
                    console.log(error);
                });
        }
   };
});

app.controller('profileCtrl', function ($scope, $document, $modal , $http) {

    $scope.edit_contact_info = function() {
        var phone = $('.phone-display').text().replace(/\s/g, '');
        var mobile = $('.mobile-display').text().replace(/\s/g, '');
        var address = $('.address-display').text();

        console.log(address);

        $(".details-info").addClass('hidden');
        $(".details-info-edit").removeClass('hidden');
        $(".phone-number-edit").val(phone);
        $(".mobile-number-edit").val(mobile);
        $(".address-edit").text(address.trim());

    };

    $scope.upload_image = function () {
        modalInstance = $modal.open({
            templateUrl : '/upload_image',
            controller : 'ImageCtrl',
            size: 'lg'
        })
    };

    $scope.cancel_update_contact = function () {
        console.log('Reached Cancel');
        $(".details-info-edit").addClass('hidden');
        $(".details-info").removeClass('hidden');
    };

    $scope.update_contact_info = function () {
        console.log('Reached Update');
        var message = {
            node : $('.profile-id').val(),
            type : 'user',
            command : 'update-contact-info',
            data : {
                address : $scope.address,
                phone : $scope.phone,
                mobile : $scope.mobile
            }
        };
        console.log(message);
        var url = '/editors/invoke';
        $http.post(url, message).
            then(function (response) {
                console.log(response);
                var data = response['data']
                var user = data['node']
                window.location = user['slug']
            }, function (error) {
                console.log(error);
            });
    }


    $scope.edit_education = function () {
        $('.education-info').addClass('hidden');
        $('.education-info-edit').removeClass('hidden');
    };

    $scope.cancel_education_edit = function () {
        $('.education-info-edit').addClass('hidden');
        $('.education-info').removeClass('hidden');
    };

    $scope.add_education_row = function() {
        console.log('Reached Add Education Row');
        $('.education-rows-section').append("<div class='row'><div class='col-lg-4 col-md-4 col-sm-4 col-xs-12 m-10 ml-40 h-25 p-10'><input class='form-control education-field' value=''></div></div>");
    };

    $scope.update_education_info = function () {
        var education_array = [];
        $('.education-field').each(function (index) {
            education_array.push($(this).val());
        });

        console.log(education_array);

        var message = {
            node : $('.profile-id').val(),
            type : 'user',
            command : 'update-institution',
            data : {
                institution : education_array
            }
        };
        var url = '/editors/invoke';
        $http.post(url, message).
            then(function (response) {
                console.log(response);
                var data = response['data'];
                var user = data['node'];
                window.location = user['slug'];
            }, function (error) {
                console.log(error);
            });
    };


    $scope.edit_experience = function () {
        $('.experience-info').addClass('hidden');
        $('.experience-info-edit').removeClass('hidden');
    };

    $scope.cancel_experience_edit = function () {
        $('.experience-info-edit').addClass('hidden');
        $('.experience-info').removeClass('hidden');
    };

    $scope.add_experience_row = function() {
        console.log('Reached Add Experience Row');
        $('.experience-rows-section').append("<div class='row'><div class='col-lg-4 col-md-4 col-sm-4 col-xs-12 m-10 ml-40 h-25 p-10'><input class='form-control experience-field' value=''></div></div>");
    };

    $scope.update_experience_info = function () {
        var experience_array = [];
        $('.experience-field').each(function (index) {
            experience_array.push($(this).val());
        });

        console.log(experience_array);

        var message = {
            node : $('.profile-id').val(),
            type : 'user',
            command : 'update-experience',
            data : {
                experience : experience_array
            }
        };
        var url = '/editors/invoke';
        $http.post(url, message).
            then(function (response) {
                console.log(response);
                var data = response['data'];
                var user = data['node'];
                window.location = user['slug'];
            }, function (error) {
                console.log(error);
            });
    };

    $scope.edit_about_info = function () {

        var bio = $('.bio-display').text();
        var proficiency = $('.proficiency-display').text();

        console.log(bio);
        console.log(proficiency);

        $('.about-info').addClass('hidden');
        $('.about-info-edit').removeClass('hidden');

        $('.bio-edit').val(bio.trim());
        $('.proficiency-edit').val(proficiency.trim());
    };

    $scope.cancel_about_edit = function () {
        $('.about-info-edit').addClass('hidden');
        $('.about-info').removeClass('hidden');
    };

    $('.work-focus-tags-list').on('click', '.focus-tags', function(e){
        e.preventDefault();
        e.stopPropagation();
        $(e.target).remove();
    });

    $('.work-focus-add-row').keypress(function(e){
        var code = (e.keyCode ? e.keyCode : e.which);
        if(code == 13 || code == 188) { //Enter keycode
            var tag = $('.work-focus-add-row').val();
            $(".work-focus-tags-list").append('<a class="focus-tags" data-tag="'+tag+'">'+tag+'&nbsp;|&nbsp;X</a>');
            $('.work-focus-add-row').val('');
            e.preventDefault();
            e.stopPropagation();
        }
    });

    $('.work-style-tags-list').on('click', '.style-tags', function(e){
        e.preventDefault();
        e.stopPropagation();
        $(e.target).remove();
    });

    $('.work-style-add-row').keypress(function(e){
        var code = (e.keyCode ? e.keyCode : e.which);
        if(code == 13 || code == 188) { //Enter keycode
            var tag = $('.work-style-add-row').val();
            $(".work-style-tags-list").append('<a class="style-tags" data-tag="'+tag+'">'+tag+'&nbsp;|&nbsp;X</a>');
            $('.work-style-add-row').val('');
            e.preventDefault();
            e.stopPropagation();
        }
    });

    $('.work-interests-tags-list').on('click', '.interests-tags', function(e){
        e.preventDefault();
        e.stopPropagation();
        $(e.target).remove();
    });

    $('.work-interests-add-row').keypress(function(e){
        var code = (e.keyCode ? e.keyCode : e.which);
        if(code == 13 || code == 188) { //Enter keycode
            var tag = $('.work-interests-add-row').val();
            $(".work-interests-tags-list").append('<a class="interests-tags" data-tag="'+tag+'">'+tag+'&nbsp;|&nbsp;X</a>');
            $('.work-interests-add-row').val('');
            e.preventDefault();
            e.stopPropagation();
        }
    });

    $scope.update_about_info = function () {

        var work_focus = [];
        var work_styles = [];
        var work_interests = [];

        var bio = $scope.bio;
        var proficiency = $scope.proficiency;

        $('.focus-tags').each(function (index) {
            work_focus.push($(this).attr('data-tag'));
        });

        $('.style-tags').each(function (index) {
            work_styles.push($(this).attr('data-tag'));
        });

        $('.interests-tags').each(function (index) {
            work_interests.push($(this).attr('data-tag'));
        });

        var url = '/editors/invoke';
        var message = {
            node : $('.profile-id').val(),
            type : 'user',
            command : 'update-about-info',
            data : {
                bio : bio,
                proficiency : proficiency,
                work_focus : work_focus,
                work_style : work_styles,
                work_interest : work_interests
            }
        };

        $http.post(url, message).
            then(function (response) {
                console.log(response);
                var data = response['data'];
                var user = data['node'];
                window.location = user['slug'];
            }, function (error) {
                console.log(error);
        });
    };

});


app.controller('ImageCtrl', function($scope, $http){

    var imageNode = null;

    $scope.close_modal = function () {
        console.log('Reached Close Modal');
        modalInstance.close();
    };

    $scope.upload_user_profile_image = function (image) {
        var image = image;
        var image_name = image.name;

        var url = '/editors/invoke';

        var node = $('.data-model-id').val();

        console.log(image);
        console.log(image.name);

        var base64String = image.dataURL.replace('data:image/jpeg;base64,', '');
        base64String = base64String.replace('data:image/png;base64,', '');

        var message = {
            node : node,
            type : 'photo',
            command : 'upload-user-image',
            data : {
                image: image.dataURL.replace('data:image/jpeg;base64,', '').replace('data:image/png;base64', '')
            }
        };

        console.log(message);

        $http.post(url, message).then(function (response) {
            console.log(response);
            var data = response['data'];
            console.log(data);
            var image = data['node'];
            var id = image['_id'];
            imageNode = id['$oid'];

            var message2 = {
                node : node,
                type : 'user',
                command : 'update-profile-photo',
                data : {
                    profile_photo : imageNode
                }
            };

            console.log(message2);

            $http.post(url, message2).then(function (response) {
                console.log(response);
                var data = response['data'];
                var user = data['node'];
                modalInstance.close();
                window.location = user['slug'];
            }, function (error) {
                console.log(error);
            });

        }, function (error) {
            console.log(error);
        });
    };
});

app.directive('image', function($q) {
        'use strict'

        var URL = window.URL || window.webkitURL;

        var getResizeArea = function () {
            var resizeAreaId = 'fileupload-resize-area';

            var resizeArea = document.getElementById(resizeAreaId);

            if (!resizeArea) {
                resizeArea = document.createElement('canvas');
                resizeArea.id = resizeAreaId;
                resizeArea.style.visibility = 'hidden';
                document.body.appendChild(resizeArea);
            }

            return resizeArea;
        };


        var resizeImage = function (origImage, options) {
            var maxHeight = options.resizeMaxHeight || 300;
            var maxWidth = options.resizeMaxWidth || 250;
            var quality = options.resizeQuality || 0.7;
            var type = options.resizeType || 'image/jpg';

            var canvas = getResizeArea();

            var height = origImage.height;
            var width = origImage.width;

            // calculate the width and height, constraining the proportions
            if (width > height) {
                if (width > maxWidth) {
                    height = Math.round(height *= maxWidth / width);
                    width = maxWidth;
                }
            } else {
                if (height > maxHeight) {
                    width = Math.round(width *= maxHeight / height);
                    height = maxHeight;
                }
            }

            canvas.width = width;
            canvas.height = height;

            //draw image on canvas
            var ctx = canvas.getContext("2d");
            ctx.drawImage(origImage, 0, 0, width, height);

            // get the data from canvas as 70% jpg (or specified type).
            return canvas.toDataURL(type, quality);
        };

        var createImage = function(url, callback) {
            var image = new Image();
            image.onload = function() {
                callback(image);
            };
            image.src = url;
        };

        var fileToDataURL = function (file) {
            var deferred = $q.defer();
            var reader = new FileReader();
            reader.onload = function (e) {
                deferred.resolve(e.target.result);
            };
            reader.readAsDataURL(file);
            return deferred.promise;
        };


        return {
            restrict: 'A',
            scope: {
                image: '=',
                resizeMaxHeight: '@?',
                resizeMaxWidth: '@?',
                resizeQuality: '@?',
                resizeType: '@?'
            },
            link: function postLink(scope, element, attrs, ctrl) {

                var doResizing = function(imageResult, callback) {
                    createImage(imageResult.url, function(image) {
                        var dataURL = resizeImage(image, scope);
                        imageResult.resized = {
                            dataURL: dataURL,
                            type: dataURL.match(/:(.+\/.+);/)[1]
                        };
                        callback(imageResult);
                    });
                };

                var applyScope = function(imageResult) {
                    scope.$apply(function() {
                        //console.log(imageResult);
                        if(attrs.multiple)
                            scope.image.push(imageResult);
                        else
                            scope.image = imageResult;
                    });
                };


                element.bind('change', function (evt) {
                    //when multiple always return an array of images
                    if(attrs.multiple)
                        scope.image = [];

                    var files = evt.target.files;
                    for(var i = 0; i < files.length; i++) {
                        //create a result object for each file in files
                        var imageResult = {
                            file: files[i],
                            url: URL.createObjectURL(files[i])
                        };

                        fileToDataURL(files[i]).then(function (dataURL) {
                            imageResult.dataURL = dataURL;
                        });

                        if(scope.resizeMaxHeight || scope.resizeMaxWidth) { //resize image
                            doResizing(imageResult, function(imageResult) {
                                applyScope(imageResult);
                            });
                        }
                        else { //no resizing
                            applyScope(imageResult);
                        }
                    }
                });
            }
        };
    });

