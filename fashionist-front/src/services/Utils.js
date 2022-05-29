


export default function checkURLParam(url, paramName, paramValue) {
    if (paramValue) {
        if (!url.endsWith('&')) {
            url += '?'
        }
        return url + `${paramName}=${paramValue}&`;
    }

    return url;
}