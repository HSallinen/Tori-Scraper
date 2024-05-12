const makeRequest = (requestParameters: {product: string, priceMin: number,priceMax:number, city: string, distance: number, email: string}) => {
    fetch('/backend/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestParameters)
    })
    .then(resp => resp.json()) // or, resp.text(), etc
    .then(data => {
        console.log(data); // handle response data
    })
    .catch(error => {
        console.error(error);
    });
};

export default makeRequest