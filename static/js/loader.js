// selecting dom element
const btn = document.querySelector("#colourise_button");

// adding event listener to button
btn.addEventListener("click", fetchHandler);

// selecting loading div
const loader = document.querySelector("#loading");

// showing loading
function displayLoading() {
    loader.classList.add("display");
    // to stop loading after some time
    setTimeout(() => {
        loader.classList.remove("display");
    }, 5000);
}

// hiding loading
function hideLoading() {
    loader.classList.remove("display");
}



function fetchHandler(event) {
    displayLoading()
    var input = textInput.value;
    var finalURL = buildURL(input);

    fetch(finalURL)
        .then(response => response.json())
        .then(json => {
            hideLoading()
            textOutput.innerText = json.contents.translated;
        })
}

function buildURL(inputData) {
    return `${url}?text=${inputData}`;
}
