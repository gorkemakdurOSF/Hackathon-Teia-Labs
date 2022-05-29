import React from "react";
import template from "./Home.jsx";
import clothesService from "../../services/Clothes";

class Home extends React.Component {
    constructor() {
        super();

        this.state = {
            clothes: [],
        };
    }

    componentDidMount() {
        clothesService.getAllClothes()
            .then((clothes) => {
                console.log(clothes)
                this.setState({ clothes })
            });
    }

    render() {
        const { clothes } = this.state
        return template(clothes);
    }
}

export default Home;
