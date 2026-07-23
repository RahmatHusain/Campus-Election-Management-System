document.addEventListener('DOMContentLoaded', () => {

    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.student-checkbox');
    const toolbar = document.getElementById('bulkToolbar');
    const counter = document.getElementById('selectedCount');

    function updateToolbar() {

        const checked = document.querySelectorAll('.student-checkbox:checked');

        counter.textContent = checked.length;

        toolbar.style.display = checked.length > 0 ? 'block' : 'none';

        if (selectAll) {

            selectAll.checked =
                checked.length === checkboxes.length && checkboxes.length > 0;
        }
    }

    // Select All
    if (selectAll) {

        selectAll.addEventListener('change', () => {

            checkboxes.forEach(cb => {
                cb.checked = selectAll.checked;
            });

            updateToolbar();
        });
    }

    // Individual Checkboxes
    checkboxes.forEach(cb => {

        cb.addEventListener('change', updateToolbar);
    });

    // Form Validation
    const form = document.getElementById('bulkActionForm');

    if (form) {

        form.addEventListener('submit', (e) => {

            const checked =
                document.querySelectorAll('.student-checkbox:checked');

            if (checked.length === 0) {

                e.preventDefault();

                alert('Please select at least one student.');
            }
        });
    }

    updateToolbar();
});