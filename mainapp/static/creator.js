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

// answers
let answerCount = 1;
const answerHtml = document.getElementById('answer_1').innerHTML;
const questionEditor = document.getElementById('question_editor').innerHTML;

function blockButtons(bool){
    if (answerCount>1){
        document.getElementById("btn_rm_answer").disabled = bool;
    }
    document.getElementById("btn_add_answer").disabled = bool;
    document.getElementById("btn_add_question").disabled = bool;
}

function addAnswer(){
    blockButtons(true);
    answerCount++;
    $("input[name='answer_count']").val(answerCount);
    let el = document.createElement("div");
    el.id = `answer_${answerCount}`;
    el.classList.add("collapse", "row", "mb-3");
    let newAnswer = answerHtml;
    newAnswer = newAnswer.replace(RegExp("answer_1", "g"), `answer_${answerCount}`);
    newAnswer = newAnswer.replace(RegExp("Answer 1:", "g"), `Answer ${answerCount}:`);
    el.innerHTML = newAnswer;
    document.getElementById("answers").appendChild(el);
    el.addEventListener('shown.bs.collapse', ()=>{
        blockButtons(false);
    });
    new bootstrap.Collapse(el);
}

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

function submitQuestion(event){
    event.preventDefault();
    $('#question_alert')[0].hidden=true;
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
                    updateQuestion(response.id, response.text, response.image);
                }else{
                    displayQuestion(response.id, response.text, response.image);
                }
                answerCount=1;
                $('#question_editor').html(questionEditor);
                $('#question_editor').removeClass("border-info");
                $('#question_form').submit((e) => submitQuestion(e));
                $('#id_image').change(() => previewImage());
            }else{
                $.each(response.errors, function(name,error){
                    error = `<small class="text-danger error"> ${error} </small>`;
                    $form.find(`[name=${name}]`).after(error);
                })
            }
        },
        error: function(data, status, error){
            $('#question_alert').html(error);
            $('#question_alert')[0].hidden=false;
        },
        cache: false,
        contentType: false,
        processData: false

    });
};

$('#question_form').submit((e) => submitQuestion(e));

function previewImage() {
    const img_data = $('#id_image')[0].files[0];
    const url = URL.createObjectURL(img_data);
    $('#image_preview').html(`<img src="${url}" alt="Image preview" class="img-thumbnail w-25" />`);
};

$('#id_image').change(() => previewImage());

function displayQuestion(id, text, image){
    $('#no_questions').remove();
    let el = document.createElement("div");
    el.id = `question_${id}`;
    el.classList.add("w-25", "p-1", "collapse");
    el.style.minWidth = "200px";
    el.innerHTML = `
        <div class="card h-100">
        <img src="${image}" alt="question image" class="card-img-top" />
        <div class="card-body">
        <h5 class="card-title">${text}</h5>
        <button class="btn btn-info" type="button" onclick="editQuestion(${id})">Edit question</button>
        <button class="btn btn-danger" type="button" onclick="deleteQuestion(${id})">Delete question</button>
        </div>
        </div>
    `;
    document.getElementById('questions').appendChild(el);
    new bootstrap.Collapse(el);
}

function updateQuestion(id, text, image){
    let el = document.getElementById(`question_${id}`);
    el.innerHTML = `
        <div class="card h-100">
        <img src="${image}" alt="question image" class="card-img-top" />
        <div class="card-body">
        <h5 class="card-title">${text}</h5>
        <button class="btn btn-info" type="button" onclick="editQuestion(${id})">Edit question</button>
        <button class="btn btn-danger" type="button" onclick="deleteQuestion(${id})">Delete question</button>
        </div>
        </div>
    `;
    el.classList.add('bg-info');
    setTimeout(()=>{el.classList.remove('bg-info');},2000)
}

function deleteQuestion(id){
    const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $alert = $('#quiz_alert');
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
            }
        },
        error: function (xhr, status, error){
            $alert.removeClass("alert-success");
            $alert.addClass("alert-danger");
            $alert.html(error);
            $alert[0].hidden=false;
        }
    })
}

function editQuestion(id){
    $alert = $('#quiz_alert');
    $.ajax({
        url: `/questions/${id}`,
        type: 'GET',
        success: function (response){
            $('#question_editor').html(response);
            $('#question_editor').addClass("border-info");
            $('#question_editor')[0].scrollIntoView();
            $('#question_form').submit((e) => submitQuestion(e));
            $('#id_image').change(() => previewImage());
            answerCount = Number($("input[name='answer_count']").val());
            blockButtons(false);
        },
        error: function (xhr, status, error){
            $alert.removeClass("alert-success");
            $alert.addClass("alert-danger");
            $alert.html(error);
            $alert[0].hidden=false;
        }
    })
}

function cancelEdit(){
    $('#question_editor').html(questionEditor);
    $('#question_editor').removeClass("border-info");
    $('#question_form').submit((e) => submitQuestion(e));
}