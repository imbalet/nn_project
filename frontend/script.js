let params;

let selectedData;

let selectedParam = null;

let variants = {};


const showVariants = (text = "", num = 20) => {
    let keys = Object.keys(variants).sort((a, b) => variants[a]["name"].toLowerCase().indexOf(text.toLowerCase()) - variants[b]["name"].toLowerCase().indexOf(text.toLowerCase()));
    let elems = [];

    document.getElementById("search").placeholder = "Начните вводить";
    document.getElementById("variants").innerHTML = "";
    for (let el of keys) {
        if (variants[el]["name"].toLowerCase().includes(text.toLowerCase())) {
            const newVar = document.createElement("div");
            const img = document.createElement("img");
            img.src = variants[el]["pic"];
            newVar.textContent = variants[el]["name"];
            newVar.className = "variant";
            newVar.addEventListener("click", () => {
                selectedData[selectedParam] = el;
                updateParamsList();
            });
            newVar.append(img);
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

const fetchVars = async (request, have = "") => {
    try {
        const response = await fetch("/get_variants");
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const updateVariants = () => {
    variants = {};
    if (selectedParam !== null && params[selectedParam]["type"] == "str") {
        //TODO тут запрос с бека GET
        /*
        запрос json
        {
            "request": "model",
            "have": {"mark": "", "model": ""}
        }


        какой-то такой формат ответа
        {
            "bmw": {"name": "БНВ", "pic": "images/penis.jpeg"},
        }
        */
        let variants_answ = {
            "bmw": { "name": "БНВ", "pic": "images/penis.jpeg" },
        }
        variants = variants_answ;
        showVariants();
    }
    else if (params[selectedParam]["type"] == "num") {
        document.getElementById("search").placeholder = "Введите значение";
    }
};


const updateParamsList = () => {
    document.getElementById("params").innerHTML = "";

    const dataKeys = Object.keys(selectedData);
    let keys = [dataKeys[0]];
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
        newDiv.innerHTML = params[key]["name"];
        newDiv.addEventListener("click", () => {
            const allParams = document.querySelectorAll('.param');
            allParams.forEach(param => param.classList.remove('pressed'));

            newDiv.classList.add('pressed');

            selectedParam = key;
            updateVariants();
        });
        if (key == keys[keys.length - 1]) { newDiv.classList.add("pressed"); }
        document.getElementById("params").append(newDiv);
    }

};


const fetchParams = async () => {
    try {
        const response = await fetch("/params");
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};


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



