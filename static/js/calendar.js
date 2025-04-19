document.addEventListener("DOMContentLoaded", function () {
    // تاریخ‌های غیرقابل رزرو که از سرور دریافت می‌شود
    const unavailableDates = window.unavailableDates || [];

    // راه‌اندازی پلاگین flatpickr برای نمایش تقویم
    flatpickr("#calendar-display", {
        dateFormat: "Y-m-d",
        disable: unavailableDates,  // تاریخ‌های غیرقابل رزرو غیرفعال می‌شوند
        locale: "fa",  // تقویم به زبان فارسی
        inline: true,  // تقویم به صورت inline (دست‌نخورده) نمایش داده می‌شود
        clickOpens: false  // کلیک کردن برای باز شدن تقویم لازم نیست
    });
});


