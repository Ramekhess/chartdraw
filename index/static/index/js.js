$(document).ready(function () {
    $("input[name='options_chart']").change(function () {
        var value = $(this).val();
        $('.options-vars').hide();
        $(this).parent().parent().find('input:checkbox[name=options_var]').each(function () {
            console.log($(this));
            $(this).prop("checked", false);
        });
        $(this).parent().siblings('.options-vars').show();
        console.log(value);
    });

    $("button.affiche_desc").on("click", function(){
        $(".affiche_desc_table").toggle();
        $(".span").toggle();
    });

    $("button.affiche_table").on("click", function(){
        $(".affiche_all_table").toggle();
        $(this).child(".span").toggle();
    });
});