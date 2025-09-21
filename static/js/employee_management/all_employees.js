nav_dropdown_active_link("employee-information-nav-link");
const employeeData = JSON.parse(document.getElementById("employee-data").textContent);

function showSaveEmployeeForm() {
    document.getElementById("save-employee").style.display = "grid";
}

function closeSaveEmployeeForm() {
    document.getElementById("save-employee").style.display = "none";
}

function modifyDeleteEmployeeForm() {
    document.getElementById("modify-delete-employee").style.display = "grid";
    updateModifyDeleteEmployeeFormInputValues();
    modifyDeleteEmployeeFormEventListeners();
}

function modifyDeleteEmployeeFormEventListeners() {
    const formMethod = document.getElementById("modify-delete-employee-form-method");
    const modifyBtn = document.getElementById("modify-btn");
    const deleteBtn = document.getElementById("delete-btn");
    const selectElement = document.getElementById("modify-name");

    selectElement.addEventListener("change", () => updateModifyDeleteEmployeeFormInputValues());

    modifyBtn.addEventListener("click", (event) => {
        event.preventDefault();
        const confirmed = confirm("Are you sure you want to modify this employee?")
        if (confirmed) {
            formMethod.value = "PUT"
            formMethod.parentElement.submit();
        }
    });

    deleteBtn.addEventListener("click", (event) => {
        event.preventDefault();
        const confirmed = confirm("Are you sure you want to delete this employee?")
        if (confirmed) {
            formMethod.value = "DELETE"
            formMethod.parentElement.submit();
        }
    });
}

function updateModifyDeleteEmployeeFormInputValues() {
    const selectElement = document.getElementById("modify-name");
    const selectedText = selectElement.options[selectElement.selectedIndex].text;
    const addressElement = document.getElementById("modify-address");
    const dateOfBirthElement = document.getElementById("modify-date_of_birth");
    const mobileNumberElement = document.getElementById("modify-mobile_number");
    const yearlySalaryElement = document.getElementById("modify-yearly-salary");

    employeeData.forEach(element => {
        if (element.name === selectedText) {
            addressElement.value = element.address;
            dateOfBirthElement.value = formatDateToInput(element.date_of_birth);
            mobileNumberElement.value = element.mobile_number;
            yearlySalaryElement.value = element.yearly_salary;
        }
    });
}

function closeModifyDeleteEmployeeForm() {
    document.getElementById("modify-delete-employee").style.display = "none";
}

function formatDateToInput(dateString) {
    // Assuming input is in "dd/mm/yyyy"
    const [day, month, year] = dateString.split("/");
    return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
}


document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        document.getElementById("save-employee").style.display = "none";
        document.getElementById("modify-delete-employee").style.display = "none";
    }
});

