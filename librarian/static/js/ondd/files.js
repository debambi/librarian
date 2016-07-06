// Generated by CoffeeScript 1.10.0
(function(window, $) {
  var CHECK_INTERVAL, filesContainer, filesUrl, initPlugin, section, updateFileList;
  CHECK_INTERVAL = 3000;
  section = $('#dashboard-ondd');
  filesContainer = null;
  filesUrl = null;
  updateFileList = function() {
    filesContainer.load(filesUrl);
    return section.trigger('remax');
  };
  initPlugin = function(e) {
    setInterval(updateFileList, CHECK_INTERVAL);
    filesContainer = section.find('#ondd-file-list');
    return filesUrl = filesContainer.data('url');
  };
  return section.on('dashboard-plugin-loaded', initPlugin);
})(this, this.jQuery);
