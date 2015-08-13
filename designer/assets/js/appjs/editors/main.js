/**
 *
 * Created by anurag on 13/08/15.
 */

jQuery(document).ready(function($){

    var App = App || {};

    App.editor = function (options) {

        var callback = null;
        if (arguments.length > 1) {
            callback = arguments[1];
        }
        $('#loadingImage').show()
        $.ajax({
            type : 'POST',
            url : '/editors/invoke',
            data : JSON.stringify(options),
            success : function(data) {
                $('#loadingImage').hide()
                if (data.status=='error' && data.message=='Please login before making requests') {
                       App.show_login();
                }
                console.log(data);
                if (callback != null) {
                    callback(data)
                } else {
                    setTimeout(function () {
                       window.location.reload();
                    }, 1000);
                }
            },
            error : function (data) {
                $('#loadingImage').hide()
            },
            contentType : 'application/json',
            dataType : 'json'
        });
    };

    window.App = App
});