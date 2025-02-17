counter = 0
font_size = 20

the_computer_list = ["computer1","computer2","computer3"]

async function get_data() {

    let dropdown = document.getElementById("computer_options")

    // computer_list = get_computer_list_from_server()
    computer_list = await get_computer_list_from_server()
    computer_list.forEach(function(computer_name) {
        let option = document.createElement("option");
        option.text = computer_name;
        
        dropdown.add(option);
    });
    show_list(computer_list)
}


async function get_computer_list_from_server() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/get_machine_list",
            {
                method : 'GET',
                headers : {
                    "accept" : "application/json"
                },
            });
        const data = await response.json()
        return data["message"]
    }
    catch(error){
        alert(error)
    }
}

async function get_select_options() {
    let dropdown = document.getElementById("computer_options")
    let selectoption = dropdown.options[dropdown.selectedIndex].text
    try {
        const response = await fetch("http://127.0.0.1:5000/api/get_keystrokes?computer=" + selectoption,
            {
                method : 'GET',
                    headers : {
                        "accept" : "application/json"
                    },
            });
        const data = await response.json()
        let result = document.getElementById("result")
        result.textContent = JSON.stringify(data["data"],null,2)
    }
    catch(error){
        alert(error)
    }
}

function show_list(computer_list) {
    if (computer_list.length === 0){
        let list = document.createElement("li");
        list.textContent = "Emptylist";
        document.getElementById("list").appendChild(list);    
    }
    else {
        computer_list.forEach(function(computer){
            let list = document.createElement("li");
            let link = document.createElement("a");
            link.href = "newpage.html?name=" + computer
            link.textContent = computer
            list.appendChild(link)
            document.getElementById("list").appendChild(list);
        });
    };
}

function home_button() {
    window.location.href = "home_page/home.html"
}
