// toc js
$(function () {
    $('.content').toc({
        minItemsToShowToc: 0,
        renderIn: '#renderIn',
        contentsText: "Table of Content",
        hideText: 'Collapse',
        showText: 'Expand',
        showCollapsed: true
    });
});