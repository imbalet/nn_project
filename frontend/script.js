// Параметры автомобиля
let params;
// Выбранные/введенные параметры
let selectedData;
// Какой парметр в данный момент вводится/выбирается
let selectedParam = null;

let cur_variants;

const showVariants = (text = "", num = 20) => {
    let elems = [];

    document.getElementById("search").placeholder = "Начните вводить";
    document.getElementById("variants").innerHTML = "";
    for (let el of cur_variants) {
        if (el["name"].toLowerCase().includes(text.toLowerCase())) {
            const newVar = document.createElement("div");
            newVar.textContent = el["name"];
            newVar.className = "variant";
            if (selectedParam == "color") {
                newVar.style.backgroundColor = '#' + el["name"];
            }
            newVar.addEventListener("click", () => {
                selectedData[selectedParam] = el["type"];
                updateParamsList();
            });
            elems.push(newVar);
        }
        if (elems.length >= num) {
            break;
        }
    }
    elems.forEach((el) => {
        document.getElementById("variants").append(el);
    });
};

const updateVariants = async () => {
    document.getElementById("variants").innerHTML = "";
    document.getElementById("search").value = "";
    if (document.getElementById("confirm"))
        document.getElementById("confirm").remove();

    if (selectedParam !== null && params[selectedParam]["type"] == "str") {
        document.getElementById("search").type = "search";
        switch (selectedParam) {
            case ("body_type_type"):
                await fetchBodyTypes(selectedData["mark"], selectedData["model"], selectedData["super_gen_name"]).then(data => cur_variants = data);
                break;
            case ("color"):
                await fetchColors().then(data => cur_variants = data);
                break;
            case ("complectation"):
                await fetchComplectations(selectedData["mark"], selectedData["model"], selectedData["super_gen_name"]).then(data => cur_variants = data);
                break;
            case ("engine"):
                await fetchEngines(selectedData["mark"], selectedData["model"], selectedData["super_gen_name"]).then(data => cur_variants = data);
                break;
            case ("gear_type"):
                await fetchGearTypes().then(data => cur_variants = data);
                break;
            case ("mark"):
                await fetchMarks().then(data => cur_variants = data);
                break;
            case ("model"):
                await fetchModels(selectedData["mark"]).then(data => cur_variants = data);
                break;
            case ("owners"):
                await fetchOwners().then(data => cur_variants = data);
                break;
            case ("region"):
                await fetchRegion().then(data => cur_variants = data);
                break;
            case ("steering_wheel"):
                await fetchSteeringWheels().then(data => cur_variants = data);
                break;
            case ("super_gen_name"):
                await fetchGens(selectedData["mark"], selectedData["model"]).then(data => cur_variants = data);
                break;
            case ("transmission"):
                await fetchTransmissions(selectedData["mark"], selectedData["model"], selectedData["super_gen_name"]).then(data => cur_variants = data);
                break;
            case ("year"):
                await fetchYears(selectedData["mark"], selectedData["model"], selectedData["super_gen_name"]).then(data => cur_variants = data);
                break;
            default:
                break;
        }

        showVariants();
    }
    else if (params[selectedParam]["type"] == "num") {
        document.getElementById("search").type = "number";
        document.getElementById("search").placeholder = "Введите значение";
        const button = document.createElement("button");
        button.id = "confirm";
        button.className = "button";
        button.textContent = "Подтвердить";
        button.addEventListener("click", (e) => {
            selectedData[selectedParam] = document.getElementById("search").value;
            updateParamsList();
        });
        document.getElementById("search_wrapper").append(button);
    }
};


const updateParamsList = () => {
    document.getElementById("params").innerHTML = "";

    const dataKeys = Object.keys(selectedData);
    let keys = [dataKeys[0]];
    const oldSelectedParam = selectedParam;
    selectedParam = keys[0];
    for (let i = 1; i < dataKeys.length; ++i) {
        if (selectedData[dataKeys[i - 1]] !== null) {
            keys.push(dataKeys[i]);
            selectedParam = dataKeys[i];
        } else {
            break;
        }
    }

    for (let key of keys) {
        const newDiv = document.createElement('div');
        newDiv.className = 'param';
        newDiv.innerHTML = selectedData[key] === null ? params[key]["name"] : selectedData[key];
        newDiv.addEventListener("click", () => {
            const allParams = document.querySelectorAll('.param');
            allParams.forEach(param => param.classList.remove('pressed'));
            newDiv.classList.add('pressed');
            selectedParam = key;
            updateVariants();
            if (Object.keys(selectedData)[Object.keys(selectedData).length - 1] == selectedParam) {
                const button = document.createElement("button");
                button.id = "predict";
                button.className = "button";
                button.textContent = "Рассчитать";
                button.addEventListener("click", (e) => {
                    if (Object.values(selectedData).every(value => value !== null)) {
                        fetch_post("predict", selectedData).then(data => console.log(data));
                    }
                    else {
                        alert("hz");
                    }
                });
                document.getElementById("selection").append(button);
            }
            else {
                if (document.getElementById("predict"))
                    document.getElementById("predict").remove();
            }
        });
        if (oldSelectedParam == keys[keys.indexOf(key) - 1] && keys.length <= Object.keys(selectedData).length) { newDiv.click(); }
        document.getElementById("params").append(newDiv);
    }
};


const fetch_get = async (param) => {
    try {
        const response = await fetch("/api/" + param);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const fetch_post = async (url, data) => {
    try {
        const response = await fetch("/api/" + url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const res = await response.json();
        return res;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const fetchModels = async (mark) => fetch_post("models", { "mark": mark });
const fetchGens = async (mark, model) => fetch_post("gens", { "mark": mark, "model": model });
const fetchComplectations = async (mark, model, gen) => fetch_post("complectations", { "mark": mark, "model": model, "gen": gen });
const fetchTransmissions = async (mark, model, gen) => fetch_post("transmission", { "mark": mark, "model": model, "gen": gen });
const fetchEngines = async (mark, model, gen) => fetch_post("engines", { "mark": mark, "model": model, "gen": gen });
const fetchYears = async (mark, model, gen) => fetch_post("years", { "mark": mark, "model": model, "gen": gen });
const fetchBodyTypes = async (mark, model, gen) => fetch_post("bodies", { "mark": mark, "model": model, "gen": gen });

const fetchParams = async () => fetch_get("params");
const fetchMarks = async () => fetch_get("marks");
const fetchColors = async () => fetch_get("colors");
const fetchSteeringWheels = async () => fetch_get("steering_wheels");
const fetchGearTypes = async () => fetch_get("gear_types");
const fetchOwners = async () => fetch_get("owners");
const fetchRegion = async () => fetch_get("regions");


document.addEventListener('DOMContentLoaded', async (e) => {
    await fetchParams().then(data => params = data);
    selectedData = Object.keys(params).reduce((acc, key) => {
        acc[key] = null;
        return acc;
    }, {});
    updateParamsList();


    updateVariants();
    document.getElementById("search").addEventListener("keyup", (e) => {
        showVariants(e.target.value);
    });

});



