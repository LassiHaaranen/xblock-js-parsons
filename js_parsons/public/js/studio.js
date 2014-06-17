function JSParsonsXBlockStudioEdit(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'save_problem_lines');

    $('button', element).click(function(eventObject) {
        var problem_lines = $("#problem_lines", element).val();
        problem_lines = problem_lines.replace(/'/g, "\"");
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify( {
                "problem_lines": problem_lines,
                "problem_instructions": $("#problem_instructions", element).val()
            }),
            success: location.reload()
        });
    });
    
    $(function ($) { });
}
