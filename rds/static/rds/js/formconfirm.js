/*
 * form-confirm
 * Copyright (c) 2015 Jakob Aarøe Dam
 * Version 0.0.1
 * Licensed under the MIT license.
 */
(function($){
    "use strict";

    var template = '<div class="form-confirm-modal modal fade">\
  <div class="modal-dialog">\
    <div class="modal-content">\
\
      <div class="modal-header">\
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
        <h4 class="modal-title">Confirm Delete</h4>\
      </div>\
\
      <div class="modal-body">\
        <p>Deleting this package will also delete it from the RDS farms</p>\
      </div>\
\
      <div class="modal-footer">\
        <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>\
        <form class="confirm-form" method="POST" action="" style="display:inline-block">\
          <button type="submit" title="Delete" class="btn btn-danger">Confirm\
            <span class="glyphicon glyphicon-trash"></span></button>\</button>\
        </form>\
      </div>\
\
    </div><!-- /.modal-content -->\
  </div><!-- /.modal-dialog -->\
</div>';

    var FormConfirm = function(element, options){
        this.options = options;
        this.$form = $(element);
    };

    FormConfirm.prototype = {

        constructor: function() {
            this.$form.on('submit', $.proxy(this.submit, this));
        },

        modal: function(){
            this.$modal = $(template);

            var modal_form = this.$modal.find('.confirm-form');

            var form_action = this.$form.attr('action');
            modal_form.attr('action', form_action);

            var form_button = this.$form.find('button[type=submit]');

            this.$modal_title = this.$modal.find('.modal-title');
            this.$modal_body = this.$modal.find('.modal-body');

            this.$modal_body.text(this.$form.attr('data-confirm-body'));

            this.$modal_title.text(form_button.attr('title'));
            this.$modal.modal({});

            // maybe remove from DOM again
            // this.$modal.on('hide.bs.modal', function(){ 
            // });
        },

        submit: function(e) {
            e.preventDefault();
            this.modal();
        }

    };

    $.fn.formconfirm = function(options, value){
        return this.each(function(){
            var _options = $.extend({}, $.fn.formconfirm.defaults, options);
            var form_confirm = new FormConfirm(this, _options);
            form_confirm.constructor();
        });
    };

    $.fn.formconfirm.defaults = {
    };

})(window.jQuery);
