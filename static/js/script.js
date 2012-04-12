/* Author: Kevin Burke */
$(document).ready(function(){
    $("#add").toggle(function(){
        $("#addevent").slideDown("slow");
    }, function(){
        $("#addevent").slideUp("slow");
    });

    var max_length    = 300;
    var the_date_val  = "Wednesday, December 1, 5pm-8pm";
    var the_name_val  = "Name or email";
    var the_snack_val = "(909) 621-8000";
    whenkeydown(max_length);

    reset_val("#the_contact", the_name_val);
    reset_val("#the_date", the_date_val );
    reset_val("#snack_phoneno", the_snack_val);

    $("#phone_submit").click(function(event){
        var phoneNo = $("#snack_phoneno").val();
        $("#phone_slideup").slideUp("slow", function(){
            /* let user know what's happened */
            $("#submitting").show();
            /*post user phone number to the server */
            $.post("/phoneno/",
                {phone : phoneNo },
                function(data){
                    $("#submitting").hide();
                    $("#phone_facebook").slideDown("slow");
                }
              );
        });

        event.preventDefault();
    });

    $("#the_submit").click(function(event){
        $(".error").hide();
        var hasError = false;
        var nameVal = $("#the_contact").val();

        if (nameVal == '' || nameVal == the_name_val){
            $("#the_count").after('<div class="error">Please enter your name.<br></div>');
            hasError = true;
        }
        var dateVal = $("#the_date").val();

        if (dateVal == '' || dateVal == the_date_val ){
            $("#the_count").after('<div class="error">Please enter a date.<br></div>');
            hasError = true;
        }
        var eventVal = $("#the_event").val();

        if (eventVal == '' || eventVal == the_date_val ){
            $("#the_count").after('<div class="error">Please enter an event description.<br></div>');
            hasError = true;
        }
        if (!hasError){
            $(this).hide();
            $.post("/mail.php",
                    {name : nameVal, date : dateVal, the_event : eventVal },
                    function(data){
                        $("#addevent").slideUp("normal", function(){
                            $("#addevent").before('<div class="success"><h1>Success!</h1><p>Your event has been added to the list.</p></div>');
                        });
                    }
                  );
        }
        event.preventDefault();
    });
});

reset_val = function(selector, default_text){
    $(selector).focus(function(){
        if ($(this).val() === default_text){
            $(this).val("");
            $(this).css("color", "#444");
        }
    });
};
whenkeydown = function(max_length) {
    $("#the_event").unbind().keyup(function(){

        if(document.activeElement.id === "the_event"){
            var text = $(this).val();

            var numofchars = text.length;

            if (numofchars <= max_length){
                $("#the_count").html("").html(max_length - text.length);

                if (max_length - numofchars <= 20){
                    $("#the_count").css("color", "#740e1c");
                }
            }
            else{
                $(this).val(text.substring(0, max_length));
            }
        }
    });
};
