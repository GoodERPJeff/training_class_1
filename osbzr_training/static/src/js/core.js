odoo.define('osbzr_training.core',function(require) {
    "use strict";
    var core = require('web.core')
    var Widget = require('web.Widget')
    var MyHomepage = Widget.extend({
        templatet:'ebweb',
        init:function (parent,data) {
            return this._super.apply(this,arguments)
        },
        start:function(){
            return true;
        },
    });
    core.action_registry.add("ebweb",MyHomepage)
});