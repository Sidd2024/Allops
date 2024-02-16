document.addEventListener('DOMContentLoaded',()=>{

    //Selects every save button of opportunity card and calls save_it function.
    document.querySelectorAll('.fa-bookmark').forEach(div => {
        div.onclick = function(e) {
            e.preventDefault();
            save_it(this);
        };
});
    //Selects every save button of opportunity card and calls share_id function.
    document.querySelectorAll('.fa-share-alt').forEach(div => {
        div.onclick = function(e) {
            e.preventDefault();
            share_it(this);
        };
    });

    //fetches the data from django function and changes the class name of bookmark icon.
    async function save_it(element) {
        await fetch(`/save_it/${element.dataset.id}`)
        .then(response => response.json())
        .then(data =>{
            element.className = data.css;
        });
    };
    
    //Copies the link of opportunity on the user's clipboard and some inner html.
    function share_it(element) {
        let link = `http://127.0.0.1:8000/opportunity/${element.dataset.id}`;
        navigator.clipboard.writeText(link);
        var span = document.createElement('span');
        element.appendChild(span);
        span.innerHTML = ` Link Copied!`;
        span.className = 'share-span'
    }

    //Submits the filter form if changes detected.
    document.getElementById('interest-form').onchange = ()=> {
        document.getElementById('interest-form').submit();
    }

    //Adds a placeholder to the search filter.
    document.getElementById('id_title').placeholder = "  Search opportunities by keyword";
    
});
