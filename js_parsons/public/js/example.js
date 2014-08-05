
function  JSParsonsXBlock(runtime, element) {
    var parson;    

    function displayErrors(fb) {
        if(fb.errors.length > 0) {
            alert(fb.errors[0]);
        }
    } 

    $(document).ready(function(){
        var initial = $(element).find(".problem_lines").text()
        parson = new ParsonsWidget({
            'sortableId': 'sortable',
            'trashId': 'sortableTrash',
            'max_wrong_lines': 1,
            'feedback_cb' : displayErrors
        });
        parson.init(initial);
        parson.shuffleLines();
        $("#newInstanceLink").click(function(event){
            event.preventDefault();
            parson.shuffleLines();
        });
        $("#feedbackLink").click(function(event){
            event.preventDefault();

            reportProgress(parson.getFeedback(), parson.user_actions)
        });
    });

    function reportProgress(feedback, actions) {        
        var handlerUrl = runtime.handlerUrl(element, 'report_progress');
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({
                "feedback": feedback,
                "actions": actions
            }),            
            success: updateScore
        });       
    }

    function updateScore(result) {
        $(".problem_score", element).text(result.student_score);
        $(".student_attempts", element).text(result.student_attempts);
    }
}


