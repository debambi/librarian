// Generated by CoffeeScript 1.10.0
(function(window, $) {
  var CHECK_INTERVAL, initPlugin, section, statusContainer, statusUrl, updateStatus;
  CHECK_INTERVAL = 3000;
  section = $('#dashboard-ondd');
  statusContainer = null;
  statusUrl = null;
  updateStatus = function() {
    return statusContainer.load(statusUrl);
  };
  initPlugin = function(e) {
    statusContainer = section.find('#signal-status');
    if (!statusContainer.length) {
      return;
    }
    statusUrl = statusContainer.data('url');
    return setInterval(updateStatus, CHECK_INTERVAL);
  };
  initPlugin();
  return section.on('dashboard-plugin-loaded', initPlugin);
})(this, this.jQuery);
