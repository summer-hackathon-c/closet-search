document.addEventListener("DOMContentLoaded", function () {
    flatpickr(".datepicker", {
    dateFormat: "Y-m-d",
    allowInput: true,
    locale: "ja",
    disableMobile: true,
    // minDate: "2000-01-01",
    maxDate: "today",
    });
});