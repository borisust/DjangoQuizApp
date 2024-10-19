
let answerCount = 1;
const questionEditor = document.getElementById('question_editor').innerHTML;

// quiz form submit action
$('#quiz_form').submit( (event) => {
    event.preventDefault();
    $('.error').remove();
    $form = $('#quiz_form');
    $alert = $('#quiz_alert');
    $alert[0].hidden=true;
    let formData = new FormData($form[0]);
    $.ajax({
        type: 'POST',
        url: $form.attr('action'),
        data: formData,
        success: function(response) {
            if (response.success){
                $alert.removeClass("alert-danger");
                $alert.addClass("alert-success");
                $alert.html("Quiz saved");
                $alert[0].hidden=false;
            }else{
                $.each(response.errors, function(name,error){
                    error = `<small class="text-danger error"> ${error} </small>`;
                    $form.find(`[name=${name}]`).after(error);
                });
            }
        },
        error: function(data, status, error){
            $alert.removeClass("alert-success");
            $alert.addClass("alert-danger");
            $alert.html(error);
            $alert[0].hidden=false;
        },
        cache: false,
        contentType: false,
        processData: false
    });
});

// lock/unlock question form buttons
function blockButtons(bool){
    if (answerCount>1){
        document.getElementById("btn_rm_answer").disabled = bool;
    }
    document.getElementById("btn_add_answer").disabled = bool;
    document.getElementById("btn_add_question").disabled = bool;
    document.getElementById("btn_reset_form").disabled = bool;
}

// add an answer option to the question form
function addAnswer(){
    blockButtons(true);
    answerCount++;
    $("input[name='answer_count']").val(answerCount);
    let el = document.createElement("div");
    el.id = `answer_${answerCount}`;
    el.classList.add("collapse", "row", "mb-3");
    let newAnswer = document.getElementById('answer_1').innerHTML;
    newAnswer = newAnswer.replace(RegExp("answer_1", "g"), `answer_${answerCount}`);
    newAnswer = newAnswer.replace("Answer 1:", `Answer ${answerCount}:`);
    newAnswer = newAnswer.replace(RegExp('value="1"', "g"), `value="${answerCount}"`);
    el.innerHTML = newAnswer;
    document.getElementById("answers").appendChild(el);
    $(`#answer_${answerCount}_text`).val("");
    el.addEventListener('shown.bs.collapse', ()=>{
        blockButtons(false);
    });
    new bootstrap.Collapse(el);
}

// remove an answer option from question form
function removeAnswer(){
    blockButtons(true);
    const el = document.getElementById(`answer_${answerCount}`);
    answerCount--;
    $("input[name='answer_count']").val(answerCount);
    el.addEventListener('hidden.bs.collapse', ()=>{
        el.remove();
        blockButtons(false);
    });
    new bootstrap.Collapse(el);
}

// preview the image to be uploaded in the question form
function previewImage() {
    const img_data = $('#id_image')[0].files[0];
    const url = URL.createObjectURL(img_data);
    $('#image_preview').html(`<img src="${url}" alt="Image preview" class="img-thumbnail" style="max-height: 200px;" />`);
};
$('#id_image').change(() => previewImage());

function changeQuestionType(){
    type = $('#id_type')[0].selectedOptions[0].value;
    if (type=='RB'){
        $('.answer_check').prop('type','radio');
    }else if (type=='CB'){
        $('.answer_check').prop('type','checkbox');
    }
}
$('#id_type').change(()=>changeQuestionType());

function resetQuestionForm(){
    answerCount=1;
    $('#question_editor').html(questionEditor);
    $('#question_editor').removeClass("border-info");
    $('#question_form').submit((e) => submitQuestion(e));
    $('#id_image').change(() => previewImage());
    $('#id_type').change(()=>changeQuestionType());
}

