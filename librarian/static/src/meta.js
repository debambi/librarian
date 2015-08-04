/*jslint browser: true*/
(function ($) {
    'use strict';
    var metaContainer = $('.reader-meta'),
        metaButton = metaContainer.find('.toggle'),
        reader = $('.reader-frame');

    metaButton.on('click', function () {
        metaContainer.toggleClass('expanded');
        reader.toggleClass('reduced');
    });
}(this.jQuery));
