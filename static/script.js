window.onload = function () {
    // Загрузка сохраненных работ из localStorage
    const works = JSON.parse(localStorage.getItem("works")) || [];
    const selectElement = document.getElementById("work-select");
    works.forEach(work => {
        const optionElement = document.createElement("option");
        optionElement.value = work;
        optionElement.textContent = work;
        selectElement.appendChild(optionElement);
    });

    const fileInput = document.getElementById("file-upload");
    const newWorkCheckbox = document.getElementById("new-work-checkbox");
    const newWorkNameInput = document.getElementById("new-work-name");
    const submitButton = document.getElementById("submit-button");
    const form = document.getElementById("upload-form");
    const loaderContainer = document.getElementById("loader-container");
    const loaderPercentage = document.getElementById("loader-percentage");
    const resultContainer = document.getElementById("result-container");

    newWorkCheckbox.onchange = function () {
        if (newWorkCheckbox.checked) {
            selectElement.style.display = "none";
            newWorkNameInput.style.display = "block";
            newWorkNameInput.disabled = false;
        } else {
            selectElement.style.display = "block";
            newWorkNameInput.style.display = "none";
            newWorkNameInput.disabled = true;
        }
    };

    submitButton.onclick = function () {
    if (fileInput.files.length === 0) {
        alert("Пожалуйста, выберите файл для загрузки.");
        return;
    }

    if (!newWorkCheckbox.checked && selectElement.value === "") {
        alert("Пожалуйста, выберите работу или создайте новую.");
        return;
    }

    const formData = new FormData(form);

    // Очистка результатов перед новым запросом
    resultContainer.innerHTML = "";

    loaderContainer.style.display = "block";

    const xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action);
    xhr.upload.onprogress = function (event) {
        if (event.lengthComputable) {
            const progressPercentage = (event.loaded / event.total) * 100;
            loaderPercentage.textContent = `${Math.round(progressPercentage)}%`;
        }
    };
    xhr.onload = function () {
        loaderContainer.style.display = "none";
        resultContainer.innerHTML = xhr.responseText;

        const workName = newWorkCheckbox.checked ? newWorkNameInput.value : selectElement.value;
        if (works.indexOf(workName) === -1) {
            works.push(workName);
            localStorage.setItem("works", JSON.stringify(works));
            const optionElement = document.createElement("option");
            optionElement.value = workName;
            optionElement.textContent = workName;
            selectElement.appendChild(optionElement);
        }
    };
    xhr.onerror = function () {
        loaderContainer.style.display = "none";
        console.error('Error:', xhr.statusText);
        resultContainer.innerHTML = "Произошла ошибка при отправке данных на сервер.";
    };
    xhr.send(formData);
    };
};
