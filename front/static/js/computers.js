window.onload = get_computer_list()

async function get_computer_list() {

    response = await fetch(window.url.get,{
        method : "get",
    });
    if (!response.ok) {
        setTimeout(() => {
            alert("somthing wrong")
        }, 500);
    }
    data = await response.json()
    try {
        let list_of_computer = data["list_of_computer"]
        add_to_datalist(list_of_computer)
    }
    catch(error){
        setTimeout(() => {
            alert(error)
        }, 500);    
    }   
}

async function add_to_datalist(list_of_computer) {
    let computer_datalist = document.getElementById("computer_datalist")
    computer_datalist.innerHTML = ""
    list_of_computer.forEach(computer => {
        let option = document.createElement("option");
        option.value = computer;
        computer_datalist.appendChild(option)
    })
}

function go_to_computer_html() {
    let computer_name = document.getElementById("computerName").value
    document.getElementById("computer").action += computer_name
}