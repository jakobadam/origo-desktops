/*
 * bootstrap-fileprogress
 * Copyright (c) 2015 Jakob Aarøe Dam
 * Version 0.0.1
 * Licensed under the MIT license.
 */
(function($){
    "use strict";

     var template = '<div class="modal fade" id="file-progress-modal">\
  <div class="modal-dialog">\
    <div class="modal-content">\
      <div class="modal-header">\
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
        <h4 class="modal-title">Uploading</h4>\
      </div>\
      <div class="modal-body">\
        <div class="modal-message"></div>\
        <div class="progress">\
          <div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0"\
               aria-valuemax="100" style="width: 0%;min-width: 2em;">\
            0%\
          </div>\
        </div>\
      </div>\
      <div class="modal-footer" style="display:none">\
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
      </div>\
    </div><!-- /.modal-content -->\
  </div><!-- /.modal-dialog -->\
</div><!-- /.modal -->';

    var FileProgress = function(element, options){
        this.options = options;
        this.$element = $(element);
    };

    FileProgress.prototype = {

        constructor: function() {
            this.$form = this.$element.parents('form');
            this.$form.on('submit', $.proxy(this.submit, this));

            $('body').append(template);
            this.$modal = $('#file-progress-modal');
            this.$modal_message = $('.modal-message');
            this.$modal_title = $('.modal-title');
            this.$modal_footer = $('.modal-footer');
            this.$modal_bar = $('.progress-bar');

            this.$modal.on('hidden.bs.modal', $.proxy(this.reset, this));
        },

        reset: function(){
            console.log('reset');
            this.$modal_title = $('.modal-title').text('Uploading');
            this.$modal_footer.hide();
            this.$modal_bar.addClass('progress-bar-success');
            this.$modal_bar.removeClass('progress-bar-danger');
        },

        submit: function(e) {
            var form = this.$form;
            e.preventDefault();

            this.$modal.modal({
                backdrop: 'static',
                keyboard: false
            });

            var data = new FormData(form.get(0));
            var xhr = $.ajax(window.location.href, {
                data: data,
                contentType: false,
                processData: false,
                success: $.proxy(this.success, this),
                error: $.proxy(this.error, this),
                type: form.attr('method')
            });

            // var xhr = new XMLHttpRequest();
            // xhr.open(form.attr('method'), window.location.href);
            // xhr.send(data);

            $.proxy(xhr.progress, this.progress);
        },

        success: function(data, status, xhr) {
            debugger;
        },

        error: function(xhr, status, error){
            this.$modal_title.text('Upload failed');

            this.$modal_bar.removeClass('progress-bar-success');
            this.$modal_bar.addClass('progress-bar-danger');
            this.$modal_footer.show();

            var h = $.parseHTML(xhr.responseText);
            var new_form = $(h).find('form');

            //this.constructor();

            new_form.find(':file').filestyle({buttonBefore: true});
            this.$form.html(new_form.children());
            //this.$form.html($('<p>wii</p>'));
        },

        progress: function(/*ProgressEvent*/e){
            var percent = Math.round((e.loaded / e.total) * 100);
            this.$modal_bar.attr('aria-valuenow', percent);
            this.$modal_bar.text(percent + '%');
            this.$modal_bar.css('width', percent + '%');
        }

    };

    $.fn.fileprogress = function(options, value){
        return this.each(function(){
            var _options = $.extend({}, $.fn.fileprogress.defaults, options);
            var file_progress = new FileProgress(this, _options);
            file_progress.constructor();
        });
    };

    $.fn.fileprogress.defaults = {
    };

})(window.jQuery);

//   if(!Modernizr.filereader){
//     // skip decorating form
//     return;
//   }

// });
