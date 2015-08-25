/**
 * Created by Arvind on 26/08/15.
 */

jQuery(document).ready(function($) {


    $('body').on('click', '[data-action="edit-cover-image"]', function (e) {
        e.stopPropagation();
        e.preventDefault();
        var model_id = $(this).attr('data-model-id');
        var aspect_ratio_x = $(this).attr('data-aspect-ratio-x');
        var aspect_ratio_y = $(this).attr('data-aspect-ratio-y');
        if (aspect_ratio_x == undefined || aspect_ratio_x.length == 0) {
            aspect_ratio_x = 16;
        } else {
            aspect_ratio_x = parseInt(aspect_ratio_x);
        }
        if (aspect_ratio_y == undefined || aspect_ratio_y.length == 0) {
            aspect_ratio_y = 9;
        } else {
            aspect_ratio_y = parseInt(aspect_ratio_y);
        }
        var model = $(this).attr('data-model');
        if (model == undefined || model.length == 0 || model_id == undefined || model_id.length == 0) {
            BootstrapDialog.alert('Something went wrong, please try again after refreshing the page.');
            return;
        }
        BootstrapDialog.show({
            title: 'Upload cover image',
            message: $('<div></div>').load('/cover-image-modal'),
            icon: 'glyphicon glyphicon-send',
            autospin: true,
            buttons: [
                {
                    id: "btn-close-dialog",
                    label: 'Close',
                    action: function (dialog) {
                        dialog.close();
                    }
                },
                {
                    id: "btn-upload-image",
                    label: 'Upload',
                    cssClass: 'btn-primary',
                    action: function (dialog) {
                        App.uploader(dialog, aspect_ratio_x / aspect_ratio_y);
                    }
                },
                {
                    id: "btn-crop-image",
                    label: 'Crop',
                    cssClass: 'btn-primary disabled',
                    action: function (dialog) {

                        var $image = $('.img-container > img')
                        if (!$image.data('cropper')) {
                            return;
                        }
                        var result = $image.cropper('getCroppedCanvas', {});
                        $('.cropped-image').html(result);
                        $('.img-container').hide();
                        $('.cropped-image').css('height', '100%');
                        $('.cropped-image').css('width', '100%');
                        $('.cropped-image').show();
                        $('#btn-save-image').addClass('disabled');

                        jQuery.ajax({
                            url: '/dialog/cropped_image',
                            data: {
                                url: $(".upload-image").val(),
                                img: $('.cropped-image > canvas')[0].toDataURL('image/jpeg')
                            },
                            type: 'POST',
                            success: function (data) {
                                console.log(data);
                                if (data.status == 'success') {
                                    $('#btn-save-image').removeClass('disabled');
                                    $('#btn-crop-image').addClass('disabled');
                                } else {
                                    $('.alert').html('<div class="alert-message">Failed to upload cropped image, try again later.</div>');
                                    $('.alert').addClass('alert-warning');
                                    $('.alert').show();
                                }
                            },
                            error: function (data) {
                                $('.alert').html('<div class="alert-message">Failed to upload cropped image, try again later.</div>');
                                $('.alert').addClass('alert-warning');
                                $('.alert').show();
                            }
                        });

                    }
                },
                {
                    id: "btn-save-image",
                    label: 'Save',
                    cssClass: 'btn-primary disabled',
                    action: function (dialog) {
                        var url = $('.upload-image').val();
                        App.base_editor.save_image_cover(model, model_id, url);
                    }
                }
            ]
        });
    });
});
