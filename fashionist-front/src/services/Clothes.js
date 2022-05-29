import client from './Base';
import urlParamCheck from './Utils';

const endpoint = '/clothes';


export async function getAllClothes(tags, wardrobeId, offset, limit) {
    let url = endpoint;

    if (tags) {
        if (!url.endsWith('&')) {
            url += '?'
        }
        for (let tag of tags) {
            url += `tags[]=${tag}&`
        }
    }

    url = urlParamCheck(url, 'wardrobe_id', wardrobeId);
    url = urlParamCheck(url, 'offset', offset);
    url = urlParamCheck(url, 'limit', limit);


    if (url.endsWith('&')) {
        url = url.substring(0, url.length - 2);
    }

    return new Promise((resolve, reject) => {
        client.get(url)
            .then((response) => {
                resolve(response.data);
            })
            .catch((error) => {
                reject(error);
            });
    });
}

export async function getClothes(id, wardrobeId) {
    let url = `${endpoint}/${id}`;
    url = urlParamCheck(url, 'wardrobe_id', wardrobeId);

    return new Promise((resolve, reject) => {
        client.get(url)
            .then((response) => {
                resolve(response.data);
            })
            .catch((error) => {
                reject(new Error(error));
            });
    });
}

export async function createClothes(url, tags) {
    return new Promise((resolve, reject) => {
        client.post(endpoint, { url, tags })
            .then((response) => {
                resolve(response.data);
            })
            .catch((error) => {
                reject(new Error(error));
            });
    });
}

export async function updateClothes(id, tags) {
    return new Promise((resolve, reject) => {
        client.put(`endpoint/${id}`, { tags })
            .then((response) => {
                resolve(response.data);
            })
            .catch((error) => {
                reject(new Error(error));
            });
    });
}

export async function deleteCLothes(id) {
    return new Promise((resolve, reject) => {
        client.delete(`endpoint/${id}`)
            .then((response) => {
                resolve(response.data);
            })
            .catch((error) => {
                reject(new Error(error));
            });
    });
}

export default {
    getAllClothes,
    getClothes,
    createClothes,
    updateClothes,
    deleteCLothes
};