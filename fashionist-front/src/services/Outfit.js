import client from './Base';
import urlParamCheck from './Utils';

const endpoint = '/clothes';


export async function getAllOutfits(tags, wardrobeId, offset, limit) {
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

export async function getOutfit(id, wardrobeId) {
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

export async function suggestOutfit(id, wardrobeId) {
    let url = `${endpoint}/2323/outfits`;

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

export async function createOutfit(clothes, tags) {
    return new Promise((resolve, reject) => {
        client.post(endpoint, { clothes, tags })
            .then((response) => {
                resolve(response.data);
            })
            .catch((error) => {
                reject(new Error(error));
            });
    });
}

export async function updateOutfit(id, clothes, tags) {
    return new Promise((resolve, reject) => {
        client.put(`endpoint/${id}`, { clothes, tags })
            .then((response) => {
                resolve(response.data);
            })
            .catch((error) => {
                reject(new Error(error));
            });
    });
}

export async function deleteOutfit(id) {
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
    getAllOutfits,
    getOutfit,
    createOutfit,
    suggestOutfit,
    updateOutfit,
    deleteOutfit,
}