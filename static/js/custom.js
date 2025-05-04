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


document.addEventListener("DOMContentLoaded", function () {
    const availableDates = JSON.parse(document.getElementById("availableDates").textContent);
    const reservedDates  = JSON.parse(document.getElementById("reservedDates").textContent);

    function toYMD(date) {
      return date.toISOString().split('T')[0];
    }

    // initialize flatpickr on the range input
    const fp = flatpickr("#datePicker", {
      mode: "range",
      locale: "fa",
      dateFormat: "Y-m-d",
      disable: reservedDates,     // غیرفعال کردن تاریخ‌های رزرو شده
      enable: availableDates.map(d => ({ from: d, to: d })), // فقط تاریخ‌های مجاز
      onChange: function(selectedDates) {
        if (selectedDates.length === 2) {
          // اگر بخواهید دو فیلد hidden برای ارسال check_in/check_out داشته باشید:
          const [start, end] = selectedDates;
          const inField  = document.createElement('input');
          const outField = document.createElement('input');
          inField.type  = 'hidden'; inField.name  = 'check_in';  inField.value  = toYMD(start);
          outField.type = 'hidden'; outField.name = 'check_out'; outField.value = toYMD(end);
          const form = document.getElementById('booking-form');
          // پاک‌شدن hiddenهای قبلی
          form.querySelectorAll('input[name="check_in"], input[name="check_out"]').forEach(el => el.remove());
          form.append(inField, outField);
        }
      }
    });
});


 // باز کردن فرم پاسخ مربوط به کامنت
    $(document).on('click', '.reply-btn', function (e) {
        e.preventDefault();
        const commentId = $(this).data('comment-id');
        $('.reply-form').slideUp(); // بستن همه فرم‌ها
        $('#reply-form-' + commentId).slideDown(); // باز کردن فرم مورد نظر
    });

    // ارسال پاسخ به صورت Ajax
    $(document).on('click', '.submit-reply', function () {
        const form = $(this).closest('.reply-form-inner');
        const commentText = form.find('.reply-textarea').val();
        const parentId = form.find('.parent-id-input').val();
        const articleId = $('#article-id').val();

        if (!commentText.trim()) {
            alert("متن پاسخ نمی‌تواند خالی باشد.");
            return;
        }

        $.post('/article/add-article-comment/', {
            articleComment: commentText,
            articleID: articleId,
            parentId: parentId,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }).then(res => {
            $('#comment_list').html(res); // رفرش کامنت‌ها
            $('.reply-form').slideUp(); // بستن فرم‌ها بعد از ارسال
        }).fail(function (err) {
            console.error("Error:", err);
            alert("مشکلی پیش آمد. لطفاً دوباره تلاش کنید.");
        });
    });

    // دکمه انصراف
    $(document).on('click', '.cancel-reply', function () {
        $(this).closest('.reply-form').slideUp();
    });