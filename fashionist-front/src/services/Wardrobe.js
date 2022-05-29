import client from './Base';

const endpoint = '/wardrobes';


export async function getWardrobe(id, outfitsOffset, outfitsLimit, clothesOffset, clothesLimit) {
    let url = `${endpoint}/${id}`;
    url = urlParamCheck(url, 'outfits_offset', outfitsOffset);
    url = urlParamCheck(url, 'outfits_limit', outfitsLimit);
    url = urlParamCheck(url, 'clothes_offset', clothesOffset);
    url = urlParamCheck(url, 'clothes_limit', clothesLimit);

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

export async function createWardrobe(clothes, outfits) {
    return new Promise((resolve, reject) => {
        client.post(endpoint, { clothes, outfits })
            .then((response) => {
                resolve(response.data);
            })
            .catch((error) => {
                reject(new Error(error));
            });
    });
}

export async function updateWardrobe(id, clothes, outfits) {
    return new Promise((resolve, reject) => {
        client.put(`endpoint/${id}`, { clothes, outfits })
            .then((response) => {
                resolve(response.data);
            })
            .catch((error) => {
                reject(new Error(error));
            });
    });
}

export async function deleteWardrobe(id) {
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