function submitQuestion(event){
    event.preventDefault();
    blockButtons(true);
    $('.error').remove();
    $form = $('#question_form');
    let formData = new FormData($form[0]);
    $.ajax({
        url: $form.attr('action'),
        type: 'POST',
        data: formData,
        success: function (response) {
            if (response.success){
                if (response.hasOwnProperty('edit')){
                    document.getElementById(`question_${response.id}`).outerHTML = response.data;
                    let el = document.getElementById(`question_${response.id}`);
                    el.classList.add('bg-info');
                    setTimeout(()=>{el.classList.remove('bg-info');},2000)
                }else{
                    document.getElementById('questions').innerHTML += response.data;
                    new bootstrap.Collapse(document.getElementById(`question_${response.id}`));
                }
                resetQuestionForm();
            }else{
                $.each(response.errors, function(name,error){
                    error = `<small class="text-danger error"> ${error} </small>`;
                    $form.find(`[name=${name}]`).after(error);
                })
                blockButtons(false);
            }
        },
        error: function(data, status, error){
            showError(error);
            blockButtons(false);
        },
        cache: false,
        contentType: false,
        processData: false

    });
};
$('#question_form').submit((e) => submitQuestion(e));

function deleteQuestion(id){
    $('#questions_spinner')[0].hidden=false;
    const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax({
        url: `/questions/${id}/delete`,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrf
        },
        success: function (response){
            if (response.success){
                const el = document.getElementById(`question_${id}`);
                el.addEventListener('hidden.bs.collapse', ()=>{
                    el.remove();
                });
                new bootstrap.Collapse(el);
            }else{
                showError('Something went wrong...');
            }
        },
        error: function (xhr, status, error){
            showError(error);
        }
    }).always(()=>{
        $('#questions_spinner')[0].hidden=true;
    });
}

// get and display a question editor
function editQuestion(id){
    blockButtons(true);
    $.ajax({
        url: `/questions/${id}`,
        type: 'GET',
        success: function (response){
            $('#question_editor').html(response);
            $('#question_editor').addClass("border-info");
            $('#question_editor')[0].scrollIntoView();
            $('#question_form').submit((e) => submitQuestion(e));
            $('#id_image').change(() => previewImage());
            $('#id_type').change(()=>changeQuestionType());
            answerCount = Number($("input[name='answer_count']").val());
        },
        error: function (xhr, status, error){
            showError(error);
            blockButtons(false);
        }
    })
}

// publish a quiz
$('#publish_form').submit((event) => {
    event.preventDefault();
    $('#btn_publish')[0].disabled = true;
    $form = $('#publish_form');
    $alert = $('#publish_error');
    $alert.html('');
    let formData = new FormData($form[0]);
    $.ajax({
        url: $form.attr('action'),
        type: 'POST',
        data: formData,
        success: function (response) {
            if (response.success){
                window.location.href = response.url;
            }else{
                $alert.html(response.msg);
                $('#btn_publish')[0].disabled = false;
            }
        },
        error: function(data, status, error){
            showError(error);
            $('#btn_publish')[0].disabled = false;
        },
        cache: false,
        contentType: false,
        processData: false

    });
});

function swapQuestions(id1, id2){
    document.getElementById('btn_questions_order').hidden = false;
    let el1 = document.getElementById(id1);
    let el2 = document.getElementById(id2);
    el2.addEventListener('hidden.bs.collapse', ()=>{
        let temp = el1.outerHTML;
        el1.outerHTML = el2.outerHTML;
        el2.outerHTML = temp;
        new bootstrap.Collapse(document.getElementById(id1));
        new bootstrap.Collapse(document.getElementById(id2));
    });
    new bootstrap.Collapse(el1);
    new bootstrap.Collapse(el2);
}


function moveQuestionBack(questionID){
    let question = $(`#question_${questionID}`);
    if (question.next().length > 0){
        swapQuestions(question[0].id, question.next()[0].id);
    }
}

function moveQuestionForward(questionID){
    let question = $(`#question_${questionID}`);
    if (question.prev().length > 0){
        swapQuestions(question[0].id, question.prev()[0].id);
    }
}

$('#question_order_form').submit((event)=>{
    event.preventDefault();
    $('#questions_spinner')[0].hidden = false;
    $form = $('#question_order_form');
    let formData = new FormData($form[0]);
    $.ajax({
        url: $form.attr('action'),
        type: 'POST',
        data: formData,
        success: function (response) {
            if (response.success){
                $('#btn_questions_order')[0].hidden = true;
            }else{
                showError('Something went wrong.');
            }
        },
        error: function(data, status, error){
            showError(error);
        },
        cache: false,
        contentType: false,
        processData: false

    }).always(()=> {
        $('#questions_spinner')[0].hidden = true;
    });
});