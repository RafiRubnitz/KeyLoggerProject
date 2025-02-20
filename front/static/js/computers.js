window.onload = get_computer_list()

async function get_computer_list() {
    response = await fetch("http://127.0.0.1:5000/computers/get_computers_list",{
        method : "get",
    });
    if (!response.ok) {
        alert("somthing wrong")
    }
    data = await response.json()
    console.log("data recived:" , data)
    try {
        let list_of_computer = data["list_of_computer"]
        add_to_datalist(list_of_computer)
    }
    catch(error){
        alert(error)    
    }   
}

async function add_to_datalist(list_of_computer) {
    let computer_datalist = document.getElementById("computer_datalist")
    computer_datalist.innerHTML = ""
    console.log(list_of_computer)
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