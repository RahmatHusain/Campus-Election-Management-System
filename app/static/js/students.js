document.addEventListener('DOMContentLoaded', function () {

    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.student-checkbox');
    const toolbar = document.getElementById('bulkToolbar');
    const selectedCount = document.getElementById('selectedCount');

    function updateToolbar() {

        const checked = document.querySelectorAll('.student-checkbox:checked');
        const count = checked.length;

        if (count > 0) {
            toolbar.style.display = 'block';
            selectedCount.textContent = `${count} selected`;
        } else {
            toolbar.style.display = 'none';
            selectedCount.textContent = '0 selected';
        }

        if (selectAll) {
            selectAll.checked = count === checkboxes.length && count > 0;
        }
    }

    if (selectAll) {

        selectAll.addEventListener('change', function () {

            checkboxes.forEach(cb => {
                cb.checked = this.checked;
            });

            updateToolbar();
        });
    }

    checkboxes.forEach(cb => {
        cb.addEventListener('change', updateToolbar);
    });

    updateToolbar();
});