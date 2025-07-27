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
    const formChildren = document.getElementById("modify-delete-employee-form").children;
    const selectElement = document.getElementById("modify-name");
    const selectedText = selectElement.options[selectElement.selectedIndex].text;

    employeeData.forEach(element => {
        if (element.name == selectedText) {
            formChildren.age.value = element.age;
            formChildren.street_address.value = element.street_address;
            formChildren.city.value = element.city;
            formChildren.state.value = element.state;
            formChildren.date_of_birth.value = formatDateToInput(element.date_of_birth);
            formChildren.salary.value = element.salary;
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

