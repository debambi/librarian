// Generated by CoffeeScript 1.10.0
var extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

(function(window, $) {
  var ExpandableBox, PulldownMenubar;
  ExpandableBox = window.o.elements.ExpandableBox;
  PulldownMenubar = (function(superClass) {
    extend(PulldownMenubar, superClass);

    function PulldownMenubar(id) {
      this.id = id;
      PulldownMenubar.__super__.constructor.call(this, this.id);
      this.menu = this.findChild('menu');
      this.firstNav = this.menu.find("[role=\"menuitem\"]").first();
    }

    PulldownMenubar.prototype.elementClass = 'pulldown-menubar';

    PulldownMenubar.prototype.onOpen = function() {
      return this.firstNav.focus();
    };

    return PulldownMenubar;

  })(ExpandableBox);
  return window["export"]('PulldownMenubar', 'widgets', PulldownMenubar);
})(this, this.jQuery);
