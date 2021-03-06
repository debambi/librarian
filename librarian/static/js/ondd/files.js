// Generated by CoffeeScript 1.10.0
(function(window, $, templates) {
  var BUNDLE_EXT, initPlugin, reProgress, roundedPercentage, section, templateIds, transfersOSD, truncateName;
  BUNDLE_EXT = ".bundle";
  section = $('#dashboard-ondd');
  templateIds = ['onddTransferTemplate', 'onddUnknownTransfer', 'onddNoTransfersTemplate'];
  reProgress = new RegExp('\{progress\}', 'g');
  roundedPercentage = function(src) {
    var rounded;
    rounded = Math.floor(src / 5) * 5;
    return Math.min(Math.max(rounded, 0), 100);
  };
  truncateName = function(name, maxSize, separator) {
    var bExtIdx, firstLen, secondLen, usableChars;
    if (maxSize == null) {
      maxSize = 50;
    }
    if (separator == null) {
      separator = '...';
    }
    bExtIdx = name.indexOf(BUNDLE_EXT);
    if (bExtIdx === name.length - BUNDLE_EXT.length) {
      name = name.substring(0, bExtIdx);
    }
    if (name.length <= maxSize) {
      return name;
    }
    usableChars = maxSize - separator.length;
    firstLen = Math.ceil(usableChars / 2);
    secondLen = Math.floor(usableChars / 2);
    if (usableChars % 2 !== 0) {
      secondLen += 1;
    }
    return name.substring(0, firstLen) + separator + name.substring(name.length - secondLen, name.length);
  };
  transfersOSD = function(data) {
    var filename, html, i, info, len, ref, transfer;
    if (data.transfers.length === 0) {
      return templates.onddNoTransfersTemplate;
    }
    html = '';
    ref = data.transfers;
    for (i = 0, len = ref.length; i < len; i++) {
      transfer = ref[i];
      if (!transfer.filename) {
        info = templates.onddUnknownTransfer;
      } else {
        filename = truncateName(transfer.filename);
        info = filename + " (" + transfer.percentage + "%)";
      }
      html += templates.onddTransferTemplate.replace('{transfer-info}', info).replace('{percentage}', transfer.percentage).replace('{progress}', roundedPercentage(transfer.percentage));
    }
    html = "<ul>" + html + "</ul>";
    return html;
  };
  initPlugin = function(e) {
    var i, len, provider, tmplId;
    for (i = 0, len = templateIds.length; i < len; i++) {
      tmplId = templateIds[i];
      $("#" + tmplId).loadTemplate();
    }
    provider = window.state.provider('ondd');
    return provider.postprocessor(transfersOSD, ['transfersOSD']);
  };
  return section.on('dashboard-plugin-loaded', initPlugin);
})(this, this.jQuery, this.templates);
