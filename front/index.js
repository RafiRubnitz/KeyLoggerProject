counter = 0
font_size = 20

the_computer_list = ["computer1","computer2","computer3"]

function get_data() {
    let dropdown = document.getElementById("computer_options")

    // computer_list = get_computer_list_from_server()
    computer_list = the_computer_list
    computer_list.forEach(function(computer_name) {
        let option = document.createElement("option");
        option.text = computer_name;
        
        dropdown.add(option);
    });
}


function get_computer_list_from_server() {
    let computer_list = []
    return computer_list
}

function get_select_options() {
    let dropdown = document.getElementById("computer_options")
    let selectoption = dropdown.options[dropdown.selectedIndex].text
    let result = document.getElementById("result")
    result.textContent = selectoption
}

// function get_data() {
    // // document.getElementById("get_data").style.color = "green"
    // if (counter == 0){
    //     document.getElementById("list").innerHTML = new_line()    
    // }
    // else {
    //     document.getElementById("list").innerHTML += new_line()
    //     document.getElementById("list").style.fontSize = increase_font_size()
    // }
// }


function new_line() {
    
    return 'line ' + String(++counter) + '\n'

}

function increase_font_size() {

    return String(++font_size) + "px"

}

function add_computer_option()
{
    let 
}
