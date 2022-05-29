


export function checkURLParam(url, paramName, paramValue) {
    if (!url.endsWith('&')) {
        url += '?'
    }
    return url + `${paramName}=${paramValue}&`;
}