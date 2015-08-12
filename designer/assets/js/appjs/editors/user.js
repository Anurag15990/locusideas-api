/**
 *
 * Created by anurag on 12/08/15.
 */

$(document).ready(function () {
    console.log('user-editor.js');
    var App = window.App || {}
    App.user = App.user || {}

    App.user.update_bio = function(node, bio, callback) {
        var options = {
            node : node,
            type : 'user',
            command : 'update-bio',
            data : {
                bio : bio
            }

        };
        App.editor(options, callback);
    };

    App.user.edit_role = function (node, role, action, callback) {
        var options = {
            node : node,
            type : 'user',
            command : 'edit-role',
            action : action,
            data : {
                role : role
            }
        };
        App.editor(options, callback);
    };

    App.user.update_institution = function (node, institution, callback) {
        var options = {
            node : node,
            type : 'user',
            command : 'update-institution',
            data : {
                institution : institution
            }
        };
        App.editor(options, callback);
    };

    App.user.update_experience = function (node, experience, callback) {
        var options = {
            node : node,
            type : 'user',
            command : 'update-experience',
            data : {
                experience : experience
            }
        };
        App.editor(options, callback);
    };

    App.user.change_password = function (node, password, confirm, callback) {
        var options = {
            node : node,
            type : 'user',
            command : 'change-password',
            data : {
                password : password,
                confirm : confirm
            }
        };
        App.editor(options, callback);
    };

    App.user.login = function (email, password, callback) {
        var options = {
            type : 'user',
            command : 'login',
            data : {
                email : email,
                password : password
            }
        };
        App.editor(options, callback);
    };

    App.user.logout = function (callback) {
        var options = {
            type : 'user',
            command : 'logout'
        };
        App.editor(options , callback)
    };

    App.user.update_contact_info = function (node, address, mobile, phone, callback) {
        var options = {
            type : 'user',
            command : 'update-contact-info',
            data : {
                address : address,
                mobile : mobile,
                phone : phone
            }
        };
        App.editor(options, callback)
    };
})  