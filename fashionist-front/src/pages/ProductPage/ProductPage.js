import React    from "react";
import template from "./ProductPage.jsx";

class ProductPage extends React.Component {
  render() {
    return template.call(this);
  }
}

export default ProductPage;
