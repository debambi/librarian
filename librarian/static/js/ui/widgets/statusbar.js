// Generated by CoffeeScript 1.10.0
var extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

(function(window, $, templates) {
  var ExpandableBox, Statusbar, statusbarHbar;
  ExpandableBox = window.o.elements.ExpandableBox;
  statusbarHbar = $('.o-statusbar-hbar');
  statusbarHbar.append(templates.statusbarToggle);
  statusbarHbar.addClass('clickable');
  Statusbar = (function(superClass) {
    extend(Statusbar, superClass);

    function Statusbar(id) {
      this.id = id;
      Statusbar.__super__.constructor.call(this, this.id);
      this.activatorButton = this.findChild('hbar-activator');
      this.activatorButton.on('click', function(e) {
        return e.preventDefault();
      });
    }

    return Statusbar;

  })(ExpandableBox);
  return window["export"]('Statusbar', 'widgets', Statusbar);
})(this, this.jQuery, this.templates);