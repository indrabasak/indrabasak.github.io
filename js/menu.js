(function ($) {
    'use strict';

    var body = $('body'),
        _window = $(window);

    /**
     * Enables menu toggle for small screens.
     */
    (function () {
        var nav = $('#site-navigation'), button, menu;
        if (!nav) {
            return;
        }

        button = nav.find('.menu-toggle');
        if (!button) {
            return;
        }

        // Hide button if menu is missing or empty.
        menu = nav.find('.nav-menu');
        console.log('menu.children().length = ' + menu.children().length);
        if (!menu || !menu.children().length) {
            button.hide();
            return;
        }

        $('.menu-toggle').on('click.suits', function () {
            nav.toggleClass('toggled-on');
            button.toggleClass('expanded');
        });
    })();
})(window.jQuery);