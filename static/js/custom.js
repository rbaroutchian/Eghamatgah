document.addEventListener('DOMContentLoaded', function() {
    const bookingForm = document.querySelector('#booking-form');
    const totalPriceElement = document.querySelector('#total-price');

    const eghamat_pk = parseInt("{{ eghamat.pk }}");

    bookingForm.addEventListener('change', function() {
        const persons = document.querySelector('#id_persons').value;
        const check_in = document.querySelector('#id_check_in').value;
        const check_out = document.querySelector('#id_check_out').value;

        if (persons && check_in && check_out) {
            const url = `/eghamatgah/${eghamat_pk}/calculate_price/`;  // اصلاح مسیر
            const params = new URLSearchParams({
                persons: persons,
                check_in: check_in,
                check_out: check_out
            });

            fetch(`${url}?${params}`)
                .then(response => response.json())
                .then(data => {
                    if (data.total_price) {
                        totalPriceElement.textContent = `قیمت نهایی: ${data.total_price} تومان`;
                    } else {
                        totalPriceElement.textContent = 'خطا در محاسبه قیمت';
                    }
                })
                .catch(error => {
                    totalPriceElement.textContent = 'خطا در ارتباط با سرور';
                });
        }
    });
});



function sendArticleComment(articleId){
    event.preventDefault();
    var comment = $('#commentText').val();
    var parentId = $('#parentId').val() || null;
    console.log("Parent ID:", parentId);
    $.post('/article/add-article-comment/',{
     articleComment : comment ,
     articleID : articleId,
     parentId : parentId,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()

    }).then(res=>{
        console.log("Response:", res);
        $('#comment_list').html(res);
        $('#commentText').val('');
        $('#parentId').val('');




        if (parentId !== null && parentId !==''){
            let newcomment=document.getElementById('single_comment_box_' + parentId);
            if (newComment) {
                newComment.scrollIntoView({ behavior: 'smooth' });
            }
            // scrollIntoView({behavior:'smooth'})
        }
        else {
            let lastComment=document.querySelector("#comment_list > div:last-child");
             if (lastComment) {
                lastComment.scrollIntoView({ behavior: 'smooth' });
            }
            // scrollIntoView({behavior:'smooth'})

        }
        })
    .fail(function(err) {
        console.error("Error:", err);
    });
}


function fillParentId(parentId){
    $('#parentId').val(parentId);
    document.getElementById('commentForm').scrollIntoView({behavior:"smooth"})
}


$(document).ready(function () {
    $("#contact-form").submit(function (event) {
        event.preventDefault();

        Swal.fire({
            title: "در حال ارسال...",
            text: "لطفاً منتظر بمانید.",
            icon: "info",
            showConfirmButton: false,
            timer: 1500
        });

        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),
            success: function (response) {
                Swal.fire({
                    title: "موفق!",
                    text: "پیام شما با موفقیت ارسال شد.",
                    icon: "success",
                    confirmButtonText: "باشه"
                });
            },
            error: function () {
                Swal.fire({
                    title: "خطا!",
                    text: "مشکلی رخ داده است.",
                    icon: "error",
                    confirmButtonText: "تلاش مجدد"
                });
            }
        });
    });
});
