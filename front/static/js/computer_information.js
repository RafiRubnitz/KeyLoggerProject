function process_data(data) {
    let keys = new Set()

    data.forEach(element => {
        Object.keys(element).forEach(key=> keys.add(key))
    });

    keys.forEach(key=> {
        const header = document.createElement("h2");
        header.textContent = key;
        document.getElementById("output").appendChild(header);


        data.forEach(obj=> {
            if (obj[key]) {
                
                Object.entries(obj[key]).forEach(([time_line,value]) => {
                    const h4 = document.createElement("h4");
                    h4.textContent = time_line
                    document.getElementById("output").appendChild(h4)
            
                    const text = document.createElement("p");
                    text.textContent = value
                    document.getElementById("output").appendChild(text)
                })
            };
        });
        
    });

}