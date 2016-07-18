// Generated by CoffeeScript 1.10.0
(function(window, $, templates) {
  'use strict';
  var DOWN, UP, body, mainPanel, modalDialogTemplate, spinnerIcon;
  UP = 38;
  DOWN = 40;
  body = $(document.body);
  mainPanel = $("#" + window.o.pageVars.mainPanelId);
  modalDialogTemplate = window.templates.modalDialogCancelOnly;
  spinnerIcon = window.templates.spinnerIcon;
  mainPanel.on('keydown', '.file-list-link', function(e) {
    var elem, listItem;
    elem = $(this);
    listItem = elem.parents('.file-list-item');
    switch (e.which) {
      case UP:
        listItem.prev().find('a').focus();
        e.preventDefault();
        break;
      case DOWN:
        listItem.next().find('a').focus();
        e.preventDefault();
    }
  });
  mainPanel.on('click', '.file-list-link', function(e) {
    var elem, icon, isDir, originalIcon, res, spinner, url;
    elem = $(this);
    isDir = elem.data('type') === 'directory';
    if (elem.data('type') === 'directory') {
      e.preventDefault();
      e.stopPropagation();
      icon = elem.find('.file-list-icon');
      url = elem.attr('href');
      originalIcon = icon.html();
      spinner = $(spinnerIcon);
      icon.html(spinner);
      res = loadContent(url);
      res.done(function() {
        window.history.pushState(null, null, url);
        return setPath(elem.data('relpath'));
      });
      res.always(function() {
        return icon.html(originalIcon);
      });
    }
  });
})(this, this.jQuery, this.templates);
