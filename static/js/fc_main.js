(function($) {

  $('#proofType').parent().append('<ul class="list-item" id="newproofType" name="proofType"></ul>');
  $('#proofType option').each(function(){
      $('#newproofType').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
  });
  $('#proofType').remove();
  $('#newproofType').attr('id', 'proofType');
  $('#proofType li').first().addClass('init');
  $("#proofType").on("click", ".init", function() {
      $(this).closest("#proofType").children('li:not(.init)').toggle();
  });
  
  var allOptions = $("#proofType").children('li:not(.init)');
  $("#proofType").on("click", "li:not(.init)", function() {
      allOptions.removeClass('selected');
      $(this).addClass('selected');
      $("#proofType").children('.init').html($(this).html());
      allOptions.toggle();
  });

  $('#reset').on('click', function(){
      $('#register-form').reset();
  });

  $('#register-form').validate({
    rules : {
        firstName : {
            required: true,
        },
        lastName : {
            required: true,
        },
        contactNo : {
            required: true
        },
        email : {
            required: true,
            email : true
        },
        location : {
            required: true,
        },
        idno : {
            required: true,
        }
    },
    onfocusout: function(element) {
        $(element).valid();
    },
});

    jQuery.extend(jQuery.validator.messages, {
        required: "",
        remote: "",
        email: "",
        url: "",
        date: "",
        dateISO: "",
        number: "",
        digits: "",
        creditcard: "",
        equalTo: ""
    });
})(jQuery);


$(document).ready(function () {
    $(".drop .option").click(function () {
      var val = $(this).attr("data-value"),
        $drop = $(".drop"),
        prevActive = $(".drop .option.active").attr("data-value"),
        options = $(".drop .option").length;
      $drop.find(".option.active").addClass("mini-hack");
      $drop.toggleClass("visible");
      $drop.removeClass("withBG");
      $(this).css("top");
      $drop.toggleClass("opacity");
      $(".mini-hack").removeClass("mini-hack");
      if ($drop.hasClass("visible")) {
        setTimeout(function () {
          $drop.addClass("withBG");
        }, 400 + options * 100);
      }
      triggerAnimation();
      if (val !== "placeholder" || prevActive === "placeholder") {
        $(".drop .option").removeClass("active");
        $(this).addClass("active");
      }
    });
  
    function triggerAnimation() {
      var finalWidth = $(".drop").hasClass("visible") ? 22 : 20;
      $(".drop").css("width", "24em");
      setTimeout(function () {
        $(".drop").css("width", finalWidth + "em");
      }, 400);
    }
  });
  