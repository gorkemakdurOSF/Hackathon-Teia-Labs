import React from "react";
import template from "./Product.jsx";

class Product extends React.Component {
  constructor(props) {
    super();

    const { liked, isLikeable, isShoppable } = props;
    this.state = {
      liked,
      isLikeable,
      isShoppable,
      isHover: false,
    };
  }

  hover = (state) => {
    this.setState({ isHover: state });
  };

  like = () => {
    this.setState((prevState) => ({
      liked: !prevState.liked
    }));
  };

  render() {
    const { liked, isLikeable, isShoppable, isHover } = this.state;
    return template(
      liked, 
      this.hover, 
      isHover, 
      isLikeable, 
      isShoppable,
      this.like,
    );
  }
}

export default Product;
