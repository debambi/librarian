// Generated by CoffeeScript 1.10.0
(function(window, $, templates) {
  var container, form, iframe, initPlugin, partialSelector, section, startMessage, startMessageId, uploadDone, uploadStart;
  partialSelector = "#firmware-update-container";
  container = $("#dashboard-firmware-panel");
  section = container.parents('.o-collapsible-section');
  startMessageId = '#firmwareUploadStart';
  startMessage = null;
  form = null;
  iframe = null;
  uploadStart = function(e) {
    var button;
    button = container.find('button');
    button.prop('disabled', true);
    container.prepend(startMessage);
    section.trigger('remax');
  };
  uploadDone = function(e) {
    var partial;
    partial = iframe.contents().find(partialSelector);
    container.html(partial);
    section.trigger('remax');
    return initPlugin();
  };
  initPlugin = function(e) {
    $(startMessageId).loadTemplate();
    startMessage = templates.firmwareUploadStart;
    form = container.find('form');
    form.on('submit', uploadStart);
    iframe = container.find('iframe');
    return iframe.on('load', uploadDone);
  };
  return section.on('dashboard-plugin-loaded', initPlugin);
})(this, this.jQuery, this.templates);
