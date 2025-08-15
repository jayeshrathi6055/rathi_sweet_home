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

    modifyBtn.addEventListener("click", () => formMethod.value = "PUT");

    deleteBtn.addEventListener("click", () => formMethod.value = "DELETE");
}

function updateModifyDeleteEmployeeFormInputValues() {
    const selectElement = document.getElementById("modify-name");
    const selectedText = selectElement.options[selectElement.selectedIndex].text;
    const ageElement = document.getElementById("modify-age");
    const streetAddressElement = document.getElementById("modify-street_address");
    const cityElement = document.getElementById("modify-city");
    const stateElement = document.getElementById("modify-state");
    const dateOfBirthElement = document.getElementById("modify-date_of_birth");
    const monthlySalaryBaseElement = document.getElementById("modify-monthly-salary-base");
    const monthlySalaryLeftElement = document.getElementById("modify-monthly-salary-left");

    employeeData.forEach(element => {
        if (element.name === selectedText) {
            ageElement.value = element.age;
            streetAddressElement.value = element.street_address;
            cityElement.value = element.city;
            stateElement.value = element.state;
            dateOfBirthElement.value = formatDateToInput(element.date_of_birth);
            monthlySalaryBaseElement.value = element.monthly_salary_base;
            monthlySalaryLeftElement.value = element.monthly_salary_left;
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

