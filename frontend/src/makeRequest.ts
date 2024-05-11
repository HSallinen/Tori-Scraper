const makeRequest = (requestParameters: any) => {
    let request = new XMLHttpRequest();
    request.open("GET", "http://127.0.0.1:8000/")
    request.send()
}
export default makeRequest