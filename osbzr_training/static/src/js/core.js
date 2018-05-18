odoo.define('osbzr_training.core',function(require) {
    "use strict";
    var core = require('web.core')
    var Widget = require('web.Widget')
    var MyHomepage = Widget.extend({
        template:'ebweb',
        init:function (parent,data) {
            return this._super.apply(this,arguments)
        },
        start:function(){
            return true;
        },
    });
    console.log('Hello my js');
    core.action_registry.add("ebweb",MyHomepage)
    console.log(core.action_registry);
});