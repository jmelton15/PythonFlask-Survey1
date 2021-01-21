$(document).ready(function () {


    async function get_Json() {
        const url = window.location
        let response = await axios.get(`${url}`)
        return response
    }
    
    $home = $("#home-btn");

    $home.on("click", async function() {
        let response = await get_Json();
        response = [];
        const url = window.location
        await axios.post(`${url}`,response);
    });
    

})