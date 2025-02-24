function process_data(data) {
    let keys = new Set()

    data.forEach(element => {
        Object.keys(element).forEach(key=> keys.add(key))
    });

    const outputDiv = document.getElementById("output");

    keys.forEach(key=> {

        const sectionDiv = document.createElement("div");
        sectionDiv.style.marginBottom = "10px";

        const header = document.createElement("h2");
        header.innerHTML = `&#9656; ${key}`;
        header.style.cursor = "pointer";
        header.style.marginBottom = "5px";
        header.textContent = key;

        const contentWrapper = document.createElement("div");
        contentWrapper.style.display = "none"; 

        header.addEventListener("click", () => {
            const isOpen = contentWrapper.style.display === "block";
            contentWrapper.style.display = isOpen ? "none" : "block";
            header.innerHTML = isOpen ? `&#9656; ${key}` : `&#9662; ${key}`;
        });

        sectionDiv.appendChild(header);
        sectionDiv.appendChild(contentWrapper)


        data.forEach(obj=> {
            if (obj[key]) {
                
                Object.entries(obj[key]).forEach(([time_line,value]) => {
                    const h4 = document.createElement("h4");
                    h4.innerHTML = `&#9656; ${time_line}`;
                    // h4.textContent = time_line;
                    h4.style.cursor = "pointer";
                    h4.style.marginBottom = "5px";

                    const contentDiv = document.createElement("div");
                    contentDiv.style.display = "none";
                    
                    // document.getElementById("output").appendChild(h4)
            
                    const text = document.createElement("p");
                    text.textContent = value

                    contentDiv.appendChild(text);

                    h4.addEventListener("click",() => {
                        const isOpen = contentDiv.style.display === "block";
                        contentDiv.style.display = isOpen ? "none" : "block";
                        h4.innerHTML = isOpen ? `&#9656; ${time_line}` : `&#9662; ${time_line}`;
                    });

                    contentWrapper.appendChild(h4)
                    contentWrapper.appendChild(contentDiv)
                })
            };
            
        });
        outputDiv.appendChild(sectionDiv);        
    });

}

function make_link_list(link_list) {
    const container = document.getElementById("link_list_div");
    container.innerHTML = ""

    link_list.forEach(link => {
        const a = document.createElement("a")
        a.href = "\\download\\" + link
        a.textContent = link.split("\\").pop()
        a.download = a.textContent
        a.style.display = "block"
        container.appendChild(a)
    })
}

async function stop_computer() {
    response = await fetch("http://127.0.0.1:5000/" + window.computer_data.mac_name + "/stop")
    if (response.ok) {
        alert("computer stopped")
    }
}        